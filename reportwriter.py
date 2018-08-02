import os
import openpyxl
import pickle

from fields import fields

column = 'CI'
name_col = 'E'

pklpaths = [p for p in os.listdir('../temp') if '.pkl' in p]
regions = ['sh-lawson', 'bj-lawson', 'cq-lawson', 'wh-lawson', 'dl-lawson']
template = '../temp/report_template.xlsx'

for pkl in pklpaths:
    with open('../temp/'+ pkl, 'rb') as f:
        p = pickle.load(f)
        wb = openpyxl.load_workbook(template)
        sh = wb['weekly']

    for q, entry in fields.items():
        if type(entry) == int:
            #then one-row query
            shloc = column+str(entry)
            write_val = p[q][0][0] #eg {'q1':[(100,)]}
            sh[shloc] = write_val
        else: #then field is a dict of name, nrow pairs
            results = p[q] #eg [('APP下载', 273764),('微信卡包', 367695),('微信小程序', 3420), etc
            for name, datum in results: #name, value tuple
                nrow = entry[name]
                shloc = column + str(nrow)
                sh[shloc] = datum

    wb.save(f'../temp/{pkl[:-4]}.xlsx')
