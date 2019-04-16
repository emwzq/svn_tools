#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import  re
import  sys
sys.path.append(re.sub('\W\w+(\.\w+)?$','',sys.argv[0]))


from tkinter import *
from  svn_core import *
from  svn_gui import *


if __name__ == '__main__':

    if len(sys.argv) == 1:
        SVN = Core()
        msg = 'Tips\n'
        msg += 'scan -- scan untrack files\n'
        msg += 'add -- add to svn\n'
        msg += 'ci -- commit'
        while True:
            print (msg)
            inp = input('svn>>')
            inps = re.split('\s+',inp)
            if hasattr(SVN,inps[0]):
                if len(inps) == 1:
                    getattr(SVN,inps[0])()
                else:
                    c = ' '.join(inps[1:])
                    getattr(SVN,inps[0])(inps[1])
            elif inp=='q':
                exit()
            else:
                print ('unknow')
    elif sys.argv[1] == 'gui':
        app = GUI()
        mainloop()
