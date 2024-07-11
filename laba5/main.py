import math
from tkinter import messagebox

import numpy as np
import matplotlib.pyplot as plt
from tkinter import *



def fun_of_x(x, y):
    try:
        res = x-(54/(27*x-8*y-46))*(((x*x-2)/4)+((y*y-1)/9)-1)+((4*y-y)/(27*x-8*y-46))*(2*x+3*y-1)
    except (ArithmeticError, ValueError):
        raise ArithmeticError
    return(res)


def fun_of_y(x,y):
    try:
        res = y-(36/(2*x-8*y-62))*(((x*x-2)/4)+((y*y-1)/9)-1)+((18-9*x)/(2*x-8*y-62))*(2*x+3*y-1)
    except (ArithmeticError, ValueError):
        raise ArithmeticError
    return res

eps = 0.000001

def interations(x0,y0):
    x = x0
    y = y0
    x1 = fun_of_x(x, y)
    y1 = fun_of_y(x, y)
    count = 0
    while abs(x1-x) > eps or abs(y1-y) > eps:
        x = fun_of_x(x,y)
        y = fun_of_y(x, y)
        x1 = fun_of_x(x, y)
        y1 = fun_of_y(x, y)

        count +=1
    print(count)
    return (np.array([x1,y1]))


def delta(x0,y0):
    count = 0
    x = x0
    y = y0
    dx = 1
    dy = 1
    while abs(dx) > eps or abs(dy) > eps:
        matrix = np.array([[((x/2)-1), ((2*y/9)-(2/9))], [2, 3]])
        otvet = np.array([[-(((x-2)*(x-2))/4)-(((y-1)*(y-1))/9)+1], [-2*x -3*y + 1]])
        try:
            res = np.linalg.solve(matrix, otvet)
        except np.linalg.LinAlgError:
            raise ArithmeticError
        dx = res[0][0]
        dy = res[1][0]
        x += dx
        y += dy
        count += 1
    print(count)
    return np.array([x, y])


def plot_func():
    oval_points = np.linspace(0, 4, 100)
    res1 = np.zeros((100,))
    res2 = np.zeros((100,))
    for i in range(100):
        res1[i] = 1 + 3 * math.sqrt(1 - ((oval_points[i] - 2) / 2) ** 2)
        res2[i] = 1 - 3 * math.sqrt(1 - ((oval_points[i] - 2) / 2) ** 2)

    line_points = np.linspace(-2, 4, 100)
    rep = np.zeros((100,))
    for i in range(100):
        rep[i] = (1.0 - 2.0 * line_points[i])/3.0

    return [oval_points, res1, res2, line_points, rep]


def bnt_click():
    plt.style.use('seaborn-v0_8-whitegrid')
    try:
        x0 =float(loginOfx0.get())
        y0 = float(loginOfy0.get())
        if abs(x0) == abs(math.inf) or abs(y0) == abs(math.inf):
            raise ValueError
    except ValueError:
        messagebox.showerror(title='Ошибка типа данных', message='введите данные корректно')
        return

    if var.get() == 1:
        try:
            point = interations(x0,y0)
        except ArithmeticError:
            messagebox.showerror(title='Некорректное начальное приближение', message='попробуйте вести данные побольше')
            return
        except ValueError:
            messagebox.showerror(title='Некорректное начальное приближение', message='попробуйте вести данные поменьше')
            return
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.scatter(point[0], point[1], c='red')
        picture = plot_func()
        ax1.plot(picture[0], picture[1], c='black')
        ax1.plot(picture[0], picture[2], c='black')
        ax1.plot(picture[3], picture[4])
    else:
        try:
            point = delta(x0,y0)
        except ArithmeticError:
            messagebox.showerror(title='Некорректное начальное приближение', message='попробуйте вести другие данные')
            return
        except ValueError:
            messagebox.showerror(title='Некорректное начальное приближение', message='попробуйте вести другие данные')
            return
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        picture = plot_func()
        ax1.plot(picture[0], picture[1], c='black')
        ax1.plot(picture[0], picture[2], c='black')
        ax1.plot(picture[3], picture[4])
        ax1.scatter(point[0], point[1], c='red')
    plt.show()
    return


root = Tk()
root.title('Erofeev 5')
root.geometry('400x400')

frame = Frame(root, bg='grey')
frame.place(relheight=1, relwidth=1)
title = Label(frame, text='x0=', bg='gray', width=200)
loginOfx0 = Entry(frame, bg='white')
title2 = Label(frame, text='y0=', bg='gray')
loginOfy0 = Entry(frame, bg='white')


var = IntVar()
var.set(0)
newton = Radiobutton(text="Метод ньютона", variable=var, value=0, bg='gray')
iter = Radiobutton(text="Метод простых итераций", variable=var, value=1, bg='gray')


title.pack()
loginOfx0.pack()
title2.pack()
loginOfy0.pack()
newton.pack(side=BOTTOM)
iter.pack(side=BOTTOM)
bnt = Button(frame, text='Построить график', bg='gray', command=bnt_click)
# bnt2 = Button(frame, text='Построить график по точкам', bg='gray', command=btn2_click)

bnt.pack()
# bnt2.pack()

root.mainloop()
