//
// calIdmc.c
//
// 実行はcalIdmc p
//
// p はBSC のcross over probability
// p は0.0 <= p <= 1.0
//
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
int m = 3;
typedef struct matrix
{
    double x0; //入力0
    double x1; //入力1
} matrix;
typedef struct channel
{
    int size;  // 出力記号数|Y|
    matrix *c; // 条件付確率
} channel;
typedef struct sortidx
{               // ソート用
    int idx;    // インデックス
    double inf; // 情報量
} sortidx;
int compare_inf(const void *a, const void *b)
{ // qsort における情報量の比較のため
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
double inf(double prob)
{ // 確率x 自己情報量
    if (prob <= 0.0 || prob >= 1.0)
    {
        return 0.0;
    }
    return (-prob * log2(prob));
}
double mutualinf(matrix c)
{ // 相互情報量
    return (0.5 * (c.x0 + c.x1 + inf(c.x0 + c.x1) - inf(c.x0) - inf(c.x1)));
}
channel do_even(channel Q)
{ // XOR がある場合
    int i, j, k;
    channel Wtmp;
    Wtmp.c = (matrix *)malloc(Q.size * Q.size * sizeof(matrix));
    for (k = 0, i = 0; i < Q.size; i++)
    {
        for (j = 0; j < Q.size; j++)
        {                // 補題1 を利用
            Wtmp.c[k].x0 // for u == 0
                = 0.5 * (Q.c[i].x0 * Q.c[j].x0 + Q.c[i].x1 * Q.c[j].x1);
            Wtmp.c[k++].x1 // for u == 1
                = 0.5 * (Q.c[i].x1 * Q.c[j].x0 + Q.c[i].x0 * Q.c[j].x1);
        }
    }
    Wtmp.size = k;
    free(Q.c);
    return (Wtmp);
}
channel do_odd(channel Q)
{ // XOR がない場合
    int i, j, k;
    channel Wtmp;
    Wtmp.c = (matrix *)malloc(2 * Q.size * Q.size * sizeof(matrix));
    for (k = 0, i = 0; i < Q.size; i++)
    {
        for (j = 0; j < Q.size; j++)
        {                // 補題1 を利用
            Wtmp.c[k].x0 // (z,x)==(0,0), (z xor x)==0
                = 0.5 * Q.c[i].x0 * Q.c[j].x0;
            Wtmp.c[k++].x1 // (z,x)==(1,0), (z xor x)==1
                = 0.5 * Q.c[i].x1 * Q.c[j].x1;
            Wtmp.c[k].x0 // (z,x)==(0,1), (z xor x)==1
                = 0.5 * Q.c[i].x1 * Q.c[j].x0;
            Wtmp.c[k++].x1 // (z,x)==(1,1), (z xor x)==0
                = 0.5 * Q.c[i].x0 * Q.c[j].x1;
        }
    }
    Wtmp.size = k;
    free(Q.c);
    return (Wtmp);
}
void calI(double p, int n, char *fn, FILE *fp)
{
    int i, j, k;
    channel W;
    sortidx IW[n];          // I(W_n^{(i)}) をIW[i] に保持
    double IW0, sumI = 0.0; // I(W_n^{(i)}) の和=n*I(W)
    for (i = 0; i < n; i++)
    { // i はI(W_n^{(i)}) のi
        // 2 元対称通信路BSC の例
        W.size = 2; // W の出力記号数
        W.c = (matrix *)malloc(W.size * sizeof(matrix));
        W.c[0].x0 = 1 - p;                           // W(0|0)=P_{Y|X}(0|0)=1-p
        W.c[1].x0 = p;                               // W(1|0)=P_{Y|X}(1|0)=p
        W.c[0].x1 = p;                               // W(0|1)=P_{Y|X}(0|1)=p
        W.c[1].x1 = 1 - p;                           // W(1|1)=P_{Y|X}(1|1)=1-p
        IW0 = mutualinf(W.c[0]) + mutualinf(W.c[1]); //I(W) n 
        for (j = 0; j < m; j++)
        { //次の?でeven とodd の判定
            W = ((i & (1 << (m - j - 1))) == 0) ? do_even(W) : do_odd(W);
        }
        //情報量I(W_n^{(i)}) = IW[i] の計算
        for (IW[i].idx = i, IW[i].inf = 0.0, k = 0; k < W.size; k++)
        {
            IW[i].inf += mutualinf(W.c[k]);
        }
        printf("|Y^%dxZ^%d|=%10d, I(W_%d^(%d))=%1.5e\n", n, i, W.size, n, i, IW[i].inf);
        sumI += IW[i].inf;
        free(W.c);
    }
    printf("\n");
    qsort(IW, n, sizeof(sortidx), compare_inf);
    for (i = 0; i < n; i++)
    {
        fprintf(fp, "%d ", IW[i].idx);
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
    int n;
    double p;
    char fn[50] = "sort_I_";
    char footer[5] = ".dat";
    if (argc != 2)
    {
        printf("Usage: %s p \n", argv[0]);
        exit(1);
    }
    strcat(fn, argv[1]);
    strcat(fn, footer);
    if ((fp = fopen(fn, "w")) == NULL)
    {
        exit(1);
    }
    p = atof(argv[1]); // p はBSC でp=W(1|0)=W(0|1)
    if (p < 0.0 || p > 1.0)
    {
        fprintf(stderr, "Bad parameter: 0 <= p <= 1.0\n");
        exit(1);
    }
    n = 1 << m; // 最終的に作成する系列長2^m
    calI(p, n, fn, fp);
    return 0;
}