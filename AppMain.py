import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from Inventory import *
from UIComponents import MenuBar
from Table import *


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.configure()
        self.nb = ttk.Notebook(self)
        self.itemMgr = ItemManager(self)
        self.menubar = MenuBar(self)
        self.config(menu=self.menubar)
        
        self.iTable = InventoryTable(self)
        self.nb.add(self.iTable, text="Inventory")

        editFrame = tk.Frame(self)
        sString = tk.StringVar()
        tk.Label(editFrame, text="Search" ).grid(row=0, column=0, sticky='w', pady=3, padx=10)
        tk.Entry(editFrame, width=32, textvariable=sString).grid(row=0, column=1, padx=10)
        ttk.Button(editFrame, text='Search', command=(lambda: self.searchTable(
            sString.get()))).grid(row=0, column=2, sticky='w', padx=10)
        editFrame.pack(side='top', pady=20)
        self.nb.add(editFrame, text="Edit")
        self.nb.pack(fill='both', expand=1, padx=3, pady=3)

        try:
            self.itemMgr.openDatabase('item.DB')
            itemList = self.itemMgr.getInventoryItemList()
            self.iTable.insertItemList(itemList)
            print('Loaded defalut DB..')
        except Exception as err:
            print("Default DB error: " + str(err))

    def openDatabase(self):
        try:
            name = filedialog.askopenfilename()
            self.itemMgr.openDatabase(name)
            self.table.flushRecords()
            itemList = self.itemMgr.getInventoryItemList()
            self.iTable.insertItemList(itemList)
        except Exception as err:
            self.showError(err)
        
    def createDatabase(self):
        try:
            name = filedialog.asksaveasfilename()
            self.itemMgr.createDatabase(name)
        except Exception as err:
            self.showError(err)

    def importInventory(self):
        try:
            self.itemMgr.importInventoryFromCSV(filedialog.askopenfilename())
            self.iTable.flushRecords()
            itemList = self.itemMgr.getInventoryItemList()
            self.iTable.insertItemList(itemList)
        except Exception as err:
            self.showError(err)

    def exportInventory(self):
        self.itemMgr.exportInventoryToCSV(filedialog.asksaveasfilename())   
        
    def configure(self):
        # config stuffs
        self.title("PyBom")
        self.geometry("1200x600+100+100")

    def showError(self, msg):
        messagebox.showinfo("Error", msg)


if __name__ == "__main__":
    app=App()
    app.mainloop()
