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
import requests

class App:
    def __init__(self, master):
        self.go = 2
        self.state = 1
        self.nonsequential = 0
        self.sequential = 0

        self.db = create_engine('sqlite:///pump.db')
        self.db.echo = False

        self.metadata = MetaData(self.db)

        self.pumps = Table('pumps', self.metadata,
            Column('board', String),
            Column('operator', String),
            Column('date', REAL),#how
            Column('serial_number', Integer),
            Column('pump_description', String),
            Column('customer', String),
            Column('purchase_order', String),
            Column('velocity', Integer),
            Column('acceleration', Integer),
            Column('type', String),
            Column('size', Integer),
            Column('piston', String),
            Column('head', String),
            Column('seal', String),
            Column('port_size', Integer),
            Column('prime_port', Integer),
            Column('tpi', Integer),
            Column('home_position', Integer),
            Column('valve', Integer),
            Column('sequential', Boolean),
            Column('dispense_percent', REAL),
            Column('dispense_1', REAL),
            Column('dispense_2', REAL),
            Column('dispense_3', REAL),
            Column('dispense_4', REAL),
            Column('dispense_5', REAL),
            Column('dispense_6', REAL),
            Column('dispense_7', REAL),
            Column('dispense_8', REAL),
            Column('dispense_9', REAL),
            Column('dispense_10', REAL),
            Column('backlash_value', REAL),
            Column('average', REAL),
            Column('stdev', REAL),
            Column('cv', REAL),
            Column('target', REAL),
            Column('variation', REAL),
            Column('test_description', Text)
        )

        frame = Tkinter.Frame(master)

        self.communication_options = Tkinter.LabelFrame(frame, text="Communication Options", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
        self.communication_options.grid(row=0, column=0, padx=20, pady=20, rowspan=2)

        self.scale_com_label = Tkinter.Label(self.communication_options, text="Scale COM Port")
        self.scale_com_label.grid(row=0, column=0, padx=5, pady=5)

        self.scale_com = Tkinter.StringVar()
        self.scale_com.set("COM7")
        self.scale_port = Tkinter.Entry(self.communication_options, textvariable=self.scale_com)
        self.scale_port.grid(row=1,column=0, padx=5, pady=5)

        self.scale_connect = Tkinter.Button(self.communication_options, text="Scale Connect", bd=10, height=1, width=10, command=self.createScalePort)
        self.scale_connect.grid(row=2, column=0, padx=5, pady=5)

        self.piston_com_label = Tkinter.Label(self.communication_options, text="Pump COM Port")
        self.piston_com_label.grid(row=3, column=0, padx=5, pady=5)

        self.piston_com = Tkinter.StringVar()
        self.piston_com.set("COM12")
        self.piston_port = Tkinter.Entry(self.communication_options, textvariable=self.piston_com)
        self.piston_port.grid(row=4,column=0, padx=5, pady=5)

        self.piston_address_label = Tkinter.Label(self.communication_options, text="Pump Address")
        self.piston_address_label.grid(row=5, column=0, padx=5, pady=5)

        self.piston_address = Tkinter.StringVar()
        self.piston_address.set("1")
        self.piston_address = Tkinter.Entry(self.communication_options, textvariable=self.piston_address)
        self.piston_address.grid(row=6,column=0, padx=5, pady=5)

        self.piston_connect = Tkinter.Button(self.communication_options, text="Piston Connect", bd=10, height=1, width=10, command=self.createPistonPort)
        self.piston_connect.grid(row=7, column=0, padx=5, pady=5)

        self.operator_label = Tkinter.Label(self.communication_options, text="Operator")
        self.operator_label.grid(row=8, column=0, padx=5, pady=5)

        self.operator_name = Tkinter.StringVar()
        self.operator_name.set("Jim Beahm")
        self.operator_entry = Tkinter.Entry(self.communication_options, textvariable=self.operator_name)
        self.operator_entry.grid(row=9,column=0, padx=5, pady=5)

        self.sn_label = Tkinter.Label(self.communication_options, text="Serial #")
        self.sn_label.grid(row=10, column=0, padx=5, pady=5)

        self.sn = Tkinter.StringVar()
        self.sn.set("Enter Serial Number")
        self.sn_entry = Tkinter.Entry(self.communication_options, textvariable=self.sn)
        self.sn_entry.grid(row=11,column=0, padx=5, pady=5)

        self.piston_desc_label = Tkinter.Label(self.communication_options, text="Piston Desc")
        self.piston_desc_label.grid(row=12, column=0, padx=5, pady=5)

        self.piston_desc = Tkinter.StringVar()
        self.piston_desc.set("MP5000CAV11200")
        self.piston_desc_entry = Tkinter.Entry(self.communication_options, textvariable=self.piston_desc)
        self.piston_desc_entry.grid(row=13,column=0, padx=5, pady=5)

        self.customer_label = Tkinter.Label(self.communication_options, text="Customer")
        self.customer_label.grid(row=14, column=0, padx=5, pady=5)

        self.customer = Tkinter.StringVar()
        self.customer.set("Enter Customer Name")
        self.customer_entry = Tkinter.Entry(self.communication_options, textvariable=self.customer)
        self.customer_entry.grid(row=15,column=0, padx=5, pady=5)

        self.purchase_label = Tkinter.Label(self.communication_options, text="Purchase Order")
        self.purchase_label.grid(row=16, column=0, padx=5, pady=5)

        self.purchase = Tkinter.StringVar()
        self.purchase.set("MP5000CAV11200")
        self.purchase_entry = Tkinter.Entry(self.communication_options, textvariable=self.purchase)
        self.purchase_entry.grid(row=17,column=0, padx=5, pady=5)

        self.save_data = Tkinter.Button(self.communication_options, text="Save", bd=10, height=1, width=10, command=self.saveFile)
        self.save_data.grid(row=18, column=0, padx=5, pady=5)

        self.piston_a = Tkinter.StringVar()
        self.piston_a.set("100000")


        self.piston_v = Tkinter.StringVar()
        self.piston_v.set("16000")

        self.piston_t = Tkinter.StringVar()
        self.piston_t.set("20")

        self.scale_weight = Tkinter.StringVar()
        self.scale_weight.set("Take A Reading")

#####################################################
        self.piston_test_options = Tkinter.LabelFrame(frame, text="Piston Setup", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
        self.piston_test_options.grid(row=1, column=1, padx=20, pady=20)

        self.prime = Tkinter.Button(self.piston_test_options, text="PRIME", bd=10, height=1, width=10, command=self.primePiston)
        self.prime.grid(row=4, column=0, padx=5, pady=5)

        self.stop = Tkinter.Button(self.piston_test_options, text="STOP", bd=10, height=1, width=10, command=self.stopPiston)
        self.stop.grid(row=5, column=0, padx=5, pady=5)

        self.run = Tkinter.Button(self.piston_test_options, text="RUN", bd=10, height=1, width=10, command=self.startAuto)
        self.run.grid(row=6, column=0, padx=5, pady=5)

        self.clear = Tkinter.Button(self.piston_test_options, text="CLEAR", bd=10, height=1, width=10, command=lambda: self.clearAll(self.table_values, int(self.number_dispenses.get())+1, self.dispenses.get()))
        self.clear.grid(row=7, column=0, padx=5, pady=5)

####################################################
        self.aspirate_options1 = Tkinter.LabelFrame(frame, text="Run Row", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
        self.aspirate_options1.grid(row=0, column=1, padx=20, pady=20)

        self.aspirate_11 = Tkinter.Button(self.aspirate_options1, text="1%", bd=10, height=1, width=10, command=lambda: self.doRow(1))
        self.aspirate_11.grid(row=0, column=0, padx=5, pady=5)

        self.aspirate_101 = Tkinter.Button(self.aspirate_options1, text="10%", bd=10, height=1, width=10, command=lambda: self.doRow(10))
        self.aspirate_101.grid(row=1, column=0, padx=5, pady=5)

        self.aspirate_501 = Tkinter.Button(self.aspirate_options1, text="50%", bd=10, height=1, width=10, command=lambda: self.doRow(50))
        self.aspirate_501.grid(row=2, column=0, padx=5, pady=5)

        self.aspirate_1001 = Tkinter.Button(self.aspirate_options1, text="100%", bd=10, height=1, width=10, command=lambda: self.doRow(100))
        self.aspirate_1001.grid(row=3, column=0, padx=5, pady=5)

#####################################################
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

        self.c = list()

        self.table_values2 = Tkinter.LabelFrame(frame, text="Stats", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
        self.table_values2.grid(row=1, column=3, padx=20, pady=20)

        self.createTable2()

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
####### Non Control Loop Commands##############################################
    def createScalePort(self):
        self.scale = Scale(self.scale_com.get().upper())

    def createPistonPort(self):
        self.piston = Pump(self.piston_com.get().upper())
        self.piston.setupPiston()

    def primePiston(self):
        self.piston.primePiston(int(self.piston_desc.get()[11])*10)

    def stopPiston(self):
        self.go = 10
        self.state = 0
        self.piston.stopPiston()
        self.test_state = 0

    def clearAll(self, frame, width, height):
        height = len([dispense.strip() for dispense in height.split(',')]) + 1
        tableData = list()
        for y in range(height):
            tableData.append(list())
            for x in range(width):
                tableData[y].append(self.b[y][x].get())
        self.tableReadData = tableData
        self.tableMaker1(tableData)

    def homeAspirateDispense(self):
        if self.controlObject["homeAspirateDispense"] == 1:
            self.piston.homePiston()
            self.controlObject["homeAspirateDispense"] = 2
            root.after(2500, self.homeAspirateDispense)
        elif self.controlObject["homeAspirateDispense"] == 2:
            self.piston.aspiratePiston(int(self.piston_desc.get()[11])*10)
            self.controlObject["homeAspirateDispense"] = 3
            root.after(2500, self.homeAspirateDispense)
        elif self.controlObject["homeAspirateDispense"] == 3:
            self.piston.dispensePercent(1, int(self.piston_desc.get()[11])*10)
            self.controlObject["runRow"] = 2
            root.after(2500, self.runRow)

    def homeAspirateDispenseAuto(self):
        if self.controlObject["homeAspirateDispenseAuto"] == 1:
            self.piston.homePiston()
            self.controlObject["homeAspirateDispenseAuto"] = 2
            root.after(2500, self.homeAspirateDispenseAuto)
        elif self.controlObject["homeAspirateDispenseAuto"] == 2:
            self.piston.aspiratePiston(int(self.piston_desc.get()[11])*10)
            self.controlObject["homeAspirateDispenseAuto"] = 3
            root.after(2500, self.homeAspirateDispenseAuto)
        elif self.controlObject["homeAspirateDispenseAuto"] == 3:
            self.piston.dispensePercent(1, int(self.piston_desc.get()[11])*10)
            self.go = 1
            root.after(1000, self.getData2)
###############################################################################
###### Database Related #######################################################
    def dbFunc(self):
        tableData = list()
        objData = list()
        stTime = time.time()
        for j in range(1, 5):
            tableData.append(list())
            for i in range(1,11):
                tableData[j-1].append(float(self.b[j][i].get()))
        for k in range(1, 5):
            objcontainer = {}
            objcontainer['board'] = 'all_motion'
            objcontainer['operator'] = self.operator_name.get()
            objcontainer['customer'] = self.customer.get()
            objcontainer['purchase_order'] = self.purchase.get()
            objcontainer['date'] = stTime
            objcontainer['serial_number'] = self.sn.get()
            objcontainer['pump_description'] = self.piston_desc.get()
            objcontainer['velocity'] = self.piston_v.get()
            objcontainer['acceleration'] = self.piston_a.get()
            objcontainer['type'] = self.piston_desc.get()[0:1]
            objcontainer['size'] = int(self.piston_desc.get()[2:6])
            objcontainer['piston'] = self.piston_desc.get()[6]
            objcontainer['head'] = self.piston_desc.get()[7]
            objcontainer['seal'] = self.piston_desc.get()[8]
            objcontainer['port_size'] = int(self.piston_desc.get()[9])
            objcontainer['prime_port'] = int(self.piston_desc.get()[10])
            objcontainer['tpi'] = self.piston_t.get()
            objcontainer['home_position'] = int(self.piston_desc.get()[12])
            objcontainer['valve'] = int(self.piston_desc.get()[13])
            objcontainer['sequential'] =  True if int(self.b[k][0].get()) <= 10 else False
            objcontainer['dispense_percent'] = int(self.b[k][0].get())
            for i in range(1,11):
                objcontainer['dispense_' + str(i)] = float(self.b[k][i].get())
            objcontainer['backlash_value'] = float(self.backlash_value.get())
            objcontainer['average'] = statistics.mean(tableData[k-1])
            objcontainer['stdev'] = statistics.pstdev(tableData[k-1])
            objcontainer['cv'] = statistics.pstdev(tableData[k-1])/statistics.mean(tableData[k-1])*100
            volume = int(self.b[j][0].get())/100 * int(self.piston_desc.get()[2:6])
            objcontainer['target'] = volume
            objcontainer['variation'] = statistics.mean(tableData[k-1])/volume
            objcontainer['test_description'] = 'Standard Customer'
            objData.append(objcontainer)
        i = self.pumps.insert()
        for p in objData:
            i.execute(p)
        r = requests.post('http://localhost:3001/piston_pumps', json = objData)

    def saveFile(self):
        result = messagebox.askyesno("Did you chceck to make sure that there are no zero's in the data")
        if result == True:
            self.dataReadout(self.table_values, int(self.number_dispenses.get())+1, self.dispenses.get())
            intTable = list()
            for i in range(1,len(self.tableReadData)):
                intTable.append(list())
                for j in range(1,len(self.tableReadData[0])):
                    if len(self.tableReadData[i][j]):
                        intTable[i-1].append(float(self.tableReadData[i][j]))
                    else:
                        intTable[i-1].append(0)
            dataTable = list()
            self.tableReadData[0].append('Average')
            self.tableReadData[0].append('Std Dev')
            self.tableReadData[0].append('COV')
            for z in range(0,len(intTable)):
                dataTable.append(list())
                dataTable[z].append(statistics.mean(intTable[z]))
                self.tableReadData[z+1].append(statistics.mean(intTable[z]))
                dataTable[z].append(statistics.pstdev(intTable[z]))
                self.tableReadData[z+1].append(statistics.pstdev(intTable[z]))
                dataTable[z].append(dataTable[z][1]/dataTable[z][0]*100)
                self.tableReadData[z+1].append(dataTable[z][1]/dataTable[z][0])
            dname = "M:\\piston_pump_testing\\practice"
            fname = self.sn.get()
            ftype = ".txt"
            full_path = dname + '\\' + fname + "_" + str(time.time()) + ftype
            F = open(full_path,"w+")
            F.write("Operator:" + "\t" + self.operator_name.get() + '\n')
            EST = Zone(-5,False,'EST')
            F.write("Date:" + "\t" + datetime.now(EST).strftime('%m/%d/%Y %H:%M:%S %Z') + '\n')
            F.write("Serial #:" + "\t" + self.sn.get() + '\n')
            F.write("Pump #:" + "\t" + self.piston_desc.get() + '\n')
            F.write("Accel:" + "\t" + self.piston_a.get() + '\n')
            F.write("Velocity:" + "\t" + self.piston_v.get() + '\n')
            F.write("Backlash Volume:" + "\t" + self.backlash_value.get() + '\n')
            for i in self.tableReadData:
                F.write('\n')
                for j in range(0,len(i)):
                    F.write(str(i[j]) + "\t")
            F.close()
            self.dbFunc()
            self.clearAll(self.table_values, int(self.number_dispenses.get())+1, self.dispenses.get())
            self.sn.set("####")

    def dataReadout(self, frame, width, height):
        height = len([dispense.strip() for dispense in height.split(',')]) + 1
        tableData = list()
        for y in range(height):
            tableData.append(list())
            for x in range(width):
                tableData[y].append(self.b[y][x].get())
        self.tableReadData = tableData
        self.tableMaker(tableData)

    def tableMaker(self, tableData):
        for y in range(len(tableData)):
            self.b.append(list())
            for x in range(len(tableData[0])):
                self.b[y].append(Tkinter.Entry(self.table_values, text="", width=5))
                self.b[y][x].grid(row=y, column=x)
                self.b[y][x].delete(0, 'end')
                self.b[y][x].insert(0, tableData[y][x])

    def tableMaker1(self, tableData):
        for y in range(len(tableData)):
            self.b.append(list())
            for x in range(len(tableData[0])):
                self.b[y].append(Tkinter.Entry(self.table_values, text="", width=5))
                self.b[y][x].grid(row=y, column=x)
                self.b[y][x].delete(0, 'end')
                if y == 0 or x == 0:
                    self.b[y][x].insert(0, tableData[y][x])
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
                data = { "row": y, "col": x }
                self.b[y][x].bind("<Button-1>", lambda event, arg=data: self.callback(event, arg))
        for y in range(value_height):
            self.b[y][0].delete(0, 'end')
            self.b[y][0].insert(0, dispenseArray[y])
        for x in range(1, len(num_array) + 1):
            self.b[0][x].delete(0, 'end')
            self.b[0][x].insert(0, num_array[x-1])

    def createTable2(self):
        dispenseData = ["Dispense %", "Average", "Standard Dev.", "CV", "Target", "Accuracy"]
        dispensePercents = ["1%", "10%", "50%", "100%"]
        for y in range(len(dispensePercents) + 1):
            self.c.append(list())
            for x in range(len(dispenseData)):
                self.c[y].append(Tkinter.Entry(self.table_values2, text="", width=20))
                self.c[y][x].grid(row=y, column=x)
        for x in range(len(dispenseData)):
            self.c[0][x].delete(0, 'end')
            self.c[0][x].insert(0, dispenseData[x])
        for y in range(len(dispensePercents)):
            self.c[y+1][0].delete(0, 'end')
            self.c[y+1][0].insert(0, dispensePercents[y])
        self.updateStats()

    def updateStats(self):
        tableData = []
        for y in range(len(self.b)-1):
            tableData.append(list())
            for x in range(len(self.b[0])-1):
                try:
                    tableData[y].append(float(self.b[y+1][x+1].get()))
                except:
                    tableData[y].append(0.0)

        for z in range(len(tableData)):
            y = z + 1
            self.c[y][1].delete(0, 'end')
            try:
                mean = float('%.5f'%(statistics.mean(tableData[z])))
            except:
                mean = 0.0
            self.c[y][1].insert(0, str(mean))
            self.c[y][2].delete(0, 'end')
            try:
                stdev = float('%.5f'%(statistics.pstdev(tableData[z])))
            except:
                stdev = 0.0
            self.c[y][2].insert(0, str(stdev))
            self.c[y][3].delete(0, 'end')
            try:
                cv = float('%.5f'%(stdev / mean * 100))
            except:
                cv = 0.0
            self.c[y][3].insert(0, str(cv))
            self.c[y][4].delete(0, 'end')
            try:
                target = int(self.b[y][0].get())/100 * int(self.piston_desc.get()[2:6])/1000
            except:
                target = 0.0
            self.c[y][4].insert(0, str(target))
            self.c[y][5].delete(0, 'end')
            try:
                variation = float('%.5f'%(mean/target * 100))
            except:
                variation = 0.0
            self.c[y][5].insert(0, str(variation))

###############################################################################
######## Row Control Loop Functions ###########################################
    def doRow(self, row):
        self.i = 0
        if row == 1:
            self.target_coords = {"x":1,"y":1}
            self.controlObject["homeAspirateDispense"] = 1
            self.homeAspirateDispense()
        elif row == 10:
            self.target_coords = {"x":1,"y":2}
            self.controlObject["homeAspirateDispense"] = 1
            self.homeAspirateDispense()
        elif row == 50:
            self.target_coords = {"x":1,"y":3}
            self.controlObject["homeAspirateDispense"] = 1
            self.homeAspirateDispense()
        elif row == 100:
            self.target_coords = {"x":1,"y":4}
            self.controlObject["homeAspirateDispense"] = 1
            self.homeAspirateDispense()
        else:
            pass

    def runRow(self):
        if self.controlObject["runRow"] == 0:
            self.scale.flushScale()
            self.scale.zeroScale()
            self.nonsequential = 0
            root.after(500, self.rowWaitForNonSequentialZero())
        elif self.controlObject["runRow"] == 1:
            self.scale.flushScale()
            self.scale.zeroScale()
            self.sequential = 0
            root.after(500, self.rowWaitForSequentialZero())
        elif self.controlObject["runRow"] == 2:
            self.i += 1
            if self.i > 10:
                self.controlObject["runRow"] = 7
                return self.runRow()
            else:
                self.chooseRowPath(self.target_coords["x"],self.target_coords["y"])
        elif self.controlObject["runRow"] == 3:
            self.rowMovePistonToNextPosition(self.target_coords['x'], self.target_coords['y'])
        elif self.controlObject["runRow"] == 5:
            self.scale.flushScale()
            self.rowWaitForAutoWeight()
        elif self.controlObject["runRow"] == 6:
            self.rowInsertAutoData(self.target_coords["x"],self.target_coords["y"])
        else:
            pass

    def rowWaitForNonSequentialZero(self):
        self.nonsequential += 1
        if self.nonsequential % 5 == 0:
            self.scale.zeroScale()
        x = self.scale.readLine()
        decoded = str(x.decode('utf-8').strip())
        if len(decoded) >= 3:
            if decoded[0] == 'Z' and decoded[2] == 'A':
                self.controlObject["runRow"] = 1
                self.runRow()
            else:
                root.after(500, self.rowWaitForNonSequentialZero)
        else:
            root.after(500, self.rowWaitForNonSequentialZero)

    def rowWaitForSequentialZero(self):
        self.sequential += 1
        if self.sequential % 5 == 0:
            self.scale.zeroScale()
        x = self.scale.readLine()
        decoded = str(x.decode('utf-8').strip())
        if len(decoded) >= 3:
            if decoded[0] == 'Z' and decoded[2] == 'A':
                self.controlObject["runRow"] = 3
                self.runRow()
            else:
                root.after(500, self.rowWaitForSequentialZero)
        else:
            root.after(500, self.rowWaitForSequentialZero)

    def chooseRowPath(self, x, y):
        height = len([dispense.strip() for dispense in self.dispenses.get().split(',')])
        if (int(self.b[y][0].get()) <= 10 and x == 1) and y != 1:
            self.piston.aspiratePiston(int(self.piston_desc.get()[11])*10)
            self.controlObject["runRow"] = 0
            root.after(1000, self.runRow)
        elif int(self.b[y][0].get()) <= 10 and x < int(self.number_dispenses.get()) + 2:
            self.controlObject["runRow"] = 1
            self.runRow()
        else:
            self.piston.aspiratePiston(int(self.piston_desc.get()[11])*10)
            self.controlObject["runRow"] = 0
            root.after(1000, self.runRow)

    def rowMovePistonToNextPosition(self, x, y):
        targetPos = self.b[y][0].get()
        self.piston.dispensePercent(int(targetPos), int(self.piston_desc.get()[11])*10)
        self.controlObject["runRow"] = 5
        root.after(1000,self.runRow)

    def rowWaitForAutoWeight(self):

        self.scale.readScale()
        x = self.scale.readLine()
        decoded = str(x.decode('utf-8').strip())
        if len(decoded) >= 3:
            if decoded[0] == 'S' and decoded[2] == 'S':
                weight = decoded[3:].strip().split(' ')
                if float(weight[0]) <= .00001:
                    root.after(500, self.rowWaitForAutoWeight)
                else:
                    self.b[self.target_coords["y"]][self.target_coords["x"]].delete(0, 'end')
                    self.b[self.target_coords["y"]][self.target_coords["x"]].insert(0, weight[0])
                    self.controlObject["runRow"] = 6
                    self.runRow()
            else:
                root.after(500, self.rowWaitForAutoWeight)
        else:
            root.after(500, self.rowWaitForAutoWeight)

    def rowInsertAutoData(self, x, y):
        self.rowNextAutoTarget(x, y)
        self.controlObject["runRow"] = 2
        self.runRow()

    def rowNextAutoTarget(self, x, y):
        height = len([dispense.strip() for dispense in self.dispenses.get().split(',')])
        if x >= int(self.number_dispenses.get()) and y < height:
            self.target_coords["x"] = 1
            self.target_coords["y"] = y + 1
            self.updateStats()
        elif x >= int(self.number_dispenses.get()) and y >= height:
            self.target_coords["x"] = 1
            self.target_coords["y"] = 1
            self.updateStats()
            self.controlObject["runRow"] = 7
            self.runRow()
        else:
            self.target_coords["x"] = x + 1
            self.target_coords["y"] = y
###############################################################################
######## Regular Control Loop Normal Functions ################################
    def homeAspirate(self):
        if self.controlObject["homeAspirate"] == 1:
            self.piston.homePiston()
            self.controlObject["homeAspirate"] = 2
            root.after(2500, self.homeAspirate)
        elif self.controlObject["homeAspirate"] == 2:
            self.piston.aspiratePiston(int(self.piston_desc.get()[11])*10)
            self.controlObject["homeAspirate"] = 3
            root.after(2500, self.homeAspirate)
        elif self.controlObject["homeAspirate"] == 3:
            root.after(2500, self.getBacklashValue(4))

    def startAuto(self):
        self.piston.setupPiston()
        self.controlObject["homeAspirate"] = 1
        self.target_coords = {"x":1,"y":1}
        desc_string = self.piston_desc.get()
        if len(desc_string) <= 13 or len(desc_string) >= 15:
            return messagebox.showerror("Error", "Check to make Sure that the piston description is properly written")
        else:
            pass
        try:
            threads = int(desc_string[11]) * 10
            if threads != 20 and threads != 40:
                return messagebox.showerror("Error", "Check to make Sure threads are 20 or 40")
            else:
                pass
        except:
            return messagebox.showerror("Error", "Make sure a number is entered in the threads field")
        try:
            volume = int(desc_string[2:6])
        except:
            return messagebox.showerror("Error", "Make sure a number is entered in the volume field")
        result = messagebox.askyesno("Final Check","{} {} {} {} {}".format("Are you sure you want to run a test for a pump with: \n", "Operator: " + self.operator_name.get() + "\n", "tpi: " + str(threads) + "\n", "volume: " + str(volume) + "\n", "Serial Number: " + self.sn.get()))
        if result == True:
            self.piston_t.set(str(threads))
            self.state = 1
            self.go = 2
            self.homeAspirate()
        else:
            pass

    def getBacklashValue(self, status):
        if status == 1:
            self.piston.dispensePercent(1, int(self.piston_desc.get()[11])*10)
            root.after(2000, self.getBacklashValue(2))
        elif status == 2:
            self.scale.flushScale()
            self.waitForBacklash()
        elif status == 3:
            self.getData2()
        elif status == 4:
            self.getBacklashZero()

    def waitForBacklash(self):
        self.scale.readScale()
        x = self.scale.readLine()
        decoded = str(x.decode('utf-8').strip())
        if len(decoded) >= 3:
            if decoded[0] == 'S' and decoded[2] == 'S':
                weight = decoded[3:].strip().split(' ')
                self.backlash_value.set(weight[0])
                if float(weight[0]) <= .00001:
                    root.after(1000, self.waitForBacklash)
                elif float(weight[0]) > .00001:
                    self.getBacklashValue(3)
            else:
                root.after(1000, self.waitForBacklash)
        elif len(decoded) < 3:
            root.after(1000, self.waitForBacklash)

    def getBacklashZero(self):
        self.scale.zeroScale()
        x = self.scale.readLine()
        decoded = str(x.decode('utf-8').strip())
        if len(decoded) >= 3:
            if decoded[0] == 'Z' and decoded[2] == 'A':
                root.after(2000, self.getBacklashValue(1))
            else:
                root.after(1000, self.getBacklashZero)
        elif len(decoded) < 3:
            root.after(1000, self.getBacklashZero)

    def getData2(self):
        if self.state == 1:
            if self.go == 0:
                self.scale.flushScale()
                self.waitForNonSequentialZero()
                self.scale.flushScale()
            elif self.go == 1:
                self.scale.flushScale()
                self.waitForSequentialZero()
                self.scale.flushScale()
            elif self.go == 2:
                self.choosePath(self.target_coords["x"],self.target_coords["y"])
            elif self.go == 3:
                self.movePistonToNextPosition(self.target_coords['x'], self.target_coords['y'])
            elif self.go == 5:
                self.scale.flushScale()
                self.waitForAutoWeight()
                self.scale.flushScale()
            elif self.go == 6:
                self.insertAutoData(self.target_coords["x"],self.target_coords["y"])
            elif self.go == 7:
                self.homeAspirateDispenseAuto()
            else:
                self.updateStats()
                pass

    def waitForNonSequentialZero(self):
        if self.go == 0:
            self.scale.zeroScale()
            x = self.scale.readLine()
            decoded = str(x.decode('utf-8').strip())
            if len(decoded) >= 3:
                if decoded[0] == 'Z' and decoded[2] == 'A':
                    self.go = 1
                    self.getData2()
                    return
                else:
                    root.after(500, self.waitForZero)
            else:
                root.after(500, self.waitForZero)
        else:
            pass

    def waitForZero(self):
        if self.go == 0:
            self.scale.zeroScale()
            x = self.scale.readLine()
            decoded = str(x.decode('utf-8').strip())
            if len(decoded) >= 3:
                if decoded[0] == 'Z' and decoded[2] == 'A':
                    self.go = 1
                    self.getData2()
                    return
                else:
                    root.after(500, self.waitForZero)
            else:
                root.after(500, self.waitForZero)
        if self.go == 4:
            self.scale.zeroScale()
            x = self.scale.readLine()
            decoded = str(x.decode('utf-8').strip())
            if len(decoded) >= 3:
                if decoded[0] == 'Z' and decoded[2] == 'A':
                    self.go = 5
                    self.movePistonToNextPosition()
                    return
                else:
                    root.after(500, self.waitForZero)
            else:
                root.after(500, self.waitForZero)
        else:
            pass

    def movePistonToNextPosition(self, x, y):
        if self.go == 3:
            targetPos = self.b[y][0].get()
            self.piston.dispensePercent(int(targetPos), int(self.piston_desc.get()[11])*10)
            self.go = 5
            root.after(2000,self.getData2)

    def waitForSequentialZero(self):
        if self.go == 1:
            self.scale.zeroScale()
            x = self.scale.readLine()
            decoded = str(x.decode('utf-8').strip())
            if len(decoded) >= 3:
                if decoded[0] == 'Z' and decoded[2] == 'A':
                    self.go = 3
                    self.getData2()
                    return
                else:
                    root.after(500, self.waitForSequentialZero)
            else:
                root.after(500, self.waitForSequentialZero)
        else:
            pass

    def choosePath(self, x, y):
        if self.go == 2:
            height = len([dispense.strip() for dispense in self.dispenses.get().split(',')])
            if (int(self.b[y][0].get()) == 1 and x == 1) and y != 1:
                self.piston.aspiratePiston(int(self.piston_desc.get()[11])*10)
                self.go = 1
                root.after(1000, self.getData2)
            elif (int(self.b[y][0].get()) <= 10 and x == 1) and y != 1 and int(self.b[y][0].get()) > 1:
                self.controlObject["homeAspirateDispenseAuto"] = 1
                self.homeAspirateDispenseAuto()
            elif int(self.b[y][0].get()) <= 10 and x < int(self.number_dispenses.get()) + 2:
                self.go = 1
                self.getData2()
            else:
                self.piston.aspiratePiston(int(self.piston_desc.get()[11])*10)
                self.go = 1
                root.after(1000, self.getData2)

    def waitForAutoWeight(self):
        if self.go == 5:
            self.scale.readScale()
            x = self.scale.readLine()
            decoded = str(x.decode('utf-8').strip())
            if len(decoded) >= 3:
                if decoded[0] == 'S' and decoded[2] == 'S':
                    weight = decoded[3:].strip().split(' ')
                    self.b[self.target_coords["y"]][self.target_coords["x"]].delete(0, 'end')
                    self.b[self.target_coords["y"]][self.target_coords["x"]].insert(0, weight[0])
                    self.go = 6
                    self.getData2()
                    return
                else:
                    root.after(500, self.waitForAutoWeight)
            else:
                root.after(500, self.waitForAutoWeight)
        else:
            pass

    def insertAutoData(self, x, y):
        if self.go == 6:
            self.nextAutoTarget(x, y)
            self.go = 2
            self.getData2()

    def nextAutoTarget(self, x, y):
        height = len([dispense.strip() for dispense in self.dispenses.get().split(',')])
        if x >= int(self.number_dispenses.get()) and y < height:
            self.updateStats()
            self.target_coords["x"] = 1
            self.target_coords["y"] = y + 1
            return
        elif x >= int(self.number_dispenses.get()) and y >= height:
            self.updateStats()
            self.target_coords["x"] = 1
            self.target_coords["y"] = 1
            self.state = 0
            self.getData2()
        else:
            self.target_coords["x"] = x + 1
            self.target_coords["y"] = y
            return

if __name__ == "__main__":
    root = Tkinter.Tk()
    app = App(root)
    root.mainloop()
