from tkinter import *
from tkinter import messagebox
import numpy as np
from matplotlib import pyplot as plt

def check():
    try:
        tmp = float(a_tf.get())
        tmp = float(b_tf.get())
        tmp = float(interval_tf.get())
    except:
        messagebox.showerror('что-то грустно(((', 'ошибка формата')
def solve_eq():
    check()
    a = float(a_tf.get())
    b = float(b_tf.get())
    xmax = float(interval_tf.get())
    c1 = 4 * a + b - 9 / 25.0
    c2 = -3 * a - b + 76 / 289.0
    xmin = 0
    i = xmin
    y_array = []
    x_array = []

    if xmax <= xmin:
        messagebox.showerror('что-то грустно(((', f'xmax не может быть меньшим или равным x')
    else:
        while i < xmax:
            y = (11 * i * np.sin(i)) / 170 + (189 * np.sin(i)) / 14450 - (7 * i * np.cos(i)) / 170 + (
                    701 * np.cos(i)) / 7225 + c1 * np.exp(-3 * i) + c2 * np.exp(-4 * i)
            x_array.append(i)
            y_array.append(y)
            i += 0.1

        fig = plt.figure()
        fig.set_figwidth(9)
        plt.plot(x_array, y_array)
        plt.title(f'График решения дифференциального уравнения при С1={c1},C2={c2}')
        plt.show()



window = Tk()
window.title('Решение дифференциального уравнения')

frame = Frame(
    window,
)
frame.pack(expand=True)

diffeq_lb = Label(
    frame,
    text="Дифференциальное уравнение: "
)

diffeq_lb.grid(row=1, column=1)

diffeq1_lb = Label(
    frame,
    text="y''+7y'+12y=xSin(x)+Cos(x)"
)

diffeq1_lb.grid(row=1, column=2)

param_lb = Label(
    frame,
    text="Параметры: "
)

param_lb.grid(row=2, column=1)

a_lb = Label(
    frame,
    text="y(0)=  "
)
a_lb.grid(row=3, column=1)

b_lb = Label(
    frame,
    text="y'(0)=  ",
)
b_lb.grid(row=4, column=1)

a_tf = Entry(
    frame,
)
a_tf.grid(row=3, column=2)

b_tf = Entry(
    frame,
)
b_tf.grid(row=4, column=2)

interval_lb = Label(
    frame,
    text='Правая граница интервала',
)
interval_lb.grid(row=5, column=1)

interval_tf = Entry(
    frame,
)
interval_tf.grid(row=5, column=2)

cal_btn = Button(
    frame,
    text='Решить уравнение',
    command=solve_eq
)
cal_btn.grid(row=6, column=2)

window.mainloop()
