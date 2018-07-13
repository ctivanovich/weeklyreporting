# -*- coding: utf-8 -*-

class WeeklyGatherer:
    '''Accepts a live cursor object and runs the queries passed to it.'''
    def __init__(self, qname, query, cursor):
        self.qname = qname
        self.query = query
        self.cursor = cursor
        self.cache = {}

    def fetch_query(self):
        self.cursor.execute(self.query)
        self.cache[qname] = self.cursor.fetchall()
        return self.cache
    # def fetch_queries(self):
    #     for k, v in self.query_dict.items():
    #         self.cursor.execute(v) #queries contain hidden EOL/tabs
    #         self.cache[k] = self.cursor.fetchall()
    #     return self.cache

    def visualize_2d_array():
        pass
