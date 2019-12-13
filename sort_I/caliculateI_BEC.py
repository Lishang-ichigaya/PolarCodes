import csv

def CaliculateI_BEC(e, N, i):
    if N == 1 and i == 0:
        return 1-e
    if i % 2 == 1:
        I_i = CaliculateI_BEC(e, int(N/2), int(i/2))
        return 2*I_i - I_i*I_i
    if i % 2 == 0:
        I_i = CaliculateI_BEC(e, int(N/2), int(i/2))
        return I_i*I_i


if __name__ == "__main__":
    e = 0.5
    N = 32
    sum = 0
    I_i = {}
    for i in range(N):
        I = CaliculateI_BEC(e, N, i)
        I_i[i] = I
        sum += I
        print(I)
    print(sum, (1-e)*N)
    print(I_i)

    I_i = sorted(I_i.items(), key=lambda I_i:I_i[1])
    
    A = [] #情報ビットのインデックス
    for i in range(N):
        A.append(I_i[i][0])
    
    print(A)
    path = "./sortI_BEC_"+str(e)+"_"+str(N)+".dat"
    with open(path, mode='w') as f :
        for num in A:
            f.write(str(num)+' ')