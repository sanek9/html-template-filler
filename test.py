#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error

class TermUI(object):
    def __init__(self):
        
        
        self._run = True
        self.comm = {
                "a" : self.select,
                "e" : self.exit
            }
    def select(self):
        try:
            conn = mysql.connector.connect(host='192.168.21.70',
                                        database='kadry',
                                        user='sanek9',
                                        password='suse100')
            if conn.is_connected():
                print('Connected to MySQL database')

            cursor = conn.cursor()
            line = raw_input("find:> ")
            cursor.execute("SELECT Family, Imya, Otch FROM Tsostav where  (Family like {0}) or (Imya like {0}) or (Otch like {0});".format("'%"+line+"%'"))
            row = cursor.fetchone()

            while row is not None:
                print(row[0]+" "+row[1]+" "+row[2])
                row = cursor.fetchone()
            
        except Error as e:
            print(e)

        finally:
            conn.close()
        
    def exit(self):
        self._run = False
    
    def run(self):
        while self._run:
            line = raw_input(":> ")
            print line
            try:
                self.comm[line]()
            except KeyError as e:
                print ('Undefined unit: {}'.format(e.args[0]))

ui = TermUI()
ui.run()
