import numpy as np
from CaliculateLR import CalculateLR
from decimal import Decimal

def GetGeneratorMatrix(N):
    """
    ポーラ符号の生成行列を作成
    M: 符号長N
    """
    M = int(np.log2(N))

    matrixF = np.array([[1, 0], [1, 1]], dtype=np.uint8)

    matrixG = matrixF
    for i in range(1, M):
        tmp = matrixG
        matrixG = np.dot(
            GetPermutationMatrix(i+1),
            np.kron(matrixF, tmp)
        )
    return matrixG


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


def GetInformationIndex(K, path):
    """
    情報ビットに対応するインデックス集合を得る
    K:メッセージの長さ
    """
    informationindex = np.loadtxt(path, dtype=np.uint16)
    #N = 65536 までは耐えられるようにunit16を使う
    #unit8 だとN=256までしか使えない
    informationindex = np.flip(informationindex)
    # 相互情報量の小さい順に、インデックスを並べ替えたものを外部で用意しておく
    return np.sort(informationindex[:K])


class CodeWorde:
    def __init__(self, N):
        """
        符号語の初期化
        N:符号長
        """
        self.N = N
        # メッセージのビット数
        self.codeword = np.zeros(N, dtype=np.uint8)

    def MakeCodeworde(self, K, message,path, checker=True):
        """
        符号語を生成
        K: メッセージ長
        message: メッセージ
        path: インデックスを小さい順に並べたファイルのパス
        checker: メッセージもどきを表示するか否か
        """
        j = 0
        informationindex = GetInformationIndex(K,path)
        for i in range(self.N):
            if i == informationindex[j]:
                self.codeword[i] = message[j]
                j += 1
                if j > K-1:        #jが範囲を超えないように調整
                    j = K-1
            else:
                self.codeword[i] = 0
        if checker == True:
            print("メッセージもどき： \t", self.codeword)
        self.codeword = np.dot(self.codeword, GetGeneratorMatrix(self.N)) % 2
        self.codeword = self.codeword.A1
        #arrayで返す

    def DecodeOutput(self, K, N, chaneloutput,path):
        """
        符号語推定値を通信路出力から推定する
        K: メッセージ長
        N: 符号長
        chaneloutput: 通信路出力
        """
        estimatedcodeword = np.array([], dtype=np.uint8)
        informationindex = GetInformationIndex(K, path)
        LRmatrix = np.full((N ,  int(np.log2(N))+1  ), Decimal("-1"))
        #LRの値を格納する配列
        j = 0
        for i in range(N):
            if i == informationindex[j]:
                hat_ui = self.EstimateCodeword_ibit(N, chaneloutput, i, estimatedcodeword, LRmatrix)
                j += 1
            else:
                hat_ui = 0
            estimatedcodeword = np.insert(estimatedcodeword, i, hat_ui)
        
        self.codeword = estimatedcodeword
        

    def EstimateCodeword_ibit(self, N, chaneloutput, i, estimatedcodeword, LRmatrix):
        """
        符号語のibit目を求める
        """
        LR = CalculateLR(N, chaneloutput, i, estimatedcodeword, LRmatrix, 0)
        return 0 if LR >= 1 else 1

    def DecodeMessage(self, K ,path):
        """
        メッセージを符号語から復元
        K: メッセージ長
        path: インデックスを小さい順に並べたファイルのパス
        """
        informationindex =np.sort(GetInformationIndex(K,path)[:K])
        j = 0
        message = np.array([],dtype=np.uint8)

        for i in range(self.N):
            if i == informationindex[j]:
                message_j = self.codeword[i] 
                message = np.insert(message,j,message_j)
                j += 1
                if j > K-1:
                    j = K-1
        return message


# tt = GetGeneratorMatrix(3)
# print(tt)
# ttt = CodeWorde(16)
# print(ttt.codeword)


if __name__ == "__main__":
    GetInformationIndex(128,"sort_I_9_0.11_20.dat")