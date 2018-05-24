import tkinter as Tkinter
import time
import statistics
import random
from decimal import *
from tkinter import messagebox
from pump import Pump
from scale import Scale
from tzones import Zone
import sqlite3
from sqlalchemy import *
from datetime import datetime,tzinfo,timedelta

class App:
    def __init__(self, master):
        frame = Tkinter.Frame(master)

        self.target_coords = {"x":1,"y":1}

        self.tableReadData = []
        self.b = list()

        self.number_dispenses = Tkinter.StringVar()
        self.number_dispenses.set("10")

        self.dispenses = Tkinter.StringVar()
        self.dispenses.set("1,10,50,100")

        self.table_values = Tkinter.LabelFrame(frame, text="Values", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
        self.table_values.grid(row=0, column=3, padx=20, pady=20)

        self.createTable(self.number_dispenses.get(), self.dispenses.get())

        self.backlash_value = Tkinter.StringVar()
        self.backlash_value.set("0")

        self.piston = 0
        self.scale = 0

        self.controlObject = {}
        self.controlObject["rowStatus"] = 0
        self.controlObject["homeAspirate"] = 0
        self.controlObject["homeAspirateDispense"] = 0
        self.controlObject["runRow"] = 0

        frame.grid(row=0, column=0, padx=20, pady=20)

###############################################################################
####### GUI Based Functions ###################################################
    def callback(self, event, arg):
        y = arg['row']
        x = arg['col']
        self.getTarget(x, y)

    def createTable(self, xdata, ydata):
        dispenseArray = [dispense.strip() for dispense in ydata.split(',')]
        dispenseArray.insert(0, 'Dispense %')
        value_height = int(len(dispenseArray))
        value_width = int(xdata) + 1
        num_array = [num for num in range(1,int(xdata)+1)]
        for y in range(value_height):
            self.b.append(list())
            for x in range(int(xdata)+1):
                self.b[y].append(Tkinter.Entry(self.table_values, text="", width=10))
                self.b[y][x].grid(row=y, column=x)
                #self.b[y][x].insert(0, str(round(random.random()*100)))
                data = { "row": y, "col": x }
                self.b[y][x].bind("<Button-1>", lambda event, arg=data: self.callback(event, arg))
        for y in range(value_height):
            self.b[y][0].delete(0, 'end')
            self.b[y][0].insert(0, dispenseArray[y])
        for x in range(1, len(num_array) + 1):
            self.b[0][x].delete(0, 'end')
            self.b[0][x].insert(0, num_array[x-1])

    def addNotificationFields():

    """
    def populate(self):
        self.backlash_value.set("0.0150")
        for i in range(1,5):
            for j in range(1,11):
                self.b[i][j].insert(0, float(i*random.randint(1,5)))
    """


if __name__ == "__main__":
    root = Tkinter.Tk()
    app = App(root)
    root.mainloop()
