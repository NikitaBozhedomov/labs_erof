import math
from tkinter import messagebox

import matplotlib.pyplot as plt
from tkinter import *
import numpy as np

import gauss


def func(x):
    try:
        res = x*x*x*math.cos(x)+x*x*math.cos(x)+x
    except ArithmeticError:
        return ArithmeticError
    return res


def addPoints(n, a, b):
    q = open('repository.txt', 'w')
    len = b - a
    for i in range(n):
        x = a + (len / n) * i
        q.write(str(x) + " " + str(func(x)) + "\n")
    q.close()


def getPoints():
    q = open('repository.txt', 'r')
    n = 0
    arrayOfPoints = []
    try:
        for i in q:
            points = i.split()
            arrayOfPoints.append([float(points[0]), float(points[1])])
            n += 1
    except IndexError:
        q.close()
        raise IndexError
    q.close()
    nparray_of_points = np.array(arrayOfPoints)
    return nparray_of_points


def x_sum(degree, n, array_of_points):
    s = 0
    for i in range(n):
        x = array_of_points[i]
        s += math.pow(x, degree)
    return s


def y_sum(degree, n, array_of_xpoints, array_of_ypoints):
    s = 0
    for i in range(n):
        x = array_of_xpoints[i]
        y = array_of_ypoints[i]
        s += y * math.pow(x, degree)
    return s


def matrica_Gramma(nparray_of_points, m, n):
    matrix = np.zeros((m+1, m+1))
    dop = np.zeros((m+1,))
    array_of_xpoints = nparray_of_points[:, 0]
    array_of_ypoints = nparray_of_points[:, 1]

    for i in range(m+1):
        matrix[0][i] = x_sum(i, n, array_of_xpoints)
        dop[i] = y_sum(i, n, array_of_xpoints, array_of_ypoints)
        matrix[i][m] = x_sum(i + m, n, array_of_xpoints)
    for j in range(1, m+1):
        for q in range(m):
            matrix[j][q] = matrix[j-1][q+1]
    solve_array = gauss.gauss(matrix, dop)

    return solve_array


def plot_polynomial(m, n, coefficent, array_of_xpoints):
    array_of_ypoints = np.zeros((n,))
    for i in range(n):
        for j in range(m+1):
            array_of_ypoints[i] += coefficent[j] * math.pow(array_of_xpoints[i], j)

    return array_of_ypoints


def bnt_click():
    plt.style.use('seaborn-v0_8-whitegrid')
    try:
        b = float(loginOfb.get())
        a = float(loginOfa.get())
        n = int(loginOfn.get())
        m = int(loginOfm.get())
    except ValueError:
        messagebox.showerror(title='Ошибка типа данных', message='введите данные корректно')
        return
    if m > n or m < 0:
        messagebox.showerror(title='Некорректная степень многочлена', message='введите степень многочлена корректно')
        return
    if a >= b :
        messagebox.showerror(title='Неверно введены границы интервала', message='введите границы корректно')
        return
    if n <= 0 or n > 10e4:
        messagebox.showerror(title='Неверно введено количество точек', message='введите количество точек корректно')
        return

    try:
        addPoints(n, a, b)
    except ZeroDivisionError:
        messagebox.showerror(title='Неверно введено количество точек', message='введите количество точек корректно')
        return

    array_of_points = getPoints()
    try:
        array_of_kvpoints = plot_polynomial(m, n, matrica_Gramma(array_of_points, m, n), array_of_points[:, 0])
    except (ArithmeticError, ValueError):
        messagebox.showerror(title='Переполнение типа данных', message='введите меньшие границы')
        return
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(array_of_points[:, 0], array_of_points[:, 1])
    ax1.plot(array_of_points[:, 0], array_of_kvpoints)
    plt.show()
    return


def btn2_click():
    try:
        m = int(loginOfm.get())
        if m < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(title='Некорректно введены данные', message='введите степень многочлена корректно')
        return

    try:
        array_of_points = getPoints()
        array_of_points = array_of_points[array_of_points[:, 0].argsort()]
        n = len(array_of_points[:,0])
        for i in range(n-1):
            if array_of_points[i][0] == array_of_points[i+1][0]:
                raise IndexError
        if n < m:
            raise ValueError
    except ValueError:
        messagebox.showerror(title='Некорректно введены данные', message='введите данные корректно')
        return
    except IndexError:
        messagebox.showerror(title='Некорректно введены точки', message='введите точки корректно')
        return

    try:
        array_of_kvpoints = plot_polynomial(m, n, matrica_Gramma(array_of_points, m, n), array_of_points[:, 0])
    except (ArithmeticError, ValueError):
        messagebox.showerror(title='Переполнение типа данных', message='введите меньшие границы')
        return
    except ValueError:
        messagebox.showerror(title='Некорректно введены данные', message='введите данные корректно1')
        return

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(array_of_points[:, 0], array_of_points[:, 1])
    ax1.plot(array_of_points[:, 0], array_of_kvpoints)
    plt.show()
    return


root = Tk()

root.title('laba4')
root.geometry('400x400')

frame = Frame(root, bg='grey')
frame.place(relheight=1, relwidth=1)
title = Label(frame, text='Левая граница промежутка,a=', bg='gray', width=200)
loginOfa = Entry(frame, bg='white', )
title2 = Label(frame, text='Правая граница промежутка,b=', bg='gray')
loginOfb = Entry(frame, bg='white', )
title3 = Label(frame, text="количество точек, n=", bg='gray')
loginOfn = Entry(frame, bg='white', )
title4 = Label(frame, text="Степень многочлена, m=", bg='gray')

loginOfm = Entry(frame, bg='white', )
title.pack()
loginOfa.pack()
title2.pack()
loginOfb.pack()
title3.pack()
loginOfn.pack()
title4.pack()
loginOfm.pack()
bnt = Button(frame, text='Построить график', bg='gray', command=bnt_click)
bnt2 = Button(frame, text='Построить график по точкам', bg='gray', command=btn2_click)

bnt.pack()
bnt2.pack()

root.mainloop()
