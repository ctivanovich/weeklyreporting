# -*- coding: utf-8 -*-
import config
import sys
import mysql.connector


class DBConnector:
    '''Creates a database connection and exposes the connection'''
    def __init__(self, dbtype='mysql', ssh_local_port=8000):
        self.dbtype = dbtype
        self.config = config
        self.ssh_local_port = ssh_local_port


    def connect_db(self):
        if self.dbtype == 'mysql':
            con = mysql.connector.connect(**config.mysql_config)
            return con

#        elif self.dbtype == 'postgre':
#            con = psycopg2.connect(**config.postgre_config)
#            return con

        else:
            print("Please pass 'mysql' or 'postgre' to identify correct database.")
