import numpy as np
from numpy.random import rand


class Message:
    def __init__(self, K):
        """
        メッセージの初期化 
        K:メッセージの長さ
        """
        self.K = K
        # メッセージのビット数
        self.message = np.zeros(K, dtype=np.uint8)
        # メッセージ

    def MakeMessage(self, P=0.5):
        """
        メッセージの作成
        P=0.5:0の出現確率
        """
        for i in range(self.K):
            self.message[i] = 0 if rand() > P else 1
    
class HatMessage(Message):
    #メッセージの推定値をを保持するクラス。名前だけ変えた。
    pass


"""
tttmessage = Message(3)
tttmessage.MakeMessage()
print(tttmessage.message)
"""