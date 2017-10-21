import sys
import time

import tkinter as tk
import tkinter.ttk as ttk

from tkinter import scrolledtext
from tkinter import filedialog

from .status import Status, StatusFrame
from .gridframe import GridFrame
from .primary import Primary

font1Size = 32
font2Size = 16
font1 = ('Helvetica', str(font1Size)) 
font2 = ('Helvetica', str(font2Size))

style = dict(background='black', 
             foreground='white',  
             font=font2)

class MainApplication(GridFrame):

    def __init__(self, parent, *args, **kwargs):
        GridFrame.__init__(self, parent, *args, **kwargs)
        self.widgets = dict()

        self.parent = parent
        self.primary = Primary(self, *args, **kwargs)
        self.add(self.primary, 0, 0)
        self.create_widgets()

    def create_widgets(self):

        tempLabel = ttk.Label(self, text='', **style, padding=30)
        #tempLabel.grid(column=1, row=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.widgets['temp'] = tempLabel

        slipList = tk.Listbox(self, **style)
        self.add(slipList, 0, 1)
        self.widgets['sliplist'] = slipList

        codeletList = tk.Listbox(self, **style)
        self.add(codeletList, 1, 1)
        self.widgets['codeletlist'] = codeletList

        l = ttk.Label(self, text='temp', **style, padding=30)
        self.add(l, 2, 1)

        self.graph1 = Status()
        sframe1 = StatusFrame(self, self.graph1, 'graph 1')
        self.add(sframe1, 1, 0)
        self.graph2 = Status()
        sframe2 = StatusFrame(self, self.graph2, 'graph 2')
        self.add(sframe2, 2, 0)

    def update(self, copycat):
        self.primary.update(copycat)
        temp      = copycat.temperature.value()
        slipnodes = copycat.slipnet.slipnodes
        codelets  = copycat.coderack.codelets

        slipList = self.widgets['sliplist']
        slipList.delete(0, slipList.size())
        self.widgets['temp']['text'] = 'Temp:\n{}'.format(round(temp, 2))
        slipnodes = sorted(slipnodes, key=lambda s:s.activation, reverse=True)
        for item in slipnodes:
            listStr = '{}: {}'.format(item.name, round(item.activation, 2))
            slipList.insert(tk.END, listStr)

        codeletList = self.widgets['codeletlist']
        codeletList.delete(0, codeletList.size())
        codelets = sorted(codelets, key=lambda c:c.urgency, reverse=True)
        for codelet in codelets:
            listStr = '{}: {}'.format(codelet.name, round(codelet.urgency, 2))
            codeletList.insert(tk.END, listStr)

class GUI(object):
    def __init__(self, title, updateInterval=.1):
        self.root = tk.Tk()
        self.root.title(title)
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)
        self.app = MainApplication(self.root)
        self.app.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.lastUpdated = time.time()
        self.updateInterval = updateInterval

    def update(self, copycat):
        self.root.update_idletasks()
        self.root.update()
        current = time.time()
        if current - self.lastUpdated > self.updateInterval:
            self.app.update(copycat)
            self.lastUpdated = current
