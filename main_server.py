# -*- coding: utf-8 -*-
from multiprocessing.pool import ThreadPool
import pickle
import config

from reportwriter import write_results
from queries import postgre_queries as QUERIES
from dbconnect import DBConnector

results = {}

queries = [(k,v) for k,v in QUERIES.items()]
db_type = 'postgre'
pool = ThreadPool(processes=8)

def log_decorator(func):
    def logger(*args, **kwargs):
        import logging
        import sys
        import time
        log = logging.getLogger(args[0][0]) #the name of the query as logfile name
        log.setLevel(logging.DEBUG)
        fh = logging.FileHandler(f"{time.strftime('%Y%m%d%H%M%S')}.log")
        handler = logging.StreamHandler(stream=sys.stdout)
        log.addHandler(handler)
        fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        fh.setFormatter(formatter)
        log.addHandler(fh)
        try:
            log.debug("Initiating process and query")
            start = time.time()
            func(args[0]) #corresponds to passing sql query to run_query
            total = (time.time()-start)/60
            log.debug("Process exited in approx. {0:.2f} minutes".format(total))
        except:
            log.error("Uncaught exception")
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
    n_queries = len(queries)
    pool.map(run_query, queries)
    # print("Waiting for threads to complete tasks...")
    pool.close()
    pool.join()
    print(f"{len(results)} queries successfully executed")
    # write_results(results)
