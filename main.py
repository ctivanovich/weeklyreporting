# -*- coding: utf-8 -*-
import csv
import logging
import threading
from threading import Lock
import sys

from sshtunnel import SSHTunnelForwarder

import config
from queries import QUERIES
from dbconnect import DBConnector

results = {}

queries = [(k,v) for k,v in QUERIES.items()]
db_type = 'mysql'

def get_logger():
    logger = logging.getLogger("threading")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("threading.log")
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger

def active_ssh_server(local_bind_address):
    ssh_server = SSHTunnelForwarder(('115.29.237.50', 22),
                                    ssh_username="ivanovich",
                                    ssh_password="Spo3UWNqBc",
                                    remote_bind_address =
                                    ('rdsnfjbfyfquanq.mysql.rds.aliyuncs.com', 3306),
                                    local_bind_address=local_bind_address)
    return ssh_server, ssh_server.local_bind_port

def run_query(qname, query, port):
    conn = DBConnector(db_type, port).connect_db()
    cur = conn.cursor()
    cur.execute(query)
    results[qname] = len(cur.fetchall())
    print(results)
    cur.close()

def main_run(qname, queries, ssh_local_port):
    with lock:
        ssh_server.start()
        n_threads = 2
        n_queries = 2
        threads = []
        run_query(qname, query, ssh_local_port)

if __name__ == '__main__':
    # db_type = sys.argv[1]
    n_threads = 1
    n_queries = 1
    threads = []
    local_bind_addresses = [('0.0.0.0', 8000+i) for i in range(n_threads)]
    lock = Lock()
    ssh_server, ssh_local_ports = active_ssh_server(('0.0.0.0', 8000))
    # main(queries, ssh_local_port, 8)
    # ssh_server.close()
    for qname, query in queries:
    #to cycle through all queries
        # Loop/create/start
        if n_queries == 0:
            break
        for i in range(n_threads):
            if n_queries == 0:
                break
            # try:
            t = threading.Thread(target=main_run, #sets thread to use main()
                args=(qname, query, 8000), #args for main()
                name=qname, daemon=True) #name of thread matches query name
            t.start()
            threads.append(t)
        # except:
            # print("Something with thread happened")
        # finally:
            n_queries -= 1
    print("Waiting for threads to complete tasks...")

    try:
        for i in threads:
            i.join(timeout=1.0)
    except (KeyboardInterrupt, SystemExit):
        print("Caught Ctrl-C on thread joining. Cleaning up. Exiting.")
    finally:
        print(results, threads)
