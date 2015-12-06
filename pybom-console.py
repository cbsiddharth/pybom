import csv
import os
import shelve


def absPath(fname):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return os.path.join(__location__, fname)


class DataBaseManager:
    def __init__(self):
        self.itemDB = {}
        self.loadItems()

    def loadItems(self):
        f = shelve.open('item-db')
        for key in f:
            self.itemDB[key] = f[key]
        f.close()

    def saveChanges(self):
        f = shelve.open('item-db')
        f.update(self.itemDB)
        f.close()

    @staticmethod
    def purgeRecords():
        key = input('\nAre you sure you want to purge all records? [Y/n]')
        if key is 'Y' or key is 'y':
            f = shelve.open('item-db')
            f.clear()
            f.close()
            print('All records purged successfully!')

    def updateItemDB(self, head, item):
        d = {}
        for key, val in zip(head, item):
            d[key] = val

        key = d['Mfr-pn']
        if key not in self.itemDB:
            print('Adding ->', self.itemDB[key])
            self.itemDB[key] = Item(mfrpn=d['Mfr-pn'], mfr=d['Mfr'], ftprint=d['Footprint'], desc=d['Description'])

    def importFromCSV(self, filename):
        header = []
        getHead = 1
        with open(filename, 'r') as f:
            print('Parsing CSV file %s...' % filename)
            items = csv.reader(f, delimiter=',', quotechar='"')
            for row in items:
                if getHead is 1:
                    getHead = 0
                    header = row
                    if 'Mfr-pn' in header:
                        continue
                    else:
                        break
                iList = row
                self.updateItemDB(header, iList)
        print('Done Importing')


class Item:
    def __init__(self, mfrpn, mfr=None, ftprint=None, desc=None, stock=0):
        self.mrfpn = mfrpn
        self.mfr = mfr
        self.ftprint = ftprint
        self.desc = desc
        self.stock = stock

    def __str__(self):
        return '%s, %s, %s, %s' % (self.mrfpn, self.mfr, self.ftprint, self.desc)


if __name__ == '__main__':
    db = DataBaseManager()
    db.importFromCSV(absPath('sample-bom.csv'))
    # db.purgeRecords()
    db.saveChanges()
