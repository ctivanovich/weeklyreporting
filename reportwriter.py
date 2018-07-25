import os
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import json
import csv
from decimal import Decimal
os.getcwd()

with open(os.getcwd()+ '\\weekreport\\results.pickle', 'rb') as f:
    res = pickle.load(f)
clean_res = {}
for k in res:
    clean_res[int(k[1:])] = res[k]
df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in clean_res.items() ])).transpose().sort_index()

df.to_excel('results.xlsx')
