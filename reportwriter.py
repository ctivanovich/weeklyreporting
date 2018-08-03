import os
import openpyxl
import pickle
import sys

from fields import fields

column = 'CI'
name_col = 'E'

pklpaths = [p for p in os.listdir('../temp') if '.pkl' in p]
template = '../temp/report_template.xlsx'

def write_report(region, pkl, sh, wb):
    for q, entry in fields.items():
        if type(entry) == int:
            #then one-row query
            shloc = column+str(entry)
            write_val = p[q][0][0] #eg {'q1':[(100,)]}
            sh[shloc] = write_val
            print(q, shloc, write_val)
        else: #then field is a dict of name, nrow pairs
            results = p[q] #eg [('APP下载', 273764),('微信卡包', 367695),('微信小程序', 3420), etc
            for name, datum in results: #name, value tuple
                nrow = entry[name]
                shloc = column + str(nrow)
                sh[shloc] = datum
                print(q, nrow, shloc, datum)
    wb.save(f'../temp/{region}.xlsx')

if __name__ == "__main__":
    for pkl in pklpaths:
        with open('../temp/'+ pkl, 'rb') as f:
            region = pkl[:-4]
            p = pickle.load(f)
            wb = openpyxl.load_workbook(template)
            sh = wb['weekly']
            write_report(region, p, sh, wb)
