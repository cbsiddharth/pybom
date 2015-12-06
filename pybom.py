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

    def import_from_csv(self, filename):
        num_updated = 0
        with open(abs_path(filename), 'r') as f:
            items = csv.reader(f, delimiter=',', quotechar='"')
            for row in items:
                new = Item(row)
                db_key = new.primary_val()
                if db_key is new.primary_key():
                    continue
                if db_key not in self.item_database:
                    # Import new keys only.
                    self.item_database[db_key] = new
                    num_updated += 1
        return num_updated


class Item:
    def __init__(self, item_list):
        dt = self.make_dict(item_list)
        self.item = dt

    def __str__(self):
        s = ''
        for i in self.item_prototype:
            if len(s) > 0:
                s += ', '
            s += '%s : %s' % (i, self.item[i])
        return s

    item_prototype = ['Mfr-pn', 'Mfr', 'Footprint', 'Description', 'Stock']

    def primary_key(self):
        return self.item_prototype[0]

    def primary_val(self):
        return self.item.get(self.primary_key(), 'empty')

    def make_dict(self, item_list):
        d = {}
        if len(self.item_prototype) != len(item_list):
            return d
        else:
            d = dict(zip(self.item_prototype, item_list))
            return d

if __name__ == '__main__':
    db = DataBaseManager()
    # db.purge_records()
    num_imported = db.import_from_csv('sample-bom.csv')
    print('Import successful. Added %d items' % num_imported)
    db.save_changes()