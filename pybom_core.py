import csv
import os
import shelve


def abs_path(name=''):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return os.path.join(__location__, name)


def ordered_list_from_dict(lst, dt):
    ordered = []
    for i in lst:
        ordered.append(dt[i])
    return ordered


class Manager:
    db_file_name = 'db_file'
    database = {}

    def __init__(self):
        self.load_db()

    def load_db(self):
        f = shelve.open(self.db_file_name)
        for key in f:
            self.database[key] = f[key]
        f.close()

    def save_changes(self):
        f = shelve.open(self.db_file_name)
        f.update(self.database)
        f.close()

    def purge_records(self):
        f = shelve.open(self.db_file_name)
        f.clear()
        f.close()


class ItemManager(Manager):
    db_file_name = 'item_db'

    def import_from_csv(self, filename):
        num_updated = 0
        try:
            with open(abs_path(filename), 'r') as f:
                items = csv.reader(f, delimiter=',', quotechar='"')
                for row in items:
                    new = Item(row)
                    db_key = new.primary_val()
                    if db_key is new.primary_key():
                        continue
                    if db_key not in self.database:
                        # Import new keys only.
                        self.database[db_key] = new
                        num_updated += 1
        except EnvironmentError:
            print('File Not Found at CWD: %s' % abs_path())
        return num_updated

    def export_to_csv(self, file_name):
        with open(abs_path(file_name), 'w') as f:
            csv_fd = csv.writer(f, delimiter=',', quotechar='"')
            item_obj = Item()
            csv_fd.writerow(item_obj.prototype)
            for db_key in self.database:
                d = self.database[db_key].item
                row = ordered_list_from_dict(item_obj.prototype, d)
                csv_fd.writerow(row)
        return abs_path(file_name)


class BundleManager(Manager):
    db_file_name = 'bundle_db'


class Item:
    prototype = ['Mfr-pn', 'Mfr', 'Footprint', 'Description', 'Stock']

    def __init__(self, item_list=prototype):
        dt = self.make_dict(item_list)
        self.item = dt

    def __str__(self):
        s = ''
        for i in self.prototype:
            if len(s) > 0:
                s += ', '
            s += '%s : %s' % (i, self.item[i])
        return s

    def primary_key(self):
        return self.prototype[0]

    def primary_val(self):
        return self.item.get(self.primary_key(), 'empty')

    def make_dict(self, item_list):
        d = {}
        if len(self.prototype) != len(item_list):
            return d
        else:
            d = dict(zip(self.prototype, item_list))
            return d


class Bundle:
    prototype = ['Mfr-pn', 'Qtr']

    def __init__(self, name):
        self.name = name
        self.item_list = []
        self.qty_list = []

    def __str__(self):
        s = 'Bundle: %s\n' % self.name
        num = 0
        for i, q in zip(self.item_list, self.qty_list):
            s += '%s : %s\n' % (i, q)
            num += 1

    def add_item(self, p_key, qty):
        self.item_list.append(p_key)
        self.qty_list.append(qty)


if __name__ == '__main__':
    db = ItemManager()
    # db.purge_records()
    num_imported = db.import_from_csv('sample_import.csv')
    print('Import successful. Added %d items' % num_imported)
    db.save_changes()
    # db.export_to_csv('sample_export.csv')
