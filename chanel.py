import numpy as np
from numpy.random import rand


class BSC:
    def __init__(self, P=0.11):
        self.P = P

    def Transmission(self, N, input):
        output = np.array([], dtype=np.uint8)
        for i in range(N):
            noise = 0 if rand() > self.P else 1
            tmp = (input[i] + noise) % 2
            output = np.insert(output, i, tmp)
        return output

"""
NNN = 12
message = np.array([1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1])
print("送信メッセージ:", end="")
print(message)
bsc = BSC()
output = bsc.Transmission(NNN, message)
print("受信メッセージ:", end="")
print(output)

count = 0
times =5000
for i in range(times):
    message = np.array([1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1])
    bsc = BSC(0.9)
    output = bsc.Transmission(NNN, message)
    for j in range(NNN):
        if output[j] != message[j]:
            count += 1

print(count/(times*NNN) )
"""