from math import sqrt

def split(A):
    D = []
    U = []
    L = []
    for i in range(len(A)):
        temD = []
        temL = []
        temU = []
        for j in range(len(A)):
            if i == j:
                temD.append(A[i][j])
            else:
                temD.append(0)
            if i > j:
                temU.append(A[i][j])
            else:
                temU.append(0)
            if j > i:
                temL.append(A[i][j])
            else:
                temL.append(0)
        D.append(temD)
        U.append(temU)
        L.append(temL)
    return L, D, U


def dot_product(a, b):
    tem_a = copy(a)
    tem_b = copy(b)
    m = len(tem_a)
    n = len(tem_a[0])
    c = zeros(m)

    for i in range(m):
        for l in range(n):
            c[i] += tem_a[i][l] * tem_b[l]
    return c


def matrix_product(A, B):
    N = len(A)
    ret = []
    for i in range(N):
        tem = []
        for j in range(N):
            sum = 0
            for k in range(N):
                sum += A[i][k] * B[k][j]
            tem.append(sum)
        ret.append(tem)
    return ret


def scale(x, vector):
    tem = []
    for i in range(len(vector)):
        tem.append(vector[i] * x)
    return tem


def findLU(A):
    N = len(A)
    U = copy(A)
    L = identity_matrix(N)
    for k in range(N):
        for j in range(k + 1, N):
            L[j][k] = U[j][k] / U[k][k]
            U[j][k:N] = sub(U[j][k:N], scale(L[j][k], U[k][k:N]))
    return L, U


def identity_matrix(n):
    m = []
    for i in range(n):
        tem = []
        for j in range(n):
            if i == j:
                tem.append(1)
            else:
                tem.append(0)
        m.append(tem)
    return m


def ones(N):
    res = []
    for i in range(N):
        res.append(1.0)
    return res


def zeros(N):
    res = []
    for i in range(N):
        res.append(0)
    return res


def sub(v1, v2):
    tem = []
    if len(v1) == len(v2):
        for i in range(len(v1)):
            tem.append(v1[i] - v2[i])
    return tem


def add(v1, v2):
    if len(v1) == len(v2):
        for i in range(len(v1)):
            v1[i] = v1[i] + v2[i]
    return v1


def norm(vector):
    sum = 0
    for i in range(len(vector)):
        sum = sum + vector[i] ** 2
    return sum ** 0.5


def subM(A, B):
    for i in range(len(A)):
        for j in range(len(B)):
            A[i][j] -= B[i][j]
    return A


def copy(A):
    ret = []
    if isinstance(A[0], list):
        # A is matrix
        for i in range(len(A)):
            tem = []
            for j in range(len(A[0])):
                tem.append(A[i][j])
            ret.append(tem)
    else:
        # A is vector
        for i in range(len(A)):
            ret.append(A[i])

    return ret

def matrix_zeros(n, m):
    matrix = []
    for i in range(n):
        tem = []
        for j in range(m):
            tem.append(0)
        matrix.append(tem)
    return matrix

def vec_zeros(n):
    vec = []
    for i in range(n):
        vec.append(0)
    return vec