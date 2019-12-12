//
// calIdmcDp.c
//
// 実行はcalIdmc m p alpha
//
// m は符号長n=2^m
// p はBSC のcross over probability
// p は0.0 <= p <= 0.3
// alpha は近似に用いるBSC の最大個数
//
// アルゴリズムの実行例
// % cal_I_dmc 6 0.11 10
// 出力はcalIdmc.c の場合と同じであるが近似をしている
//
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
static int overflow = 0;
typedef struct sub_bsc
{
    double w; // weight
    double p; // probability of W(1|0) = W(0|1) = p
} sub_bsc;
typedef struct channel
{
    int size;
    sub_bsc *c;
} channel;
typedef struct sortidx
{
    int idx;
    double inf;
} sortidx;
typedef struct dpnode
{
    int idx;
    double inf;
} dpnode;
int compare_sub(const void *a, const void *b)
{
    sub_bsc ta = *(sub_bsc *)a;
    sub_bsc tb = *(sub_bsc *)b;
    if ((double)ta.p == (double)tb.p)
    {
        return (0);
    }
    else if ((double)ta.p > (double)tb.p)
    {
        return (1);
    }
    else
    {
        return (-1);
    }
}
int compare_inf(const void *a, const void *b)
{
    sortidx ta = *(sortidx *)a;
    sortidx tb = *(sortidx *)b;
    if ((double)ta.inf == (double)tb.inf)
    {
        return (0);
    }
    else if ((double)ta.inf > (double)tb.inf)
    {
        return (1);
    }
    else
    {
        return (-1);
    }
}
double mutualinf(double p)
{
    if (p <= 0.0 || p >= 1.0)
    {
        return 1.0;
    }
    double mi;
    mi = 1.0 + p * log2(p) + (1.0 - p) * log2(1.0 - p);
    return (mi <= 0.0) ? 0.0 : mi;
}
channel dp(channel Q, int alpha)
{
    int i, j, k;
    int idxs[alpha];
    dpnode dpn[alpha][Q.size - alpha + 1];
    double wsum = 0.0, psum = 0.0, min;
    qsort(Q.c, Q.size, sizeof(sub_bsc), compare_sub);
    for (i = 0; i < alpha - 1; i++)
    {
        for (j = 0; j < Q.size - alpha + 1; j++)
        {
            if (i == 0)
            {
                psum = (wsum * psum + Q.c[j].w * Q.c[j].p) / (wsum + Q.c[j].w);
                wsum += Q.c[j].w;
                dpn[i][j].inf = wsum * mutualinf(psum);
                dpn[i][j].idx = 0;
            }
            else
            {
                for (wsum = psum = 0.0, min = -1.0, k = j; k >= 0; k--)
                {
                    psum = (wsum * psum + Q.c[i + k].w * Q.c[i + k].p) / (wsum + Q.c[i + k].w);
                    wsum += Q.c[i + k].w;
                    if (wsum * mutualinf(psum) + dpn[i - 1][k].inf > min)
                    {
                        dpn[i][j].idx = k;
                        min = wsum * mutualinf(psum) + dpn[i - 1][k].inf;
                    }
                }
                dpn[i][j].inf = min;
            }
        }
    }
    for (wsum = psum = 0.0, min = -1.0, k = Q.size - alpha; k >= 0; k--)
    {
        psum = (wsum * psum + Q.c[i + k].w * Q.c[i + k].p) / (wsum + Q.c[i + k].w);
        wsum += Q.c[i + k].w;
        if (wsum * mutualinf(psum) + dpn[alpha - 2][k].inf > min)
        {
            dpn[alpha - 1][Q.size - alpha].idx = k;
            min = wsum * mutualinf(psum) + dpn[alpha - 2][k].inf;
        }
    }
    dpn[alpha - 1][Q.size - alpha].inf = min;
    idxs[alpha - 1] = Q.size;
    j = dpn[alpha - 1][Q.size - alpha].idx;
    for (i = alpha - 2; i >= 0; i--)
    {
        idxs[i] = i + j + 1;
        j = dpn[i][j].idx;
    }
    for (i = j = 0; i < alpha; i++)
    {
        for (wsum = psum = 0.0; j < idxs[i]; j++)
        {
            wsum += Q.c[j].w;
            psum += Q.c[j].w * Q.c[j].p;
            Q.c[i].w = (wsum < 0.0) ? 0.0 : wsum;
            Q.c[i].p = (psum / wsum < 0.0) ? 0.0 : psum / wsum;
        }
    }
    Q.size = alpha;
    return (Q);
}
channel do_even(channel Q, int alpha)
{ // XOR がある場合
    int i, j, k;
    channel Wtmp;
    double tw, tp;
    Wtmp.c = (sub_bsc *)malloc(Q.size * Q.size * sizeof(sub_bsc));
    for (k = 0, i = 0; i < Q.size; i++)
    {
        for (j = i; j < Q.size; j++)
        {
            tw = Q.c[i].w * Q.c[j].w;
            tp = Q.c[i].p + Q.c[j].p - 2.0 * Q.c[i].p * Q.c[j].p;
            if (0.0 < tw && 0.0 <= tp && tp <= 1.0)
            {
                Wtmp.c[k].w = (j == i) ? tw : 2.0 * tw;
                Wtmp.c[k++].p = (0.0 <= tp && tp <= 0.5) ? tp : 1.0 - tp;
            }
            else
            {
                overflow++;
            }
        }
    }
    Wtmp.size = k;
    if (Wtmp.size > alpha)
    {
        Wtmp = dp(Wtmp, alpha);
    }
    return (Wtmp);
}
channel do_odd(channel Q, int alpha)
{ // XOR がない場合
    int i, j, k;
    channel Wtmp;
    double tw, tp;
    Wtmp.c = (sub_bsc *)malloc(2 * Q.size * Q.size * sizeof(sub_bsc));
    for (k = 0, i = 0; i < Q.size; i++)
    {
        for (j = i; j < Q.size; j++)
        {
            tw = Q.c[i].w * Q.c[j].w *
                 (Q.c[i].p * (1.0 - Q.c[j].p) + (1.0 - Q.c[i].p) * Q.c[j].p);
            tp = (1.0 - Q.c[i].p) * Q.c[j].p / (Q.c[i].p * (1.0 - Q.c[j].p) + (1.0 - Q.c[i].p) * Q.c[j].p);
            if (0.0 < tw && 0.0 <= tp && tp <= 1.0)
            {
                Wtmp.c[k].w = (j == i) ? tw : 2.0 * tw;
                Wtmp.c[k++].p = (0.0 <= tp && tp <= 0.5) ? tp : 1.0 - tp;
            }
            else
            {
                overflow++;
            }
            tw = Q.c[i].w * Q.c[j].w *
                 (Q.c[i].p * Q.c[j].p + (1.0 - Q.c[i].p) * (1.0 - Q.c[j].p));
            tp = Q.c[i].p * Q.c[j].p / (Q.c[i].p * Q.c[j].p + (1.0 - Q.c[i].p) * (1.0 - Q.c[j].p));
            if (0.0 < tw && 0.0 <= tp && tp <= 1.0)
            {
                Wtmp.c[k].w = (j == i) ? tw : 2.0 * tw;
                Wtmp.c[k++].p = (0.0 <= tp && tp <= 0.5) ? tp : 1.0 - tp;
            }
            else
            {
                overflow++;
            }
        }
    }
    Wtmp.size = k;
    if (Wtmp.size > alpha)
    {
        Wtmp = dp(Wtmp, alpha);
    }
    return (Wtmp);
}
void calI(double p, int n, int m, int alpha, char *fn, FILE *fp)
{
    int i, j, k, l;
    channel W;
    channel **db;
    sortidx IofW[n];        // I(W_n^{(i)}) をIW[i] に保持
    double IW0, sumI = 0.0; // I(W_n^{(i)}) の和=n*I(W)
    db = (channel **)malloc((m - 1) * sizeof(channel));
    for (i = 0; i < m; i++)
    {
        db[i] = (channel *)malloc((1 << (i + 1)) * sizeof(channel));
        for (j = 0; j < (1 << (i + 1)); j++)
        {
            db[i][j].size = 0;
            db[i][j].c = NULL;
        }
    }
    for (i = 0; i < n; i++)
    { // i はI(W_n^{(i)}) のi
        l = 0;
        W.size = 1; // W.size はW におけるBSC 分解の個数
        W.c = (sub_bsc *)malloc(W.size * sizeof(sub_bsc));
        W.c[0].w = 1.0;            // W の初期化で最初のBSC のw = 1.0
        W.c[0].p = p;              // W の初期化で最初のBSC のp
        IW0 = mutualinf(W.c[0].p); // I(W) = I(BSC(p))
        for (j = 0; j < m; j++)
        { //次の?でeven とodd の判定
            if ((i & (1 << (m - j - 1))) == 0)
            {
                if (db[j][l].size != 0)
                {
                    W = db[j][l];
                }
                else
                {
                    W = db[j][l] = do_even(W, alpha);
                }
            }
            else
            {
                l++;
                if (db[j][l].size != 0)
                {
                    W = db[j][l];
                }
                else
                {
                    W = db[j][l] = do_odd(W, alpha);
                }
            }
            l = l << 1;
        }
        //情報量IofW[i] の計算
        IofW[i].idx = i;
        for (IofW[i].inf = 0.0, k = 0; k < W.size; k++)
        {
            if (W.c[k].w > 0.0)
            {
                IofW[i].inf += W.c[k].w * mutualinf(W.c[k].p);
            }
        }
        printf("%8dth I(W_%d^(%d)) = %1.5e\n", i, n, IofW[i].idx, IofW[i].inf);
        sumI += IofW[i].inf;
        free(W.c);
    }
    printf("\n");
    qsort(IofW, n, sizeof(sortidx), compare_inf);
    for (i = 0; i < n; i++)
    {
        fprintf(fp, "%d ", IofW[i].idx);
    }
    fclose(fp);
    printf("I(W) = %3.5e\t", IW0);
    printf("%d*I(W) = %3.5e\n", n, n * IW0);
    printf("Sum_i I(W_%d^(i)) = %3.5e\n", n, sumI);
    printf("Sort I(W_%d^(i)), and creat %s \n", n, fn);
}
int main(int argc, char *argv[])
{
    FILE *fp;
    int n, m, alpha;
    double p;
    char fn[50] = "sort_I_";
    char footer[] = ".dat";
    if (argc != 4)
    {
        printf("Usage: %s m p alpha\n", argv[0]);
        exit(1);
    }
    strcat(fn, argv[1]);
    strcat(fn, "_");
    strcat(fn, argv[2]);
    strcat(fn, "_");
    strcat(fn, argv[3]);
    strcat(fn, footer);
    if ((fp = fopen(fn, "w")) == NULL)
    {
        exit(1);
    }
    m = atoi(argv[1]); // n=2^m
    if (m < 0 || m > 9)
    {
        fprintf(stderr, "Bad parameter: 0 <= m <= 9");
        exit(1);
    }
    p = atof(argv[2]); // BSC のcross over probability
    if (p < 0 || p > 0.2)
    { // p は0 <= p <= 0.2
        fprintf(stderr, "Bad parameter: 0 <= p <= 0.2\n");
        exit(1);
    }
    alpha = atoi(argv[3]); // alpha はBSC の最大個数
    if (alpha < 3)
    { //出力アルファベットサイズは2*alpha
        fprintf(stderr, "Bad parameter: alpha >=3\n");
        exit(1);
    }
    n = 1 << m; // 最終的に作成する系列長2^m
    calI(p, n, m, alpha, fn, fp);
    return 0;
}
