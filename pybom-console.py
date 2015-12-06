#!/usr/bin/env python
from os import sys
from pybom import DataBaseManager
from pybom import Item
    

message = """
+-----------------------------------------------+
| pyBOM - A light weight Bill Of Materials (BOM)|
| manager for electronics stock keeping units   |
+-----------------------------------------------+
Options:
    1] List all items
    2] Add/Update new item
    3] Fetch existing item
    4] Save local Changes
    5] Quit
-----------------------------------------------
"""


def confirm_action(msg):
    act = input('%s [Y/n]: ' % msg)
    if act is 'y' or act is 'Y':
        return True
    else:
        return False


class Console:
    def __init__(self):
        self.db = DataBaseManager()

    def list_items(self):
        for item in self.db.item_database:
            print(self.db.item_database[item])

    def fetch_item(self, key):
        if key in self.db.item_database:
            print(self.db.item_database[key])
        else:
            print('Key not found')

    @staticmethod
    def get_item(mfr_pn):
        mfr = input('Enter Manufacturer: ')
        ft_print = input('Enter Footprint: ')
        desc = input('Enter Description: ')
        stock = input('Enter Stock At hand: ')
        item = Item(mfr_pn, mfr, ft_print, desc, stock)
        return item

    def display_loop(self):
        print(message)
        key = input('Choose an option: ')
        k = eval(key)
        if k == 1:
            self.list_items()
        if k == 2:
            mfr_pn = input('Enter Manufacturer Part Number: ')
            has_new = 0
            if mfr_pn in self.db.item_database:
                print('Item already exits!')
                self.fetch_item(self, mfr_pn)
                if confirm_action('Do you wish to update it?'):
                    new = self.get_item(mfr_pn)
                    has_new = 1
            else:
                new = self.get_item(mfr_pn)
                has_new = 1

            if has_new:
                print('You entered, ')
                self.fetch_item(mfr_pn)
                if confirm_action('Save Changes?'):
                    self.db.item_database[mfr_pn] = new

        if k == 3:
            mfr_pn = input('Enter Mrf-pn: ')
            self.fetch_item(mfr_pn)
        elif k == 4:
            if confirm_action('Do you wish to save local changes? This cannot be undone.'):
                self.db.save_changes()
        elif k == 5:
            sys.exit(0)

        if input('Press [q] to exit or any key to continue...') == 'q':
            sys.exit(0)
        else:
            self.display_loop()

if __name__ == '__main__':
    console = Console()
    console.display_loop()
