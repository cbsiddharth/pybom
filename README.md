# pyBOM - OpenSource BOM/Inventory Manager

pyBOM is a simple, open source, light weight, BOM (Bill Of Materials) and inventory management tool for the electronic stock keeping units.

The requirement for this tools has been derived out of real world problems that I faced when trying to find a free tool that was tailored to meet the need of a small company or an electronic hobbyist.

**This project is under active development. Forks are encouraged!**

### File Organisation
* `pybom_core.py` - Has all the bases classes and data type definitions
* `pybom_console.py` - Text based console app. Primarily used as testing environment.
* `pybom_gui.py` - (TODO) Standalone Tkinter GUI
* `pybom.py` - (TODO) Web version of the same UI to simplify things in production environment.

### Features/TODOs:
1) Add/Edit/Update Component (Item) entry.
2) Incoming / Outgoing stock bulk update.
3) Create PCB units (Bundles) with component and quantity.
4) PCB units that can be made with current stock at hand.
5) Bulk import / export of data.
6) Support for barcode scanner in stock management.

### Note:
I am not a python developer by profession. So chances are you will see a lot bad decisions in data types and code structuring. So instead of just bitching about it, roll up your sleeves and get yours hands dirty.

### Contributing:
This project is under development. Patches/forks are welcome.
Mail: siddharth3141@gmail.com