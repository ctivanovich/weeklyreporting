# -*- coding: utf-8 -*-
import csv
import threading
import sys

import config
from queries import QUERIES
from dbconnect import DBConnector
from weeklygatherer import WeeklyGatherer


ARGS = sys.argv
db_type = ARGS[1]

def multithread(n = 1, names = [], ids = []):
    pass

if __name__ == '__main__':
    dbc = DBConnector(db_type, config)
    cur = dbc.connect_db().cursor()

    session = WeeklyGatherer(QUERIES, cur)
    cur.close()
    results = session.fetch_queries()
