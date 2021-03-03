import time
from operations import *
def print_matrix(A):
    print("Matrix")
    for i in range(len(A)):
        for j in range(len(A)):
            print(A[i][j], end=" ")
        print()


def Jakobi(A, b):
    N = len(A)
    res = []
    r = ones(N)
    tmp = zeros(N)
    res = sub(dot_product(A, r), b)
    k = 0
    r = ones(N)
    time0 = time.time()
    while norm(res) > 10 ** (-9):
        for i in range(len(A)):
            v = 0
            for j in range(len(A)):
                if i != j:
                    v = v + A[i][j] * r[j]
            tmp[i] = (b[i] - v) / A[i][i]

        r = copy(tmp)
        res = sub(dot_product(A, r), b)
        k += 1
    time_dif = time.time() - time0
    return r, k, time_dif


def Gauss_Seidel(A, b):
    N = len(A)
    res = []
    r = ones(N)
    res = sub(dot_product(A, r), b)
    tmp = zeros(N)
    k = 0
    res = ones(N)
    time0 = time.time()
    while norm(res) > 10 ** -9:
        for i in range(len(A)):
            v = 0
            for j in range(len(A)):
                if i != j:
                    v = v + A[i][j] * r[j]
            tmp = (b[i] - v) / A[i][i]
            r[i] = tmp
        res = sub(dot_product(A, r), b)
        k += 1
    time_dif = time.time() - time0
    return r, k, time_dif


def LU(A, b, x):
    N = len(A)
    time0 = time.time()
    # wyznaczenie L i U
    L, U = findLU(A)
    # rozwiazywanie rownania
    # y = Ux
    y = dot_product(U, x)
    # Ly=b forward subs.
    for i in range(N):
        sigma = 0
        for j in range(i):
            sigma = sigma + L[i][j] * y[j]
        y[i] = (b[i] - sigma) / L[i][i]
    # y = Ux backward subs.
    for i in range(N - 1, -1, -1):
        beta = 0
        for j in range(i + 1, N):
            beta = beta + U[i][j] * x[j]
        x[i] = (y[i] - beta) / U[i][i]
    time_dif = time.time() - time0
    res = sub(dot_product(A, x), b)
    print("Norm: ", norm(res))
    return x, time_dif

def LUpivot(A,b,x):
    N = len(A)
    U = copy(A)
    L = []
    P = []
    y = []
    for i in range(N):
        temp1 = []
        temp2 = []
        for j in range(N):
            temp1.append(0)
            temp2.append(0)
        P.append(temp1)
        L.append(temp2)
        y.append(0)
    for i in range(N):
        L[i][i] = 1
        P[i][i] = 1
    time0 = time.time()
    for k in range(N):
        ind = k
        max_el = U[k][k]
        for j in range(k,N):
            if abs(U[j][k]) > max_el:
                ind = j
                max_el = abs(U[j][k])
        for j in range(k,N):
            temp = U[k][j]
            U[k][j] = U[ind][j]
            U[ind][j] = temp
        for j in range(k):
            if k == 0:
                break
            temp = L[k][j]
            L[k][j] = L[ind][j]
            L[ind][j] = temp
        for j in range(N):
            temp = P[k][j]
            P[k][j] = P[ind][j]
            P[ind][j] = temp
        for j in range(k+1,N):
            L[j][k] = U[j][k]/U[k][k]
            for i in range(k,N):
                U[j][i] = U[j][i] - L[j][k]*U[k][i]
    new_b = dot_product(P,b)
    # Ly=b forward subs.
    for i in range(N):
        sigma = 0
        for j in range(i):
            sigma = sigma + L[i][j] * y[j]
        y[i] = (new_b[i] - sigma) / L[i][i]
    # y = Ux backward subs.
    for i in range(N-1,-1,-1):
        beta = 0
        for j in range(i + 1, N):
            beta = beta + U[i][j] * x[j]
        x[i] = (y[i] - beta) / U[i][i]
    time_dif = time.time() - time0
    res = sub(dot_product(A, x), b)
    print("Norm: ", norm(res))
    return x, time_dif