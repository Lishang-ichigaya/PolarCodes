import numpy as np
from CaliculateLR import CalculateLR_BSC
from CaliculateLR import CalculateLR_BEC
from decimal import Decimal
from Encoder import GetInformationIndex
from Encoder import GetGeneratorMatrix


class Decoder:
    def __init__(self, K, N, chaneloutput, chaneltype, path, checker=True):
        """
        デコーダクラスの初期化
        K:メッセージ長
        N:符号長
        chaneloutput: 0,1の通信路出力
        chaneltype: 通信路の種類
        path: 相互情報量の小さい順にインデックスを並べたファイルのパス
        checker: メッセージもどきを表示するか否か
        """
        self.K = K
        self.hat_message = np.array([])         #推定したメッセージを格納
        self.N = N
        self.hat_message_prime = np.array([])   #推定したメッセージもどきを格納
        self.chaneloutput = chaneloutput
        self.chaneltype = chaneltype            #通信路の種類を指定
        self.path = path
        self.checker = checker

    def DecodeOutput(self, P):
        """
        符号語推定値を通信路出力から推定する
        P: 誤り確率
        """
        estimatedcodeword = np.array([], dtype=np.uint8)
        informationindex = GetInformationIndex(self.K, self.path)
        LRmatrix = np.full((self.N,  int(np.log2(self.N))+1), Decimal("-1"))
        # LRの値を格納する配列
        j = 0
        for i in range(self.N):
            if i == informationindex[j]:
                hat_ui = self.EstimateCodeword_ibit(
                    P, self.N, self.chaneloutput, i, estimatedcodeword, LRmatrix)
                j += 1
            else:
                hat_ui = 0
            estimatedcodeword = np.insert(estimatedcodeword, i, hat_ui)

        self.hat_message_prime = estimatedcodeword

    def EstimateCodeword_ibit(self, P, N, chaneloutput, i, estimatedcodeword, LRmatrix):
        """
        符号語のibit目を求める
        """
        if self.chaneltype=="BSC":
            LR = CalculateLR_BSC(P, N, chaneloutput, i, estimatedcodeword, LRmatrix, 0)
            return 0 if LR >= 1 else 1
        elif self.chaneltype=="BEC":
            LR = CalculateLR_BEC(P, N, chaneloutput, i, estimatedcodeword, LRmatrix, 0)
            return 0 if LR >= 1 else 1
        else:
            exit(1)

    def DecodeMessage(self, P):
        """
        メッセージを符号語から復元
        K: メッセージ長
        path: インデックスを小さい順に並べたファイルのパス
        """
        self.DecodeOutput(P)
        if self.checker == True:
            print("メッセージもどき推定値:\t", self.hat_message_prime)
        
        informationindex = np.sort(GetInformationIndex(self.K, self.path)[:self.K])
        j = 0
        message = np.array([], dtype=np.uint8)

        for i in range(self.N):
            if i == informationindex[j]:
                message_j = self.hat_message_prime[i]
                message = np.insert(message, j, message_j)
                j += 1
                if j > self.K-1:
                    j = self.K-1
        self.hat_message = message


if __name__ == "__main__":
    K = 16
    N = 32
    path = "./sort_I/sort_I_5_0.11_20.dat"
    chaneloutput = np.array([0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1,
                             1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1])

    decoder0 = Decoder(K, N, chaneloutput, "BSC", path)
    #decoder0.DecodeOutput(0.11)
    decoder0.DecodeMessage(0.11)

   #    print(decoder0.hat_message_prime)
    print(decoder0.hat_message)