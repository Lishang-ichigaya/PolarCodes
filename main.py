from subprocess import check_call
import numpy as np
import sys
import time

from message import Message
from codeword import CodeWorde
from chanel import BSC


if __name__ == '__main__':
    K = 200
    N = 512
    M = int(np.log2(N))
    P = 0.11
    path = "sort_I_" + str(M) + "_" + str(P) + "_" + "20" + ".dat"
    #path ="./polarcode/"+"sort_I_" + str(M) + "_" + str(P) + "_" + "20" + ".dat"

    if len(sys.argv) == 2:
        # 相互情報量を計算する場合は 'c' オプションをつける
        if sys.argv[1] == "c":
            check_call(["./calIdmcDp.exe", str(M), str(P), "20"])

        if sys.argv[1] == "ber":
            eroorcount = 0
            frameerrorcout = 0
            kaisu = 10

            start = time.time()
            for i in range(kaisu):
                message = Message(K)
                message.MakeMessage()

                codeword = CodeWorde(N)
                codeword.MakeCodeworde(K, message.message, path, False)

                bsc011 = BSC(0.11)
                output = bsc011.Transmission(N, codeword.codeword)

                estimatedcodeword = CodeWorde(N)
                estimatedcodeword.DecodeOutput(K, N, output, path)

                estimatedmessage = estimatedcodeword.DecodeMessage(K, path)

                error = np.bitwise_xor(message.message, estimatedmessage)
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

        codeword = CodeWorde(N)
        codeword.MakeCodeworde(K, message.message, path)
        print("符号語:\t\t\t", codeword.codeword)

        bsc011 = BSC(0.11)
        output = bsc011.Transmission(N, codeword.codeword)
        print("通信路出力:\t\t", output)

        estimatedcodeword = CodeWorde(N)
        estimatedcodeword.DecodeOutput(K, N, output, path)
        print("メッセージもどき推定値:\t", estimatedcodeword.codeword)

        estimatedmessage = estimatedcodeword.DecodeMessage(K, path)
        print("メッセージ推定値:\t", estimatedmessage)

        error = np.bitwise_xor(message.message, estimatedmessage)
        print("誤り数:", np.count_nonzero(error))
