import tkinter as tk
import sys

from Inventory import Item
from UIComponents import *

class EditItemPopup(object):
    mItem = None
    dicEnt = {}
    def __init__(self, parent, oItem=None):
        self.parent = parent
        self.oItem = oItem # original item
        self.top = tk.Toplevel(None)

        frm = tk.Frame(self.top)
        frm.pack(side="top", fill="both", expand=True, padx=3, pady=3)
        formFrame = tk.Frame(frm)
        valList = Item.getPrototype()
        valList.pop(0) # remove item ID
        for i, val in zip(range(5), valList):
            tk.Label(formFrame, text=val).grid(row=i, column=0, padx=10, pady=10, sticky='ne')
            self.dicEnt[val] = tk.StringVar()
            self.dicEnt[val].set(oItem.item[val])
            ent = tk.Entry(formFrame, textvariable=self.dicEnt[val], width=32)
            ent.grid(row=i, column=1, padx=10, pady=10, sticky='nw')
        formFrame.grid()

        buttonFrame = tk.Frame(self.top)
        tk.Button(buttonFrame, text='Cancel', command=self.top.destroy).pack(side='left')
        tk.Button(buttonFrame, text='Save', command=self.entryToItem).pack(side='right')
        buttonFrame.pack(side="top", fill="both", expand=True, padx=40, pady=10)
        self.top.bind('<Return>', self.returnKeyHandler)
        self.top.bind('<Escape>', self.escapeKeyHandler)

    def escapeKeyHandler(self, event):
        self.top.destroy()

    def returnKeyHandler(self, event):
        self.entryToItem()

    def entryToItem(self):
        for proto in Item.getPrototype():
            if proto in self.dicEnt.keys():
                value = self.dicEnt[proto].get()
                valList.append(value)
        # insert not editable fields.
        valList.insert(0, self.oItem.item['ID'])
        new = Item(valList)
        if not Item.compare(self.oItem, new):
            self.mItem = new
        self.top.destroy()

class MenuBar(tk.Menu):
    exportFileName = ""
    importFileName = ""
    dbFileName = ""
    def __init__(self, parent):
        self.parent = parent
        tk.Menu.__init__(self, parent)

        filemenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=filemenu)
        filemenu.add_command(label="New Database",  underline=0, command=self.parent.createDatabase)
        filemenu.add_command(label="Open Database", underline=0, command=self.parent.openDatabase)

        filemenu.add_separator()
        filemenu.add_command(label="Exit", underline=1, command=self.quit)

        toolsmenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Tools",underline=0, menu=toolsmenu)
        toolsmenu.add_command(label="Export Inventory", underline=0, command=self.parent.exportInventory)
        toolsmenu.add_command(label="Import Inventory", underline=0, command=self.parent.importInventory)
        
        helpmenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help",underline=0, menu=helpmenu)
        helpmenu.add_command(label="About", underline=0, command=self.showAbout)

    def quit(self):
        sys.exit(0)

    def showAbout(self):
        toplevel = tk.Toplevel()
        toplevel.title("About pyBOM")
        ABOUT_TEXT = """
        pyBOM is a light weight, BOM (Bill Of Materials) and
        inventory management tool for the electronic stock keeping units.

        Siddharth Chandrasekaran
        siddharth@embedjournal.com"""
        tk.Label(toplevel, text=ABOUT_TEXT, height=10, width=80).pack(fill='both', padx=20)
