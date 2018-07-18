import pickle
import os

os.getcwd()
with open(os.getcwd()+'\\weekreport\\results.pickle', 'rb') as f:
    results = pickle.load(f)
results
