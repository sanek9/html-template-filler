#!/bin/python

import imgkit
from tdi import html as _html
from tdi.tools import html as _html_tools

import os
os.chdir(os.path.dirname(os.path.abspath(os.path.normpath(__file__))))

#imgkit.from_url('http://google.com', 'out.jpg')

class Model(object):

    def __init__(self):
        print "init"

    def render_title(self, node):
        node.content = "Ya ya"

    def render_photo(self, node):
        print "render"
	print node['src']
#	print dir(node)

tpl = _html.from_files(['badge.html'])
print dir(tpl)
m = tpl.render_string(Model())
with open('tmp.html', 'w') as f:
	f.write(m)

options = {
	'width' : '10'
}
#print m
imgkit.from_file('tmp.html', 'out.jpg', options=options)
#imgkit.from_string('Hello!', 'out.jpg')
