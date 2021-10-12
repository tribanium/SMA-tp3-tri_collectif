import tkinter as tk
import time

fen = tk.Tk()  # ouvre une instance de fenêtre

h = 800
w = 800

can = tk.Canvas(fen, bg='white', height=h, width=w)

N = 50
M = 50

can.pack()

"""# Vertical lines
for index in range(0, M):
    can.create_line(index*w/M, 0, index*w/M, h, fill='black')

# Horizontal lines
for index in range(0, N):
    can.create_line(0, index*h/N, w, index*h/N, fill='black')


def color_cell(row_number, col_number):
    can.create_rectangle((row_number-1)*w/M, (col_number-1)
                         * h/N, row_number*w/M, col_number*h/N, fill="red")


def remove_color_cell(row_number, col_number):
    color = can.cget('bg')
    can.create_rectangle((row_number-1)*w/M, (col_number-1)
                         * h/N, row_number*w/M, col_number*h/N, fill=color)"""

grid = []

for row in range(N):
    row_list = []
    for col in range(M):
        rect = can.create_rectangle(col*w/M, row*h/N, (col+1)*w/M, (row+1)*h/N)
        row_list.append(rect)
    grid.append(row_list)

color_cell(3, 5)
fen.update()
time.sleep(4)
remove_color_cell(3, 5)
fen.update()
time.sleep(3)
