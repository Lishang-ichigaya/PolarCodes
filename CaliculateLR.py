import numpy as np
from decimal import Decimal

#i + n * branch,  m=log2(n)

def CalculateLR(N, chaneloutput_y, i, estimatedcodeword_u, LRmatrix, branch):
    """
    尤度比LRを計算する
    N:符号長
    chaneloutpuy_y:受信したビット列
    i:推定したいビット位置
    estimatedcodeword_u:現在までに推定された符号語ビット列
    """
    
    M = int(np.log2(N))
    if LRmatrix[i + N * branch][M] != Decimal("-1"):
        #計算済みのLR(i, n, branch)
        return LRmatrix[i + N * branch][M]

    if N == 1:
        LR_1 = Decimal(0.11/0.89) if chaneloutput_y == np.array([1]) else Decimal(0.89/0.11)
        LRmatrix[i + N * branch][M] = LR_1
        return LRmatrix[i + N * branch][M]
    
    y_1 = chaneloutput_y[:int(N/2)]
    y_2 = chaneloutput_y[int(N/2):]

    if i > 1:
        # ここからuが存在するとき
        hat_u_i = estimatedcodeword_u[i-1]

        j = i if i % 2 == 0 else i-1
        # ⇔ j-1 = i-1 or i-2
        estimatedcodeword_u = estimatedcodeword_u[:j]

        # 偶数と奇数に分解
        hat_u1 = estimatedcodeword_u[::2]
        hat_u2 = estimatedcodeword_u[1::2]

        # 偶奇でxor、奇数はそのまま
        hat_u1 = hat_u1 ^ hat_u2
        hat_u2 = hat_u2
    else:
        # uが存在しないときのそうさ
        # ⇔ i<=1
        if i == 1:
            hat_u_i = estimatedcodeword_u[0]

        j = 0
        hat_u1 = np.array([], dtype=np.uint8)
        hat_u2 = np.array([], dtype=np.uint8)

    #Arikanが提案した再起式に従って、再帰的に計算。
    if i % 2 == 0:
        LR1 = CalculateLR(int(N/2), y_1, int(j/2), hat_u1, LRmatrix, 2*branch)
        LR2 = CalculateLR(int(N/2), y_2, int(j/2), hat_u2, LRmatrix, 2*branch+1)
        LR = (
            (LR1 * LR2 + 1)
            /
            (LR1 + LR2)
        )
    else:
        LR1 = CalculateLR(int(N/2), y_1, int(j/2), hat_u1, LRmatrix, 2*branch)
        LR2 = CalculateLR(int(N/2), y_2, int(j/2), hat_u2, LRmatrix, 2*branch+1)
        if hat_u_i == 0:
            LR = LR1 * LR2
        else:
            LR = np.reciprocal(LR1) * LR2
    LRmatrix[i + N * branch][M] = LR
    return LR

"""
N = 8
output = np.array([0,0,1,0,0,0,0,0], dtype=np.uint8)
i = 0
hat_u = np.array([], dtype=np.uint8)

print("受信系列:\t\t", output)
print("i-i番目までの復号系列:\t", hat_u)
LR = CalculateLR(N, output, i, hat_u)
print("LR: " ,LR)
print("u_",i," = ", 0 if LR>=1 else 1)
"""
"""
        test1 = np.array([1,0,0,1])
        test2 = np.array([1,0,1,0])

        test3 = np.bitwise_xor(test1,test2)
        print(test1)
        print(test2)
        print(test3)
"""
