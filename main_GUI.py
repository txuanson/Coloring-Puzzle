from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import time
from main_algo import pySAT_coloring
from main_algo import BF_coloring
from main_algo import Backtracking_coloring


class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        master.title("Coloring Puzzle")
        master.minsize(640, 400)
        self.buttons(master)
        self.grid(row=0, column=0)

    def buttons(self, master):
        self.labelFrame = Label(
            master, text='Choose file', font=('Pursia', 11))
        self.labelFrame.place(x=40, y=20)
        self.path_file = StringVar(value='')
        self.label = Entry(master, textvariable=self.path_file,
                           width=45, font=('Pursia', 11))
        self.label.place(x=150, y=20)
        self.button = Button(
            master, text="Browse", command=self.fileDialog, font=('Pursia', 11))
        self.button.place(x=550, y=15)

        self.value_options = {'PySAT': '1', 'A Star': '2',
                              'Brute Force': '3', 'Backtracking': '4'}
        self.getAlgo = StringVar(master, '1')

        i = 1
        for (text, value) in self.value_options.items():
            Radiobutton(master, text=text, variable=self.getAlgo,
                        value=value).place(x=(100 * i) + 40, y=50)
            i += 1

        self.start_button = Button(
            master, text="Start", width=60, command=self.checkType, font=('Pursia', 11))
        self.start_button.place(x=40, y=110)

        self.running_time = StringVar(master, 0)
        self.timeFrame = Label(
            master, text='Time', font=('Pursia', 11))
        self.timeFrame.place(x=40, y=80)

        self.time = Entry(master, textvariable=self.running_time,
                          width=45, font=('Pursia', 11))
        self.time.place(x=150, y=80)

    def fileDialog(self):
        self.time.configure(textvariable=0)
        self.filename = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(('text files', 'txt'), ("all files", "*.*")))
        self.path_file.set(self.filename)
        self.label.configure(textvariable=self.path_file)
        openFile = open(self.filename, 'r')
        lines = openFile.readline().strip()
        lines = openFile.readlines()
        lines_int = [list(map(int, line.strip().split(' '))) for line in lines]
        self.boardInput = np.array(lines_int)

    def checkType(self):
        # print(self.getAlgo.get())
        if self.getAlgo.get() == '1':
            t0 = time.time()
            self.time.configure(textvariable='Running')
            self.result = pySAT_coloring(self.boardInput)
            t1 = time.time()
            self.running_time.set(t1 - t0)
            self.time.configure(textvariable=self.running_time)
            self.initialDraw()
        elif self.getAlgo.get() == '3':
            t0 = time.time()
            self.time.configure(textvariable='Running')
            self.result = BF_coloring(self.boardInput)
            t1 = time.time()
            self.running_time.set(t1 - t0)
            self.time.configure(textvariable=self.running_time)
            if self.result is not None:
                self.initialDraw()
        elif self.getAlgo.get() == '4':
            t0 = time.time()
            self.time.configure(textvariable='Running')
            self.result = Backtracking_coloring(self.boardInput)
            t1 = time.time()
            self.running_time.set(t1 - t0)
            self.time.configure(textvariable=self.running_time)
            if self.result is not None:
                self.initialDraw()

    def initialDraw(self):
        self.boardSize = 20 * 2 + 30 * len(self.boardInput)
        self.sqSize = self.boardSize / len(self.boardInput)

        mainframe = ttk.Frame(self, padding=(20, 150, 20, 20))
        mainframe.grid(column=0, row=0, sticky=(N, S, E, W))

        self.mainboard = Canvas(
            mainframe, width=self.boardSize - 1, height=self.boardSize - 1, bg='white')

        self.mainboard.grid(row=1, column=0)

        for row in range(len(self.boardInput)):
            for col in range(len(self.boardInput)):
                top = row * self.sqSize
                left = col * self.sqSize
                bottom = row * self.sqSize + self.sqSize
                right = col * self.sqSize + self.sqSize

                color = 'green'
                if self.result[row][col] == 0:
                    color = 'red'

                valueOnBoard = ''
                if self.boardInput[col][row] != -1:
                    valueOnBoard = self.boardInput[col][row]

                self.mainboard.create_text(
                    top + self.sqSize / 2, left + self.sqSize / 2, text=valueOnBoard, font=('Pursia', 11))

                rect = self.mainboard.create_rectangle(
                    left, top, right, bottom, outline='gray', fill=color)
                # print(self.boardInput[col][row], end=' ')
                self.mainboard.lower(rect)
            # print()

        self.mainboard.focus_set()


tk = Tk()
root = GUI(tk)
root.mainloop()
