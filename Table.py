import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from Inventory import *


class InventoryTable(tk.Frame):
    def __init__(self, parent, frame):
        tk.Frame.__init__(self)
        self.frame = tk.Frame(frame)
        self.parent = parent
        self.createInventoryTable()

    def createInventoryTable(self):
        actionFrame = tk.Frame(self.frame)
        tk.Button(actionFrame, text='Add', command=self.addButtonHandler).pack(side='left', padx=10)
        tk.Button(actionFrame, text='Edit', command=self.editButtonHandler).pack(side='left', padx=10)
        tk.Button(actionFrame, text='Delete', command=self.deleteButtonHandler).pack(side='left', padx=10)
        tk.Button(actionFrame, text='Export', command=self.exportButtonHandler).pack(side='left', padx=10)
        actionFrame.pack(side='top', pady=10)

        self.treeview = tv = ttk.Treeview(self.frame)
        ts = ttk.Scrollbar(self.frame)

        ts.configure(command=tv.yview)
        tv.configure(yscrollcommand=ts.set)

        tv['columns'] = ('MFRPN', 'MFR', 'FOOTPRINT', 'DESCRIPTION', 'STOCK')
        tv.heading("#0", text='ID', anchor='w')
        tv.column("#0", anchor="w", width=50)

        tv.heading('MFRPN', text='Manufacturer Part No', command=lambda: self.sortText('MFRPN', 0))
        tv.column('MFRPN', anchor='w', width=200)
        tv.heading('MFR', text='Manufacturer', command=lambda: self.sortText('MFR', 0))
        tv.column('MFR', anchor='w', width=150)
        tv.heading('FOOTPRINT', text='Footprint', command=lambda: self.sortText('FOOTPRINT', 0))
        tv.column('FOOTPRINT', anchor='w', width=100)
        tv.heading('DESCRIPTION', text='Description', command=lambda: self.sortText('DESCRIPTION', 0))
        tv.column('DESCRIPTION', anchor='w', width=350)
        tv.heading('STOCK', text='Stock', command=lambda: self.sortNumeric('STOCK', 0))
        tv.column('STOCK', anchor='e', width=50)

        tv.bind("<Double-1>", self.editButtonHandler)
        tv.bind("<Escape>", self.dropSelection)
        tv.bind("<Delete>", self.deleteButtonHandler)
        tv.pack(side='left', fill='both', expand=1)
        ts.pack(side='right', fill='y')
        self.frame.pack(fill='both', expand=1)

    def dropSelection(self, event):
        for index in self.treeview.selection():
            self.treeview.selection_remove(index)

    def editButtonHandler(self, event=None):
        index = self.treeview.selection()[0]
        item = self.getSelectedItems()[0]
        self.editItem(index, item)

    def deleteButtonHandler(self, event=None):
        selection = self.treeview.selection()
        if not selection:
            return
        result = messagebox.askquestion("Delete", "Are You Sure? "
            "The selected items will be removed permanently!", icon='warning')
        if result == 'yes':
            # first remove from DB
            items = self.getSelectedItems()
            itemIDList = []
            for item in items:
                itemIDList.append(item.item['ID'])
            self.parent.itemMgr.deleteItems(tuple(itemIDList))
            # now remove from table
            for index in selection:
                self.treeview.delete(index)

    def exportButtonHandler(self):
        try:
            file = filedialog.asksaveasfilename()
            itemList = self.getSelectedItems()
            self.parent.itemMgr.exportItemsToCSV(file, itemList)
        except Exception as err:
            messagebox.showinfo("Error", err)

    def addButtonHandler(self):
        item = Item()
        editWindow = EditItemPopup(self, item)
        self.parent.wait_window(editWindow.top)
        if editWindow.mItem is not None:
            try:
                newID = self.parent.itemMgr.insertItem(editWindow.mItem)
                editWindow.mItem.item['ID'] = newID
                self.insertItem('end', editWindow.mItem)
            except Exception as err:
                messagebox.showinfo("Error", err)

    def editItem(self, index, item):
        editWindow = EditItemPopup(self, item)
        self.parent.wait_window(editWindow.top)
        if editWindow.mItem is not None:
            self.updateSelection(index, editWindow.mItem)
            self.parent.itemMgr.updateItem(editWindow.mItem)

    def getSelectedItems(self):
        selList = self.treeview.selection()
        itemList = []
        for sel in selList:
            valList = []
            valList = self.treeview.item(sel)['values']
            valList.insert(0, self.treeview.item(sel)['text'])
            itemList.append(Item(valList))
        return itemList

    def updateSelection(self, index, item):
        pos = self.treeview.index(index)
        self.treeview.delete(index)
        self.insertItem(pos, item)

    def insertItem(self, pos, item):
        records=item.getRecords()
        self.treeview.insert('', pos, text=records[0], values=records[1:])

    def insertItemList(self, itemList):
        for item in itemList:
            self.insertItem('end', item)

    def flushRecords(self):
        self.treeview.delete(*self.treeview.get_children())

    def isnumeric(self, s):
        """test if a string is numeric"""
        for c in s:
            if c in "1234567890-.":
                numeric = True
            else:
                return False
        return numeric

    def change_numeric(self, data):
        """if the data to be sorted is numeric change to float"""
        new_data = []
        # change child to a float
        for child, col in data:
            new_data.append((float(child), col))
        return new_data

    def sortby(self, col, descending, isNumeric):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(self.treeview.set(child, col), child) for child in self.treeview.get_children('')]
        # if the data to be sorted is numeric change to float
        if isNumeric == True:
            data = self.change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            self.treeview.move(item[1], '', ix)
        # switch the heading so that it will sort in the opposite direction
        self.treeview.heading(col,
            command=lambda col=col: self.sortby(col, int(not descending), isNumeric))

    def sortText(self, col, descending):
        self.sortby(col, descending, False)

    def sortNumeric(self, col, descending):
        self.sortby(col, descending, True)