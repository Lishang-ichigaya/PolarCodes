import numpy as np
from numpy.random import rand


class BSC:
    def __init__(self, P):
        self.P = P
        self.input = np.array([], dtype=np.uint8)
        self.output = np.array([], dtype=np.uint8)

    def Transmission(self):
        for i in range(np.size(self.input)):
            noise = 0 if rand() > self.P else 1
            tmp = (self.input[i] + noise) % 2
            self.output = np.insert(self.output, i, tmp)


class BEC:
    def __init__(self, e):
        self.e = e
        self.input = np.array([], dtype=np.uint8)
        self.output = np.array([], dtype=np.uint8)

    def Transmission(self):
        for i in range(np.size(self.input)):
            tmp = self.input[i] if rand() > self.e else 3
            self.output = np.insert(self.output, i, tmp)


if __name__ == "__main__":
    N = 16
    input = np.array([1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0])

    bsc = BSC(1)
    bsc.input = input
    bsc.Transmission()
    
    output = bsc.output
    print(input)
    print(output)

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
