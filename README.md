### Restore broken .dxf files created by netDxf

Sometimes software that uses netDxf generates broken files with textstrings being split to multiple lines. 
This app restores the lines, deletes false ones and creates restored dxf file.

Runs on *Python 3*

UI is executed with *PyQt5* package

Requirements are listed in [requirements.txt](/requirements.txt)

**To run the app use** `python app_fix_dxf.py`