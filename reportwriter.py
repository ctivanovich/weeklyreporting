import os
import openpyxl
import pickle
from decimal import Decimal

from fields import fields

column = 'CI'
name_col = 'E'

pklpaths = [p for p in os.listdir() if '.pkl' in p]
regions = ['sh-lawson', 'bj-lawson', 'cq-lawson', 'wh-lawson', 'dl-lawson']
template = '../report_template.xlsx'

with open(pklpaths[3], 'rb') as f:
    p = pickle.load(f)
    wb = openpyxl.load_workbook(template)
    sh = wb['weekly']

for q, rows in fields.items():
        if type(rows) == int:
            cells = [column + str(rows)]
            names = [name_col + str(rows)]
        else:
            cells = [column+str(r) for r in rows]
            names = [name_col+str(r) for r in rows]
        for name, cnum in zip(names, cells):
            try:
                res = p['q'+str(q)]
                print(sh[name].value, res[0])
                if sh[name].value == res[0]:
                    print(f"name {name} and cell {cell} match")
            except IndexError:
                print(f"No entry for query {q} or res at {i} for {q} nonexistent")
#18,19,20,27,59
sh.columns('E')
