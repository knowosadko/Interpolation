from time import sleep

import numpy as np
import pandas as pd
import Algorithms
import matplotlib.pyplot as plt
import operations
import os


def main():
    path = '2018_paths'
    for filename in os.listdir(path):
        data = pd.read_csv(os.path.join(path, filename), sep=",", header=None)
        data_list = [list(row) for row in data.values]
        rng = 5 # 20 -> 27,  10 -> 52, 5 - 104
        input_frame = create_input_data(data, rng)
        input_list = input_frame.values.tolist()
        input_list.append(data_list[-1])
        output_lagrange = []
        for i in data_list:
            temp = []
            temp.append(i[0])
            temp.append(lagrange_interpolation(i[0],input_list))
            output_lagrange.append(temp)

        x_inter = []
        y_lagrange = []
        x = []
        y = []
        x_points = []
        y_points = []
#lagrange
        for i in range(len(output_lagrange)):
            x_inter.append(output_lagrange[i][0])
            y_lagrange.append(output_lagrange[i][1])
            x.append(data_list[i][0])
            y.append(data_list[i][1])
        for i in range(len(input_list)):
            x_points.append(input_list[i][0])
            y_points.append(input_list[i][1])
        max, min = max_min(y)
        plt.figure()
        plt.plot(x_points, y_points,'o' ,color='yellow', label="knots")
        plt.plot(x,y, color = 'blue' , label="input data")
        plt.plot(x_inter, y_lagrange, color ='red',label="interpolation")
        plt.ylim(0.8*min, 1.1*max)
        plt.title("Lagrange "+filename+ " N = "+str(len(input_list)))
        plt.xlabel("length [m]")
        plt.ylabel("height [m]")
        plt.legend()
        plt.grid()
        plt.show()
# splines
        y_splines = []
        function = spline_function(input_list)
        for i in range(len(data_list)):
            y_splines.append(f(data_list[i][0], function, input_list))
        plt.figure()
        plt.plot(x_points, y_points, 'o', color='yellow',label='knots')
        plt.plot(x, y, color='blue',label='input data')
        plt.plot(x_inter,y_splines, color='red',label='interpolation')
        plt.title("Splines " + filename + " N = "+str(len(input_list)))
        plt.xlabel("length [m]")
        plt.ylabel("height [m]")
        plt.legend()
        plt.grid()
        plt.show()


def create_input_data(dataframe, rng):
    tempframe = dataframe
    for i in range(len(dataframe)):
        if i % rng > 0:
            tempframe = tempframe.drop(dataframe.index[i])
    return tempframe


def lagrange_interpolation(x, datalist) -> float:
    n = len(datalist)
    result = 0.0
    for i in range(n):
        product = datalist[i][1]
        xi = datalist[i][0]
        for j in range(n):
            xj = datalist[j][0]
            if i != j:
                product*=(x-xj)/(xi-xj)
        result += product
    return result


def spline_function(datalist):
    n = len(datalist)
    x = operations.vec_zeros(4*(n-1))
    A = operations.matrix_zeros(4*(n-1), 4*(n-1))
    b = operations.vec_zeros(4*(n-1))
    for i in range(n-1):
        h = datalist[i+1][0] - datalist[i][0]
        # a0 = f (x0)
        A[4*i][4*i] = 1
        b[4*i] = datalist[i][1]
        # a0 + b0h + c0h**2 + d0h**3 = f(x1)
        A[4*i+1][4*i] = 1
        A[4*i+1][4*i+1] = h
        A[4*i+1][4*i+2] = h**2
        A[4*i+1][4*i+3] = h**3
        b[4*i+1] = datalist[i+1][1]
        # derivatives
        if i < n-2:
            # b0 + 2c0h + 3d0h**2 - b1 = 0
            A[4*i+2][4*i+1] = 1
            A[4*i+2][4*i+2] = 2*h
            A[4*i+2][4*i+3] = 3*h**2
            A[4*i+2][4*i+5] = -1
            b[4*i+2] = 0
            # 2c0 + 6d0h - 2c1 = 0
            A[4*i+3][4*i+2] = 2
            A[4*i+3][4*i+3] = 6*h
            A[4*i+3][4*i+6] = -2
            b[4*i+3] = 0
        else:
            A[4*i+2][3] = 1
            b[4*i+2] = 0
            A[4*i+3][4*i+2] = 2
            A[4*i+3][4*i+3] = 6*h
            b[4*i+3] = 0
    function, _ = Algorithms.LUpivot(A, b, x)
    return function


def spline_interpolation(x, function, datalist):
    y = 1
    for i in range(len(datalist)-1):
        if datalist[i][0] == x:
            return datalist[i][1]
        if x < datalist[i + 1][0]:
            h = x - datalist[i][0]
            y = function[i*4] + function[i*4+1]*h + function[i*4+2]*(h**2) + function[i*4+3]*(h**3)
            return y
    return y

def max_min(list):
    max = list[0]
    min = list[0]
    for i in list:
        if i > max:
            max = i
        if i < min:
            min = i
    return max, min


def f(x, function, points):
    for i in range(len(points)-1):
        if x == points[i+1][0]:
            return points[i+1][1]
        if x < points[i+1][0]:
            h = x - points[i][0]
            a = function[4*i]
            b = function[4*i+1]
            c = function[4*i+2]
            d = function[4*i+3]
            y = a + b*h + c*h**2 + d*h**3
            return y
    return 1

if __name__ == "__main__":
    main()
