from math import sin


def generate_matrices(a1, N):
    # a1 = 14.0 | 3.0
    a2 = -1.0
    a3 = -1.0
    A = []
    for i in range(N):
        temp = []
        for j in range(N):
            if i == j:
                temp.append(a1)
            elif j + 1 == i or j - 1 == i:
                temp.append(a2)
            elif j + 2 == i or j - 2 == i:
                temp.append(a3)
            else:
                temp.append(0.0)
        A.append(temp)
    b = []
    for i in range(N):
        b.append(sin(2 * i))
    x = []
    for i in range(N):
        x.append(0.0)

    return A, b, x