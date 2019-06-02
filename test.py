import sys
import re

sys.path.append(re.sub('\W\w+(\.\w+)?$','',sys.argv[0]))

from pprint import pprint
pprint(sys.path)


class   myTest():
    def __init__(self):
        self.top = ''
        self.tc = ''

    #def assign(self,a,b):
    #    getattr(self,a) = b

#App = Test()

#App.assign('top','while')

#print (self.top)
