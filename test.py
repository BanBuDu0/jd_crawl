import db_control
import os

i = db_control.finddata('鞋子')
    
if not i:
    print('not None')