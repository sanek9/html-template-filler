#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import mysql.connector
import os
from mysql.connector import Error
from badgebuilder import BadgeBuilder

PHOTO_PATH='photo'

class TermUI(object):
    def __init__(self):
        
        
        self._run = True
        self.comm = {
                "s" : self.select,
                "a" : self.append,
                "e" : self.exit,
                "p" : self.print_list,
                "m" : self.make
            }
        self.persons = {}
        
    def get_connection(self):
        conn = mysql.connector.connect(host='192.168.21.70',
                                        database='kadry',
                                        user='sanek9',
                                        password='suse100')
        if conn.is_connected():
            print('Connected to MySQL database')
        return conn
    def make(self):
        try:
            conn = self.get_connection();
            self._save_photo(conn, self.persons)
        except Error as e:
            print(e)

        finally:
            conn.close()
            
        bb = BadgeBuilder()
        
        
        #line = raw_input("save path [./out.pdf]: ")
        bb.make(self.persons,"out.pdf")
    def select(self):
        try:
            conn = self.get_connection();

            line = raw_input("find:> ")
            tmp = self._fetch_persons(conn, "(s.Family like {0}) or (s.Imya like {0}) or (s.Otch like {0});".format("'%"+line+"%'"))
            
            self._print_persons(tmp)
            if(tmp):
                self._add_to_list(tmp)
            
        except Error as e:
            print(e)

        finally:
            conn.close()
    def _print_persons(self, persons):
        if(persons):
            for tab, person in persons.items():
                print(u"|{:>4}|{:>20}|{:>20}|{:>20}|{:>60}|{:>60}|".format(person['tab'], person['name'], person['surname'], person['patronymic'], person['post'], person['department']))
        else:
            print("List is empty")
            
    def _fetch_persons(self, conn, where):
        cursor = conn.cursor()
        cursor.execute("SELECT s.Cod_sostav, s.N_Tab, s.Family, s.Imya, s.Otch, d.Name_dolg, o.Name_otdel \
            FROM Tsostav s\
            left join Spr_dolg d on s.Cod_dolg = d.Cod_dolg\
            left join Spr_otdel o on s.Cod_otdel = o.Cod_otdel\
            where {};".format(where))
            
        row = cursor.fetchone()
        tmp = {}
        while row is not None:
            person = {
                    'Cod_sostav' : row[0],
                    'tab' : row[1],
                    'name' : row[2],
                    'surname' : row[3],
                    'patronymic' : row[4],
                    'post' : row[5],
                    'department' : row[6],
                    'photo':None
                }
            tmp[person['tab']] = person
            
            row = cursor.fetchone()
        return tmp
                
    def append(self):
        self._add_to_list()
    def _add_to_list(self, tmp={}):
        
        f = True
        
        
        
        line = raw_input("tabs:> ")
        
        ntmp = []
        for tab in line.split(' '):
            if(tab in tmp):
                self.persons[tab] = tmp[tab]
            else:
                ntmp.append(tab)
    
        if(ntmp):
            
            print("Load from database...")
            try:
                conn = self.get_connection();
                p = self._fetch_persons(conn, "s.N_Tab in ({})".format(", ".join(ntmp)))
                self.persons.update(p)
            except Error as e:
                print(e)

            finally:
                conn.close()
        
        print("ok")
        
    def _save_photo(self, conn, persons):
        cursor = conn.cursor()
        print(persons)
        print(persons.keys())
        for n in persons.keys():
            print n
        query = "select s.N_Tab, f.Foto from Tsostav s \
        left join Tfoto f on s.Cod_sostav = f.Cod_sostav\
        where s.N_Tab in ({})".format( ', '.join(persons.keys()))
        print (query)
        cursor.execute(query)
        row = cursor.fetchone()
        while row is not None:
            path = os.path.join(PHOTO_PATH, row[0]+".jpg")
#            print("path "+path)
            with open(path, 'wb') as f:
                f.write(row[1])
#            print ("row0 "+ row[0])
            persons[row[0]]['photo'] = path
            row = cursor.fetchone()
            
    def print_list(self):
        
        self._print_persons(self.persons)
        
    def exit(self):
        self._run = False
    
    def run(self):
        while self._run:
            line = raw_input(":> ")
            try:
                self.comm[line]()
            except KeyError as e:
                print ('Undefined unit: {}'.format(e.args[0]))

ui = TermUI()
ui.run()
