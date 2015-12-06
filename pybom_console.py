#!/usr/bin/env python
from os import sys
from pybom_core import *

mainMenu = """
+-----------------------------------------------+
| pyBOM - A light weight Bill Of Materials (BOM)|
| manager for electronics stock keeping units   |
+-----------------------------------------------+
Options:
    1] List all items
    2] Add/Update new item
    3] Fetch existing item
    4] Save local Changes
    5] Import data
    6] Export data
    7] Purge records
    8] Quit
-----------------------------------------------
"""


def confirm_action(msg):
    act = input('%s [Y/n]: ' % msg)
    if act is 'y' or act is 'Y':
        return True
    else:
        return False


class Console:
    def __init__(self, item_db, bundle_db):
        self.item_db = item_db
        self.bundle_db = bundle_db

    @staticmethod
    def get_item(mfr_pn):
        item_list = list()
        item_list.append(mfr_pn)
        item_list.append(input('Enter Manufacturer: '))
        item_list.append(input('Enter Footprint: '))
        item_list.append(input('Enter Description: '))
        item_list.append(input('Enter Stock At hand: '))
        return Item(item_list)

    def get_new_item(self):
        mfr_pn = input('Enter Manufacturer Part Number: ')
        has_new = 0
        new = Item()
        if mfr_pn in self.item_db.database:
            print('Item already exits!')
            self.fetch_item(mfr_pn)
            if confirm_action('Do you wish to replace it?'):
                new = self.get_item(mfr_pn)
                has_new = 1
        else:
            new = self.get_item(mfr_pn)
            has_new = 1

        if has_new:
            print('Existing: ', end='')
            self.fetch_item(mfr_pn)
            print('Entered:  ', end="")
            print(new)
            if confirm_action('Make changes?'):
                self.item_db.database[mfr_pn] = new

    def import_db(self):
        print('Choose DB to import:')
        print('A] Item DB')
        print('B] Bundle DB')
        key = input('Enter choice: ')
        if key is 'A' or key is 'a':
            if confirm_action('Are you sure? this cannot be undone.'):
                file_name = input('Enter file name: ')
                num = self.item_db.import_from_csv(file_name)
                print('Import successful. Added %d items' % num)
        elif key is 'B' or key is 'b':
            if confirm_action('Are you sure? this cannot be undone.'):
                file_name = input('Enter file name: ')
                num = self.bundle_db.import_from_csv(file_name)
                print('Import successful. Added %d items' % num)
        else:
            print('Invalid Option!')

    def export_db(self):
        print('Choose DB to export:')
        print('A] Item DB')
        print('B] Bundle DB')
        key = input('Enter choice: ')
        print('you entered %s' % key)
        if key is 'A' or key is 'a':
            file_path = self.item_db.export_to_csv('bundle_db.csv')
            print('Done Exporting to %s' % file_path)
        elif key is 'B' or key is 'b':
            file_path = self.bundle_db.export_to_csv('bundle_db.csv')
            print('Done Exporting to %s' % file_path)
        else:
            print('Invalid Option!')

    def purge_db(self):
        print('Choose a DB to purge:')
        print('A] Item DB')
        print('B] Bundle DB')
        key = input('Enter option: ')
        if key is 'A' or key is 'a':
            if confirm_action('Are you sure? this cannot be undone.'):
                self.item_db.purge_records()
        elif key is 'B' or key is 'b':
            if confirm_action('Are you sure? this cannot be undone.'):
                self.bundle_db.purge_records()
        else:
            print('Invalid Option!')

    def list_items(self):
        for i in self.item_db.database:
            print(self.item_db.database[i])

    def fetch_item(self, key):
        if key in self.item_db.database:
            print(self.item_db.database[key])
        else:
            print('Key not found')

    def display_loop(self):
        print(mainMenu)
        key = input('Choose an option: ')
        k = eval(key)
        if k == 1:
            self.list_items()
        if k == 2:
            self.get_new_item()
        if k == 3:
            mfr_pn = input('Enter Mrf-pn: ')
            self.fetch_item(mfr_pn)
        elif k == 4:
            if confirm_action('Do you wish to save local changes? This cannot be undone.'):
                self.item_db.save_changes()
        elif k == 5:
            self.import_db()
        elif k == 6:
            self.export_db()
        elif k == 7:
            self.purge_db()
        elif k == 8:
            sys.exit(0)

        if input('Press [q] to exit or any key to continue...') == 'q':
            sys.exit(0)
        else:
            self.display_loop()

if __name__ == '__main__':
    item = ItemManager()
    bundle = BundleManager()
    console = Console(item, bundle)
    console.display_loop()
