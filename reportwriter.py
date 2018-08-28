import datetime
import os
import pickle
import sys

from copy import copy
from decimal import Decimal

import openpyxl
from openpyxl.formula import Tokenizer

from fields import fields

report_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%m/%d/%Y")

paths = [['../temp/'+p, '../temp/' + p[:-4] + '.xlsx'] for p in os.listdir('../temp') if '.pkl' in p]

def write_report(pkl, sh, next_col):
    for q, entry in fields.items():
        try:
            if type(entry) == int:
                #then one-row query
                shloc = next_col + str(entry)
                write_val = p[q][0][0] #eg {'q1':[(100,)]}
                if write_val == None:
                    sh[shloc] = 0
                else:
                    sh[shloc] = float(write_val)
            elif type(entry) == dict: #then field is a dict of name, nrow pairs
                results = p[q] #eg [('APP下载', 273764),('微信卡包', 367695),('微信小程序', 3420), etc
                for name, datum in results: #name, value tuple
                    nrow = str(entry[name])
                    shloc = next_col + nrow
                    if datum == None:
                        sh[shloc] = 0
                    else:
                        sh[shloc] = float(datum)
        except KeyError:
            print(f'{q} is not in the results dictionary for {region}')

def init_new_col(sh, cur_col):
    next_col = openpyxl.utils.get_column_letter(openpyxl.utils.column_index_from_string(cur_col) + 1)
    prev_col =  openpyxl.utils.get_column_letter(openpyxl.utils.column_index_from_string(cur_col) - 1)
    for i, row in enumerate(openpyxl.utils.rows_from_range('{0}2:{0}213'.format(cur_col))):
        cell = sh[row[0]]
        new_cell = sh[next_col+str(i+2)]
        if type(cell.value) == type(None) or  cell.value == '-':
            new_cell.value = 0
        elif type(cell.value)==str:
            formula = '='+ ''.join([item.value for item in Tokenizer(cell.value).items])
            if prev_col in formula:
                if 'SUM' not in formula or 'AVG' not in formula:
                    formula = formula.replace(prev_col, cur_col)
            formula = formula.replace(cur_col, next_col)
            new_cell.value = formula
            print(formula)
        if cell.has_style:
            new_cell._style = copy(cell._style)

if __name__ == "__main__":
    for pklpath, reportpath in paths:
        with open(pklpath, 'rb') as f:
            region = pklpath[8:-4]
            p = pickle.load(f)
            wb = openpyxl.load_workbook(reportpath)
            sh = wb['报告－每周']
            cur_col = list(sh.columns)[-1][0].column
            next_col = openpyxl.utils.get_column_letter(openpyxl.utils.column_index_from_string(cur_col) + 1)
            init_new_col(sh, cur_col) #writes new column for next week, adding formulae and styles
            sh[next_col+str(2)] = report_date
            write_report(p, sh, next_col)
            wb.save(f'../temp/{region}.xlsx')
