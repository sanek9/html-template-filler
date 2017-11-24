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
        self._help = [
                ("s" , "Search in database"),
                ("t" , "Adds to the list by personal numbers"),
                ("p" , "Prints the list"),
                ("d" , "Removes from list"),
                ("m" , "Makes badges"),
                ("q" , "Quit"),
                ("h" , "Prints this help")
            ]
        self.comm = {
                "s" : self.select,
                "t" : self.append,
                "q" : self.quit,
                "d" : self.delete,
                "p" : self.print_list,
                "m" : self.make,
                "h" : self.help
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

            line = raw_input(u"search:> ")
            tmp = self._fetch_persons(conn, u"(s.Family like {0}) or (s.Imya like {0}) or (s.Otch like {0});".format("'%"+line+"%'"))
            
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
                print(u"|{:>4}|{:>20}|{:>20}|{:>20}|{:>70}|{:>70}|".format(person['tab'], person['name'], person['surname'], person['patronymic'], person['post'], person['department']))
        else:
            print(u"List is empty")
            
    def _fetch_persons(self, conn, where):
        cursor = conn.cursor()
        cursor.execute(u"SELECT s.Cod_sostav, s.N_Tab, s.Family, s.Imya, s.Otch, d.Name_dolg, o.Name_otdel \
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
    def delete(self):
        line = raw_input(u"delete tabs:> ")
        if(line is u"all"):
            line = raw_input (u"Are you sure? [y/N]:")
            if(line is u"y"):
                self.persons = []
            return
        
        tabs = line.split(' ')
        tmp = {}
        for tab in tabs:
            if(tab in self.persons):
                tmp[tab]=self.persons[tab]
        
        self._print_persons(tmp)
        line = raw_input ("They are will be deleted, continue? [y/N]:")
        if(line is u"y"):
            for key, val in tmp.items():
               del self.persons[key]

    def _add_to_list(self, tmp={}):
        
        f = True
        
        persons_len = len(self.persons)
        
        line = raw_input(u"tabs:> ")
        if(not line is u"all"):
            tabs = [x for x in line.split(' ') if len(x)==4]
            
        else:
            tabs = tmp.keys()
        ntmp = []
        for tab in tabs:
            if(tab in tmp):
                self.persons[tab] = tmp[tab]
            else:
                ntmp.append(tab)
        
        if(ntmp):
            
            print(u"Load from database...")
            try:
                conn = self.get_connection();
                p = self._fetch_persons(conn, u"s.N_Tab in ({})".format(", ".join([ str(n) for n in ntmp])))
                self.persons.update(p)
            except Error as e:
                print(e)

            finally:
                conn.close()
        
        print(u"{} items added. Total: {}".format(len(self.persons) - persons_len, persons_len))
        
    def _save_photo(self, conn, persons):
        cursor = conn.cursor()
        print(persons)
        print(persons.keys())
        for n in persons.keys():
            print n
        query = u"select s.N_Tab, f.Foto from Tsostav s \
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
        
    def quit(self):
        self._run = False
    
    def run(self):
        self.help()
        while self._run:
            line = raw_input(":> ")
            try:
                self.comm[line]()
            except KeyError as e:
                print (u'Undefined unit: {}'.format(e.args[0]))
                self.help()
    def help(self):
        print(u"Help:")
        for k, v in self._help:
            print(u"{:>10}     {}".format(k,v))

ui = TermUI()
ui.run()
