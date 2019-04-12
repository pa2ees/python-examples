import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi, fromiter, log10, reshape, array
from pylab import psd, xlim, gca
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from subprocess import call, check_output
import matplotlib.pyplot as plt

import Tkinter as Tk
import sys
import csv
import os

class PlotClass:
    def __init__(self, root, plotData):
        self.fig = Figure(figsize=(16, 8), dpi=100)
        self.figsub1 = self.fig.add_subplot(221)
        self.figsub2 = self.fig.add_subplot(212)
        self.figsub3 = self.fig.add_subplot(222)
        #self.figsub2.set_yscale('log')
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.data1 = plotData
        #self.data1.plotData(self.figsub)
        self.canvas.show()
        
    def getCanvas(self):
        return self.canvas

    def update(self):
        #self.data1.updateData()
        self.data1.plotData(self.figsub1, self.figsub2, self.figsub3)
        self.canvas.show()

    def clearGraph(self):
        self.figsub1.cla()
        self.figsub2.cla()
        self.figsub3.cla()
        self.canvas.show()

class PlotData:
    def __init__(self):
        #self.data_array
        #self.rangenum = 3.0
        #self.t = arange(0.0, self.rangenum, 0.01)
        #self.s = sin(2*pi*self.t)
        pass

    def plotData(self, figsub1, figsub2, figsub3):
        #a.plot(self.t, self.s)
        figsub1.plot(self.adc_int_values)
        figsub1.grid(1)
        print len(self.data_psd[0])
        #self.data_test = [self.data_psd[0][512:578], self.data_psd[1][512:578]]
        figsub2.plot(self.data_psd[1]/1000000.0, 10*log10(self.data_psd[0]))
        figsub2.grid(1)
        for i in arange(12):
            figsub3.plot(self.adc_raw_values[i])

    
    def importData(self, filename):
        self.filename = filename
        ifile = open(filename, "r")
        reader = csv.reader(ifile)
        for row in reader:
            if len(row) > 1:
                if row[1].lstrip() == "XXX":
                    break
                
        #self.data_array = fromiter((int(row[1].lstrip(), 16) for row in reader), int)
        self.raw_data = [[int(num.lstrip(),16) for num in row if num != ' '] for row in reader]

        self.adc_int_values = [row[1] for row in self.raw_data]
        
        self.adc_raw_values = [row[2:] for row in self.raw_data]
        self.adc_raw_values = reshape(array(self.adc_raw_values), array(self.adc_raw_values).size, order='F').reshape(12,-1)
        
        for i in arange(12):
            for j in arange(len(self.adc_raw_values[0])):
                self.adc_raw_values[i][j] = self.adc_raw_values[i][j] + 2*i


        for i in range(len(self.adc_int_values)):
            if self.adc_int_values[i] >= 2048:
                self.adc_int_values[i] = self.adc_int_values[i] - 4096

        self.data_psd = psd(self.adc_int_values, 2048, 50000000, label=self.filename)
        #print len(self.data_psd)
        #print self.data_psd[1]


class GuiClass:
    def __init__(self):
        self.root = Tk.Tk()
        self.xyz = Tk.StringVar()
        self.root.protocol('WM_DELETE_WINDOW', self._quit)
        self.root.geometry("+%s+%s" % (100, 50))
        #print self.root.resizable()
        self.ButtonGrid = Tk.Frame(self.root)
        self.ButtonGrid.pack(padx=20, anchor="w")#grid(row=0, column=0, columnspan=1, padx=5, pady=5)
        self.PlotGrid = Tk.Frame(self.root)
        self.PlotGrid.pack()
        #self.quitButton = Tk.Button(self.ButtonGrid, text='Quit', command=self._quit)
        #self.quitButton.grid(in_=self.ButtonGrid, row=0, column=0, padx=5, pady=2, sticky="ew")
        self.updateButton = Tk.Button(self.ButtonGrid, text='Update From Enterprise Board', command=self.updateFromEntBoard)
        self.updateButton.grid(in_=self.ButtonGrid, row=1, column=0, padx=5, pady=2, sticky="ew")
        self.updateButton2 = Tk.Button(self.ButtonGrid, text='Update From File', command=self.updateFromFile)
        self.updateButton2.grid(row=0, column=0, padx=5, pady=2, sticky="ew")
        self.clearButton = Tk.Button(self.ButtonGrid, text='Clear', command=self.clearGraph)
        self.clearButton.grid(in_=self.ButtonGrid, row=2, column=0, padx=5, pady=2, sticky="ew")
        self.programButton = Tk.Button(self.ButtonGrid, text='Program', command=self.programChip)
        self.programButton.grid(in_=self.ButtonGrid, row=1, column=2, padx=5, pady=2)
        self.radioButton = Tk.Radiobutton(self.ButtonGrid, text="X", variable=self.xyz, value='x')
        self.radioButton.grid(in_=self.ButtonGrid, row=0, column=1, padx=15, pady=2)
        self.radioButton.select()
        self.radioButton = Tk.Radiobutton(self.ButtonGrid, text="Y", variable=self.xyz, value='y')
        self.radioButton.grid(in_=self.ButtonGrid, row=1, column=1, padx=15, pady=2)
        self.radioButton = Tk.Radiobutton(self.ButtonGrid, text="Z", variable=self.xyz, value='z')
        self.radioButton.grid(in_=self.ButtonGrid, row=2, column=1, padx=15, pady=2)
        self.workingLabel = Tk.Label(self.ButtonGrid, text="State: Idle", background="Green")
        self.workingLabel.grid(in_=self.ButtonGrid, row=1, column=3, padx=15, pady=2)
        self.plotData = PlotData()
        self.plot1 = PlotClass(self.PlotGrid, self.plotData)
        self.plot1.getCanvas().get_tk_widget().pack()#grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def _quit(self):
        self.root.quit()
        self.root.destroy()

    def updateFromEntBoard(self):
        self.updateState("State: Capturing Data", "Red")
        call(("C:/Altera/11.0/qprogrammer/bin/quartus_stp -t \"D:/Google Drive/pythonscripts/tmp/testscript_%s.tcl\"" % str(self.xyz.get())))
        self.updateState("State: Importing Data", "Red")
        self.plotData.importData('D:/Google Drive/data2/barf.csv')
        self.updateState("State: Plotting Data", "Red")
        self.clearGraph()
        self.plot1.update()
        self.root.update()
        self.updateState("State: Idle", "Green")


    def updateState(self, text, background):
        self.workingLabel.config(text=text, background=background)
        self.root.update()

    def programChip(self):
        self.updateState("State: Programming", "Red")
        call(("C:/Altera/11.0/qprogrammer/bin/quartus_pgm -c \"USB-Blaster [USB-0]\" --mode=JTAG -o p;\"D:/Altera Projects/Enterprise/adc_%s/trx.sof\"" % str(self.xyz.get())))
        self.updateState("State: Idle", "Green")

    def updateFromFile(self):
        self.updateState("State: Importing Data", "Red")
        self.plotData.importData('D:/Google Drive/data2/barf.csv')
        self.updateState("State: Plotting Data", "Red")
        self.clearGraph()
        self.plot1.update()
        self.root.update()
        self.updateState("State: Idle", "Green")


    def clearGraph(self):
        self.plot1.clearGraph()
        self.root.update()

mainwin = GuiClass()

Tk.mainloop()
