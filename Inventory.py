import csv
import sqlite3
import tkinter as tk
import sys


class DatabaseManager(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def __del__(self):
        self.conn.close()


class Item:
    def __init__(self, itemList=None):
        self.item = self.make_dict(list(itemList))

    def __str__(self):
        return "'%d', '%s', '%s', '%s', '%s', %s" % ( self.item['ID'], self.item['MFRPN'], self.item['MFR'], self.item['FOOTPRINT'],
                self.item['DESCRIPTION'], self.item['STOCK'] )

    @staticmethod
    def getPrototype():
        return ['ID', 'MFRPN', 'MFR', 'FOOTPRINT', 'DESCRIPTION', 'STOCK']

    @staticmethod
    def compare(item1, item2):
        for key in item1.item.keys():
            if key not in item2.item.keys():
                return False
            if key == 'ID':
                continue
            if item1.item[key] != item2.item[key]:
                return False
        return True

    def getItemList(self):
        return [ self.item['ID'], self.item['MFRPN'], self.item['MFR'], self.item['FOOTPRINT'],
                self.item['DESCRIPTION'], self.item['STOCK'] ]

    def getStrInsertDB(self):
        return "null, '%s', '%s', '%s', '%s', %s" % ( self.item['MFRPN'], self.item['MFR'], self.item['FOOTPRINT'],
                self.item['DESCRIPTION'], self.item['STOCK'] )

    def make_dict(self, itemList):
        if len(Item.getPrototype()) != len(itemList):
            print ("->" + str(Item.getPrototype()))
            print ("<-" + str(itemList))
            raise Exception("Inalid item entry!")
        else:
            itemList[0] = int(itemList[0])
            itemList[5] = int(itemList[5])
            return dict(zip(Item.getPrototype(), itemList))


class ItemManager:
    def __init__(self, parent):
        self.parent = parent
    
    def openDatabase(self, dbFile):
        db = DatabaseManager(dbFile)
        try:
            tables = db.query("SELECT name FROM sqlite_master WHERE type='table';", ).fetchone()
        except sqlite3.DatabaseError:
            raise Exception('Invlaid Inventory File!')

        inventory = []
        for table in tables:
            found=1
            db.query("SELECT * FROM %s;" % table)
            fieldnames=[f[0] for f in db.cur.description]
            if len(fieldnames) != len(Item.getPrototype()):
                found = 0
            else:
                for val in Item.getPrototype():
                    if val not in fieldnames:
                        found = 0
            if found == 1:
                inventory.append(table)

        if len(inventory) == 0:
            raise Exception("Doesn't look like a valid inverntory file")
            return

        self.dbFile = dbFile
        
    def loadInventoryTable(self, table):
        db = DatabaseManager(self.dbFile)
        rows = db.query("SELECT * FROM INVENTORY;").fetchall()
        for row in rows:
            item = Item(row)
            table.insertItem(item)

    def createDatabase(self, dbFile):
        db = DatabaseManager(dbFile)
        db.query('CREATE TABLE IF NOT EXISTS INVENTORY (ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            ' MFRPN NOT NULL, MFR TEXT, FOOTPRINT TEXT, DESCRIPTION TEXT, STOCK INT NOT NULL);')
        self.dbFile = dbFile

    def insertItemToInventory(self, itemList):
        db = DatabaseManager(self.dbFile)
        for item in itemList:
            db.query('INSERT OR IGNORE INTO INVENTORY VALUES (%s);' % item.getStrInsertDB())

    def getItemFromID(self, itemID):
        db = DatabaseManager(self.dbFile)
        row = db.query('SELECT * FROM INVENTORY WHERE ID=%d;' % itemID).fetchone()
        return Item(row)

    def updateItem(self, item):
        db = DatabaseManager(self.dbFile)
        query = 'UPDATE INVENTORY SET '
        notStart = False
        for key in item.item.keys():
            if key == 'ID':
                continue
            if notStart:
                query += ', '
            if key == 'STOCK':
                query += key + " = " + str(item.item[key])
            else:
                # strings have to be of the form 'str'
                query += key + " = '" + str(item.item[key]) + "'"
            notStart = True
        query += ' WHERE ID = %d;' % item.item['ID'] 
        db.query(query)

    def importInventoryFromCSV(self, filename):
        try:
            itemList = []
            with open(filename, 'r') as f:
                rows = csv.reader(f, delimiter=',', quotechar='"')
                for row in rows:
                    if (row != Item.getPrototype()):
                        itemList.append(Item(row))
            self.insertItemToInventory(itemList)

        except EnvironmentError:
            print('File error: %s' % filename)


    def exportInventoryToCSV(self, filename):
        db = DatabaseManager(self.dbFile)
        rows = db.query("SELECT * FROM INVENTORY;")
        with open(filename, 'w') as f:
            wfd = csv.writer(f, delimiter=',', quotechar='"')
            wfd.writerow(Item.getPrototype())
            wfd.writerows(rows)
