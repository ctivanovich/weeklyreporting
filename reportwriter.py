from decimal import Decimal
import datetime
import os
import openpyxl
import pickle
import pprint
import sys

from fields import fields


# report_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y/%m/%d")
report_date = '2018/07/23'
column = 'H'
name_col = 'E'

pklpaths = [p for p in os.listdir('../temp') if '.pkl' in p]
template = '../temp/report_template.xlsx'

def write_report(region, pkl, sh, wb):
    for q, entry in fields.items():
        try:
            if type(entry) == int:
                #then one-row query
                shloc = column+str(entry)
                write_val = p[q][0][0] #eg {'q1':[(100,)]}
                if write_val == None:
                    sh[shloc] = '-'
                else:
                    sh[shloc] = float(write_val)
                    # sh[shloc].number_format = '0,000.0'
                    # print(q, shloc, write_val)
            else: #then field is a dict of name, nrow pairs
                results = p[q] #eg [('APP下载', 273764),('微信卡包', 367695),('微信小程序', 3420), etc
                for name, datum in results: #name, value tuple
                    if datum == None:
                        sh[shloc] = '-'
                    else:
                        nrow = entry[name]
                        shloc = column + str(nrow)
                        sh[shloc] = float(datum)
                        # sh[shloc].number_format = '0,000.0'
                        # print(q, nrow, shloc, datum)
        except KeyError:
            print(f'{q} is not in the results dictionary for {region}')
    wb.save(f'../temp/{region}.xlsx')

if __name__ == "__main__":
    for pkl in pklpaths:
        with open('../temp/'+ pkl, 'rb') as f:
            region = pkl[:-4]
            p = pickle.load(f)
            wb = openpyxl.load_workbook(template)
            sh = wb['weekly']
            sh[column+str(2)] = report_date
            write_report(region, p, sh, wb)
