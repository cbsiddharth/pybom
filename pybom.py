import csv
import os
import shelve


def abs_path(name):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return os.path.join(__location__, name)


class DataBaseManager:
    def __init__(self):
        self.item_database = {}
        self.load_items()

    def load_items(self):
        f = shelve.open('item-db')
        for key in f:
            self.item_database[key] = f[key]
        f.close()

    def save_changes(self):
        f = shelve.open('item-db')
        f.update(self.item_database)
        f.close()

    @staticmethod
    def purge_records():
        f = shelve.open('item-db')
        f.clear()
        f.close()

    def add_item_to_database(self, d):
        item = Item(mfrpn=d['Mfr-pn'], mfr=d['Mfr'], ftprint=d['Footprint'], desc=d['Description'])
        self.item_database[d['Mfr-pn']] = item

    def import_from_csv(self, filename):
        item_head = []
        head_row = 1
        num_updated = 0
        with open(abs_path(filename), 'r') as f:
            items = csv.reader(f, delimiter=',', quotechar='"')
            for row in items:
                if head_row:
                    item_head = row
                    head_row = 0
                    if 'Mfr-pn' in item_head:
                        continue
                    else:
                        break
                item = row
                d = dict(zip(item_head, item))
                key = d['Mfr-pn']
                # don't import keys that already exist.
                if key not in self.item_database:
                    self.add_item_to_database(d)
                    num_updated += 1
        return num_updated


class Item:
    def __init__(self, mfrpn, mfr=None, ftprint=None, desc=None, stock=0):
        self.mrfpn = mfrpn
        self.mfr = mfr
        self.ftprint = ftprint
        self.desc = desc
        self.stock = stock

    def __str__(self):
        return '%s, %s, %s, %s' % (self.mrfpn, self.mfr, self.ftprint, self.desc)