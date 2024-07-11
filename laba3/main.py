from tkinter import messagebox
import math
import matplotlib.pyplot as plt
from tkinter import *

lezhandr = {
    '2': [[-0.5773503, 0.5773503], [1, 1]],
    '3': [[-0.7745967, 0, 0.7745967], [0.5555556, 0.8888889, 0.5555556]],
    '4': [[-0.8611363, -0.3399810, 0.3399810, 0.8611363], [0.3478548, 0.6521451, 0.6521451, 0.3478548]],
}

A = 0


def fun(x):
    try:
        res = math.log(x) * math.sin(x) + x * x * math.cos(x)
    except ArithmeticError:
        return ValueError
    return res


def addPoints(n, a, b):
    f = open('laba3.txt', 'w')
    len = b - a
    for i in range(n):
        x = a + (len / n) * i
        f.write(str(x) + " " + str(fun(x)) + "\n")
    f.close()


def getPoints():
    q = open('laba3.txt', 'r')
    n = 0
    arrayOfPoints = []
    try:
        for i in q:
            arrayOfPoints.append((i.split()))
            arrayOfPoints[n][0] = float(arrayOfPoints[n][0])
            arrayOfPoints[n][1] = float(arrayOfPoints[n][1])
            n += 1
    except IndexError:
        raise ValueError
    q.close()
    return arrayOfPoints


def baza(xv, i):
    def rest(x):
        l1 = 1
        l2 = 1
        for j in range(len(xv)):
            if j != i:
                l1 *= (x - xv[j])
                l2 *= (xv[i] - xv[j])
        if (l2 == 0):
            raise ZeroDivisionError
        return l1 / l2

    return rest


def lezhan(xv, yv):
    arr = []
    m = len(xv)
    for i in range(len(xv)):
        arr.append(baza(xv, i))

    def poly(x):
        sum = 0
        for i in range(m):
            sum += yv[i] * arr[i](x)
        return sum

    return poly


# def find_integral(a, b, m):
#     point1 = a
#     point2 = a
#     Integral = 0
#     while point1 <= b:
#         if fun(point2) >= 0:
#             while fun(point2) >= 0 and point2 <= b:
#                 point2 += 0.01
#             Integral += gauss(point1, point2, m)
#             point1 = point2
#         else:
#             while fun(point2) < 0 and point2 <= b:
#                 point2 += 0.01
#             Integral += gauss(point1, point2, m)
#             point1 = point2
#     return Integral

def find_integral1(a, b, m, k, q):
    point1 = a
    point2 = a
    Integral = 0
    if a < 1:
        while point1 <= b:
            if k * point2 + q >= 0:
                while k * point2 + q >= 0 and point2 <= b:
                    point2 += 0.00000001
                Integral += gauss1(point1, point2, m, k, q)
                point1 = point2
            else:
                while k * point2 + q < 0 and point2 <= b:
                    point2 += 0.00000001
                Integral += gauss1(point1, point2, m, k, q)
                point1 = point2
        return Integral
    else:
        while point1 <= b:
            if k * point2 + q >= 0:
                while k * point2 + q >= 0 and point2 <= b:
                    point2 += 0.01
                Integral += gauss1(point1, point2, m, k, q)
                point1 = point2
            else:
                while k * point2 + q < 0 and point2 <= b:
                    point2 += 0.01
                Integral += gauss1(point1, point2, m, k, q)
                point1 = point2
    return Integral


# def gauss(a, b, m):
#     sum = 0
#     try:
#         arr = lezhandr[str(m)]
#     except KeyError:
#         raise KeyError
#     for i in range(m):
#         rar = (b + a) / 2.0 + ((b - a) / 2.0) * arr[0][i]
#         sum += arr[1][i] * fun(rar)
#     integral = ((b - a) / 2.0) * sum
#     return (integral)

def gauss1(a, b, m, k, q):
    sum = 0
    try:
        arr = lezhandr[str(m)]
    except KeyError:
        raise KeyError
    for i in range(m):
        rar = (b + a) / 2.0 + ((b - a) / 2.0) * arr[0][i]
        sum += arr[1][i] * (k * rar + q)
    integral = ((b - a) / 2.0) * sum
    return (integral)


def bttn1_click():
    try:
        b = float(inpb.get())
        a = float(inpa.get())
        n = int(inpn.get())
        m = int(inpm.get())
    except ValueError:
        messagebox.showerror(title='Ошибка', message='данные могут принимать только численное значение')
        return

    if b - a <= 0:
        messagebox.showerror(title='что-то грустно(((', message='неправильно введены границы интервала')
        return

    if n <= 1:
        messagebox.showerror(title='что-то грустно(((',
                             message='количество точек не может быть меньше или равно единице')
        return

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    try:
        addPoints(n, a, b)
        xv = [getPoints()[i][0] for i in range(len(getPoints()))]
        yv = [getPoints()[i][1] for i in range(len(getPoints()))]
        global A
        for i in range(1, len(xv)):
            k = (yv[i] - yv[i - 1]) / (xv[i] - xv[i - 1])
            q = yv[i] - k * xv[i]
            A += find_integral1(xv[i - 1], xv[i], m, k, q)

    except KeyError:
        messagebox.showerror(title='что-то грустно(((', message='количество узлов может принимать значения от 2 до 4')
        return

    except (ValueError, TypeError):
        messagebox.showerror(title='что-то грустно(((', message='неправильно введены границы интервала')
        return
    yl = []
    lezh = lezhan(xv, yv)
    for i in xv:
        yl.append(lezh(i))
    ax1.plot(xv, yl)
    plt.title(f'I={A}')
    plt.show()
    A = 0
    return


def bttn2_click():
    try:
        m = int(inpm.get())
    except ValueError:
        messagebox.showerror(title='Ошибка', message='данные могут принимать только численное значение')
        return

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    try:
        mylist = getPoints()
        mylist.sort(key=lambda x: x[0])
        xv = [mylist[i][0] for i in range(len(mylist))]
        yv = [mylist[i][1] for i in range(len(mylist))]
        global A
        for i in range(1, len(xv)):
            k = (yv[i] - yv[i - 1]) / (xv[i] - xv[i - 1])
            q = yv[i] - k * xv[i]
            A += find_integral1(xv[i - 1], xv[i], m, k, q)

    except KeyError:
        messagebox.showerror(title='что-то грустно(((', message='количество узлов может принимать значения от 2 до 4')
        return

    except (ValueError, TypeError, ZeroDivisionError):
        messagebox.showerror(title='что-то грустно(((', message='количество точек не может быть равно или меньше нуля')
        return
    yl = []
    lezh = lezhan(xv, yv)
    for i in xv:
        yl.append(lezh(i))
    ax1.plot(xv, yl)
    plt.title(f'I={A}')
    plt.show()
    A = 0

    return


window = Tk()
window.title('laba 3')
window.geometry('300x300')

frame = Frame(window, bg='grey')
frame.place(relheight=1, relwidth=1)
title = Label(frame, text='\ny(x) = ln(x)*Sin(x) + x*x*Cos(x)', bg='gray')
title1 = Label(frame, text='Левая граница интервала', bg='gray')
inpa = Entry(frame, bg='white', )
title2 = Label(frame, text='Правая граница интервала', bg='gray')
inpb = Entry(frame, bg='white', )
title3 = Label(frame, text="Количество точек", bg='gray')
inpn = Entry(frame, bg='white', )
title4 = Label(frame, text="Количество узлов", bg='gray')
inpm = Entry(frame, bg='white', )

title.pack()
title1.pack()
inpa.pack()
title2.pack()
inpb.pack()
title3.pack()
inpn.pack()
title4.pack()
inpm.pack()
bttn1 = Button(frame, text='Построить график', bg='gray', command=bttn1_click)
bttn2 = Button(frame, text='Построить график по точкам', bg='gray', command=bttn2_click)

bttn1.pack()
bttn2.pack()

window.mainloop()
