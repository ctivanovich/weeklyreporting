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

region = sys.argv[1]
queries = [(k,v) for k,v in get_queries(region).items()]

db_type = 'mysql'

pool = ThreadPool(processes=8)

def set_region(region):
    return sys.argv[1]

def log_decorator(func):
    def logger(*args, **kwargs):
        log = logging.getLogger(args[0][0]) #the name of the query as logfile name
        log.setLevel(logging.DEBUG)
        log.addHandler(log_fh)
        try:
            log.debug(f"Initiating process and query for  {args[0][0]}")
            start = time.time()
            func(args[0]) #corresponds to passing sql query to run_query
            total = (time.time()-start)/60
            log.debug("Process exited in approx. {0:.2f} minutes".format(total))
        except:
            log.error(f"Uncaught exception for  {args[0][0]}")
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

    #run pool of processes
    pool.map(run_query, queries)
    pool.close()
    pool.join()
    print(f"{len(results)} of {len(queries[1:])} queries successfully executed")
    with open('results.pickle', 'wb') as f:
        pickle.dump(results, f)
