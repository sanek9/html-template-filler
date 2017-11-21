#!/bin/python

import imgkit
from tdi import html as _html
from tdi.tools import html as _html_tools

import os
os.chdir(os.path.dirname(os.path.abspath(os.path.normpath(__file__))))

#imgkit.from_url('http://google.com', 'out.jpg')

class Badge(object):

    def __init__(self):
        print "init"

    def render_title(self, node):
        node.content = "Ya ya"

    def render_photo(self, node):
        print "render"
	print node['src']
#	print dir(node)

class Model(object):
    def __init__(self):
        self.scope_menu = Badge()
	
    def render_template(self, node):
	fruits = [
    		u'apples', u'pears', u'bananas', u'pineapples',
	]
	node.repeat(self.repeat_template, fruits, len(fruits) - 2)
	
    def repeat_template(self, node, fruit, last_sep_idx):
	print dir(node.badge.name)
	



tpl = _html.from_files(['layout.html', 'badge.html'])
print dir(tpl)
m = tpl.render_string(Model())
#print m
with open('tmp.html', 'w') as f:
	f.write(m)

options = {
	'width' : '0'
}
#print m
imgkit.from_file('tmp.html', 'out.jpg', options=options)
#imgkit.from_string('Hello!', 'out.jpg')
