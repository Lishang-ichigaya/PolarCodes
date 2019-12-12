//
// common.c
//
// source_{enc,dec}.c
// channel_enc_dec.c
// と同じディレクトリに置く
//
typedef struct ldi
{
    double zero; // D もしくはL の分子
    double one;  // D もしくはL の分母
} ldi;
ldi **nd; // D もしくはL の格納用

int n, m;
// 系列u[0..n-1] を表示する．
void print_seq(char *u)
{
    int i;
    for (i = 0; i < n; i++)
    {
        printf("%d", u[i]);
    }
    printf("\n");
}
// B_n の操作を行う
unsigned int bitrev(unsigned int b)
{
    //左:1から始まる，右:0から始まる　ような01が特定の数ごとに変化するやつ
    b = (b & 0x55555555) << 1 | (b & 0xaaaaaaaa) >> 1;
    b = (b & 0x33333333) << 2 | (b & 0xcccccccc) >> 2;
    b = (b & 0x0f0f0f0f) << 4 | (b & 0xf0f0f0f0) >> 4;
    b = (b & 0x00ff00ff) << 8 | (b & 0xff00ff00) >> 8;
    b = (b & 0x0000ffff) << 16 | (b & 0xffff0000) >> 16;
    //b = (b & 0x00000000ffffffff) << 32 | (b & 0xffffffff00000000) >> 32;
    return b >> (32 - m);
}
// s T_n の操作を行う．
void matrixt(char *s)
{
    int i, j;
    for (i = 1; i <= m; i++)
    {
        for (j = 0; j < n; j++)
        {
            if ((j % (1 << i)) < (1 << (i - 1)))
            {
                s[j] = s[j] ^ s[(1 << (i - 1)) + j];
            }
        }
    }
}