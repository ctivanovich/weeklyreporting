# -*- coding: utf-8 -*-
from multiprocessing.pool import ThreadPool
import logging
import sys
import time
import pickle
import os

from queries import get_queries
from dbconnect import DBConnector

results = {}

regions = ['sh-lawson', 'bj-lawson', 'cq-lawson', 'wh-lawson', 'dl-lawson', 'ah-lawson']
db_type = 'mysql'

pool = ThreadPool(processes=8)

def log_decorator(func):
    def logger(*args, **kwargs):
        log = logging.getLogger(args[0][0]) #the name of the query as logger name
        log.setLevel(logging.DEBUG)
        log.addHandler(log_fh)
        try:
            log.debug(f"Initiating process and query for {args[0][0]}")
            start = time.time()
            func(args[0]) #corresponds to passing sql query to run_query
            total = (time.time()-start)/60
            log.debug("Process exited in approx. {0:.2f} minutes".format(total))
        except:
            log.error(f"Uncaught exception for {args[0][0]}")
        finally:
            log.debug(f"Exiting run_query for {args[0][0]}")
        return func
    return logger

@log_decorator
def run_query(query):
    conn = DBConnector(db_type).connect_db()
    cur = conn.cursor()
    cur.execute(query[1])
    results[query[0]]= cur.fetchall()
    cur.close()

if __name__ == '__main__':
    #initiate log with common log file
    log_fh = logging.FileHandler(f"{time.strftime('%Y%m%d')}.log")
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    log_fh.setFormatter(formatter)
    results = {}

    #run pool of processes
    for region in regions:
        queries = [(k,v) for k,v in get_queries(region).items()]

        pool.map(run_query, queries)
        pool.close()
        pool.join()
        print(f"{len(results)} of {len(queries[1:])} queries successfully executed")
        import pprint
        pprint.pprint(results)
        print('\n\n')


    with open('results.pkl', 'wb') as f:
        pickle.dump(results, f)
