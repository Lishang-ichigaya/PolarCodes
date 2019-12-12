import numpy as np


def GetPermutationMatrix(M):
    """
    偶数番目を前に、奇数番目を後ろに置き換える行列を得る
    M: 符号長Nについて、N=2^Mを満たすM

    例:
    [1,0,0,0]  [1,0,0,0]
    [0,1,0,0]->[0,0,1,0]
    [0,0,1,0]  [0,1,0,0]
    [0,0,0,1]  [0,0,0,1]
    """
    if M == 1:
        return np.identity(1, dtype=np.uint8)
    matrixI_2 = np.matrix([[1, 0], [0, 1]])
    matrixR = np.matrix([[1, 0], [0, 1]])
    for i in range(M-1):
        matrixR = np.kron(matrixI_2, matrixR)
    matrixEven, matrixOdd = matrixR[::2], matrixR[1::2]
    matrixR = np.concatenate([matrixEven, matrixOdd]).T
    return matrixR


I_2 = np.array([[1, 0], [0, 1]])
F = np.array([[1, 0], [1, 1]])


I_1F = np.array([[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 1]])
A_4 = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
I_2G_2 = np.array([[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 1]])

G_4 = np.dot(np.dot(I_1F, A_4), I_2G_2)

# print(G_4)


# print("N=8")

I_2F = np.kron(np.identity(4, dtype=np.uint8), F)
A_8 = GetPermutationMatrix(3)
I_2G_4 = np.kron(I_2, G_4)

# print(I_2F)
# print(A_8)
# print(I_2G_4)

G_8 = np.dot(np.dot(I_2F, A_8), I_2G_4)
print("生成行列")
print(G_8)

#G_8 = np.concatenate([G_8,G_8])
#G_8 = np.concatenate([G_8,G_8],axis=1)

G_8 = np.kron(np.identity(2), G_8)
print(G_8)

ih = 0
if ih % 2 == 1:
    print("aaa")
else:
    print("bbb")
