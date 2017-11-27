#!/bin/python

import imgkit
import pdfkit
from tdi import html as _html
from tdi.tools import html as _html_tools
import mysql.connector
from mysql.connector import Error

import os
os.chdir(os.path.dirname(os.path.abspath(os.path.normpath(__file__))))

#imgkit.from_url('http://google.com', 'out.jpg')



class Model(object):
    def __init__(self, objects, func):
        self.objects = objects
        self.func = func

    def render_layout(self, node):
#        print (type(self.objects))
#        print(self.objects)
        node.repeat(self.repeat_layout, self.objects, len(self.objects) - 2)

    def repeat_layout(self, node, obj, last_sep_idx):
        self.func(node.template, obj)
	

class BadgeBuilder(object):
    def _func(self, node, key):
#        print (type(person))
#        print(person)
        person = self.persons[key]
        node.name.content = person['name']
        node.surname.content = person['surname']
        node.patronymic.content = person['patronymic']
        node.post.content = person['post']
        node.department.content = person['department']
 #       print(person['photo'])
        node.photo['src'] = person['photo']
    
    def make(self, persons, out):
        self.persons = persons
#        print (type(persons))
#        print(persons)
        tpl = _html.from_files(['layout.html', 'badge.html'])
#        print dir(tpl)
        m = tpl.render_string(Model(persons, self._func))
#        print m
        with open('tmp.html', 'w') as f:
            f.write(m)

        options = {
        #	'format': 'png'
        #	'width' : '0'
        }


        pdfkit.from_file('tmp.html', 'out.pdf', options=options)


#imgkit.from_string('Hello!', 'out.jpg')
