from tkinter import messagebox
import numpy as np
import math
import matplotlib.pyplot as plt
from tkinter import *

rarr = {}

# Определяется функция fun(x), которая вычисляет значение функции в точке x
def fun(x):
    y = x * x + x * math.sin(x)
    if np.isnan(y):
        return ValueError
    else:
        return y


# Определяется функция addPoints(n, a, b), которая создает файл laba2.txt и записывает в него координаты точек:
def addPoints(n, a, b):
    f = open('laba2.txt', 'w')
    len = b - a
    for i in range(n + 1):
        x = a + (len / n) * i
        f.write(str(x) + " " + str(fun(x)) + "\n")
    f.close()


# Определяется функция getPoints(), которая читает файл laba2.txt и возвращает список координат точек:
def getPoints():
    q = open('laba2.txt', 'r')
    n = 0
    arrayOfPoints = []
    try:
        for i in q:
            arrayOfPoints.append((i.split()))

            rarr[(arrayOfPoints[n][0])] = (arrayOfPoints[n][1])
            arrayOfPoints[n][0] = float(arrayOfPoints[n][0])
            arrayOfPoints[n][1] = float(arrayOfPoints[n][1])
            n += 1
    except IndexError:
        raise ValueError

    q.close()
    return arrayOfPoints


# Определяется функция razd(xv,yv,k), которая вычисляет разделенную разность в точке k:
def razd(xv, yv, k):
    sum = 0
    for i in range(k + 1):
        pr = 1
        for j in range(k + 1):
            if (j != i):
                pr *= (xv[i] - xv[j])
        sum = sum + (yv[i]) / pr
    return (sum)


# Функция, которая возвращает интерполяционный многочлен Ньютона
def newton(xv, yv, m):
    rep = []
    for i in range(1, len(xv)):
        rep.append((razd(xv, yv, i)))

    def new1(x):
        result = yv[0]
        for k in range(1, m + 1):
            pr = 1
            for j in range(k):
                pr *= (x - xv[j])
            result += rep[k - 1] * pr
        return result

    return (new1)


def baza(xv, i):
    def rest(x):
        l1 = 1
        l2 = 1
        for j in range(len(xv)):
            if (j != i):
                l1 *= (x - xv[j])
                l2 *= (xv[i] - xv[j])
        if (l2 == 0):
            raise ZeroDivisionError
        return l1 / l2

    return rest


# Функция, которая возвращает интерполяционный многочлен Лагранжа
def lagranz(m, xv, yv):
    arr = []
    for i in range(len(xv)):
        arr.append(baza(xv, i))

    def poly(x):
        sum = 0
        for i in range(m + 1):
            sum += yv[i] * arr[i](x)
        return sum

    return poly


# Функция, которая вызывается при нажатии на кнопку bttn1
def bttn1():
    try:
        b = int(loginOfb.get())  # Правая граница
        a = int(loginOfa.get())  # Левая граница
        n = int(loginOfn.get())  # Количество точек
        m = int(loginOfm.get())  # Степень интерполяционного многочлена
    except ValueError:
        messagebox.showerror(title='что-то грустно(((', message='данные могут принимать только численное значение')
        return

    if b - a <= 0:
        messagebox.showerror(title='что-то грустно(((', message='неправильно введены границы интервала')
        return
    if n <= 1:
        messagebox.showerror(title='что-то грустно(((', message='количество точек не может быть равно или меньше нуля')
        return
    if m <= 0:
        messagebox.showerror(title='что-то грустно(((', message='неправильно введена степень многочлена')
        return
    if m > n:
        messagebox.showerror(title='что-то грустно(((',
                             message='степень многочлена не может превышать количество точек')
        return

    # Начиная со 115 строки, идут выводы ошибок

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    try:
        addPoints(n, a, b)
        xv = [getPoints()[i][0] for i in range(len(getPoints()))]
        yv = [getPoints()[i][1] for i in range(len(getPoints()))]
    except ValueError:
        messagebox.showerror(title='Некорректно ввел данные',
                             message='введите данные корректно')
        return
    yn = []
    yl = []
    x1 = []
    for i in range(1001):
        x1.append(a + (b - a) * i / 1000)
    if var.get() == 1:
        try:
            newpol = newton(xv, yv, m)
            for i in x1:
                yn.append(newpol(i))

            ax1.plot(x1, yn)
            ax1.plot(xv, yv)

            plt.show()
        except ValueError:
            messagebox.showerror(title='Некорректно ввел данные',
                                 message='введите данные корректно1')
            return

    else:

        lagr = lagranz(m, xv, yv)
        for i in x1:
            yl.append(lagr(i))
        ax1.plot(x1, yl)
        ax1.plot(xv, yv)
        plt.show()

    return


def bttn2():
    try:
        m = int(loginOfm.get())
        if m <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(title='что-то грустно(((', message='данные могут принимать только численное значение')
        return
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    try:
        mylist = getPoints()
        mylist.sort(key=lambda x: x[0])
        xv = [mylist[i][0] for i in range(len(mylist))]
        yv = [mylist[i][1] for i in range(len(mylist))]
        if len(xv) < m:
            raise ValueError
    except ValueError:
        messagebox.showerror(title='что-то грустно(((',
                             message='степень многочлена не может превышать количество точек')
        return
    yn = []
    yl = []
    if var.get() == 1:
        try:
            newpol = newton(xv, yv, m)
            for i in xv:
                yn.append(newpol(i))

            ax1.plot(xv, yn)
            ax1.plot(xv, yv)

            plt.show()
        except ValueError:
            messagebox.showerror(title='Некорректно введены данные',
                                 message='введите данные корректно1')
            return
        except ZeroDivisionError:
            messagebox.showerror(title='что-то грустно(((',
                                 message='количество точек не может быть равно или меньше нуля')

    else:
        try:
            lagr = lagranz(m, xv, yv)
            for i in xv:
                yl.append(lagr(i))
            ax1.plot(xv, yl)
            ax1.plot(xv, yv)
            plt.show()
        except ValueError:
            messagebox.showerror(title='Некорректно введены данные',
                                 message='введите данные корректно1')
        except ZeroDivisionError:
            messagebox.showerror(title='что-то грустно(((',
                                 message='неправильно введены границы интервала')
        except IndexError:
            messagebox.showerror(title='что-то грустно(((',
                                 message='степень многочлена не может превышать количество точек')

    return


# Создание оконного приложения
window = Tk()
window.title('laba 2')
window.geometry('300x300')
var = IntVar()

frame = Frame(window, bg='gray')
frame.place(relheight=1, relwidth=1)
title = Label(frame, text='Левая граница', bg='gray', width=200)
lagr = Radiobutton(text="Лагранж", variable=var, value=0, bg='gray')
new = Radiobutton(text=" Ньютон", variable=var, value=1, bg='gray')
loginOfa = Entry(frame, bg='white', )
title2 = Label(frame, text='Правая граница', bg='gray')
loginOfb = Entry(frame, bg='white', )
title3 = Label(frame, text="количество точек, n=", bg='gray')
loginOfn = Entry(frame, bg='white', )
title4 = Label(frame, text="Cтепень многочлена, m=", bg='gray')
loginOfm = Entry(frame, bg='white', )
title.pack()
loginOfa.pack()
title2.pack()
loginOfb.pack()
title3.pack()
loginOfn.pack()
title4.pack()
loginOfm.pack()
button1 = Button(frame, text='Построить график', bg='gray', command=bttn1)
button2 = Button(frame, text='Построить график по заданным точкам', bg='gray',
                 command=bttn2)
button1.pack()
button2.pack()
lagr.pack(after=button2, side=LEFT)
new.pack(after=button2, side=LEFT)

window.mainloop()
