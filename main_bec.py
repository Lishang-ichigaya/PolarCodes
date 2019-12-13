from subprocess import check_call
import numpy as np
import sys
import time

from message import Message
#from codeword import CodeWorde
from Encoder import Encoder
from chanel import BEC
from Decoder import Decoder


if __name__ == '__main__':
    K = 16
    N = 32
    M = int(np.log2(N))
    chaneltype = "BEC"
    e = 0.5
    path = "./sort_I/sortI_BEC_"+ str(e) + "_" + str(N) + ".dat"
    # path ="./polarcode/"+"sort_I_" + str(M) + "_" + str(P) + "_" + "20" + ".dat"

    if len(sys.argv) == 2:
        if sys.argv[1] == "ber":
            eroorcount = 0
            frameerrorcout = 0
            kaisu = 100

            start = time.time()
            for i in range(kaisu):
                message = Message(K)
                message.MakeMessage()

                encoder0 = Encoder(K, N, message.message, path, False)
                encoder0.MakeCodeworde()
                
                bec = BEC(e)
                bec.input = encoder0.codeword
                bec.Transmission()
                output = bec.output
            
                decoder0 = Decoder(K, N ,output, "BEC", path, False)
                decoder0.DecodeMessage(e)

                error = np.bitwise_xor(message.message, decoder0.hat_message)
                eroorcount += np.count_nonzero(error)

                frameerrorcout += 0 if np.count_nonzero(error) == 0 else 1
                print(i, "/", kaisu, "回目, ",
                      0 if np.count_nonzero(error) == 0 else 1)
            end = time.time()

            print("送信:", K*kaisu, "復号誤り:", eroorcount)
            print("FER: ", frameerrorcout/kaisu)
            print("BER: ", eroorcount/(K*kaisu))
            print("実行時間: ", end-start)

    if len(sys.argv) == 1:
        print("K=", K, "N=", N)

        message = Message(K)
        message.MakeMessage()
        print("メッセージ:\t\t", message.message)

        encoder0 = Encoder(K, N, message.message, path)
        encoder0.MakeCodeworde()
        print("符号語:\t\t\t", encoder0.codeword)

        bec = BEC(e)
        bec.input = encoder0.codeword
        bec.Transmission()
        output = bec.output
        print("通信路出力:\t\t", output)


        decoder0 = Decoder(K, N ,output, chaneltype, path)
        decoder0.DecodeMessage(e)
        #↑復号
        hat_message = Message(K)
        hat_message.message = decoder0.hat_message
        print("メッセージ推定値:\t", hat_message.message)

        error = np.bitwise_xor(message.message, hat_message.message)
        print("誤り数:", np.count_nonzero(error))
