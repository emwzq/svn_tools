#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import  re
import  sys
sys.path.append(re.sub('\W\w+(\.\w+)?$','',sys.argv[0]))

from tkinter import *
from tkinter.scrolledtext import ScrolledText

from  svn_core import *
from mygui import *


class   GUI(Core):
    def __init__(self):
        super().__init__()

        self.top = Tk()

        self.btnfm=Frame(self.top)
        self.btnfm.pack(fill=X,expand=YES)

        myButton(self.btnfm, text='CheckOut', command=self.checkout,row=1, column=0)
        self.ci_text = myText(self.btnfm,height=1,row=1,rowspan=1,column=1,columnspan=16)

        myButton(self.btnfm, text='SCAN  ', command=self.btn_scan,row=2, column=0)
        myButton(self.btnfm, text='Add   ', command=self.btn_add ,row=3, column=0)
        myButton(self.btnfm, text='Commit', command=self.btn_ci  ,row=4, column=0)
        myButton(self.btnfm, text='Update', command=self.btn_up  ,row=5, column=0)
        myButton(self.btnfm, text='INFO  ', command=self.info    ,row=6, column=4)

        myButton(self.btnfm, text='DEL->untrack',command=self.del_untrack,row=7, column=0)
        myButton(self.btnfm, text='DEL->ignore ',command=self.del_ignore ,row=8, column=0)

        myLabel(self.btnfm, text='Commit message field',row=2,column=1,columnspan=1)
        self.ci_text = myText(self.btnfm,height=4,row=3,rowspan=2,column=1,columnspan=4)

        '''状态区'''
        self.status_text = myText(self.btnfm,height=18,row=4,rowspan=16,column=1,columnspan=16)
        myButton(self.btnfm, text='QUIT  ', command=self.top.quit, row=40, column=0)

    def checkout(self):
        pass

    def btn_scan(self):
        self.scan()
        self.status_text.delete(0.0,END)

        if (len(self.untrack_dirs)==0) and (len(self.untrack_files)==0):
            self.status_text.insert(INSERT, 'No file needed add to repository!\n')
        else:
            for i in self.untrack_dirs:
                self.status_text.insert(INSERT, 'New Dir : ' + i + '\n')
            for i in self.untrack_files:
                self.status_text.insert(INSERT, 'New File: ' + i + '\n')

    def btn_add(self):
        self.status_text.delete(0.0,END)
        self.status_text.insert(INSERT,self.add())

    def btn_ci(self):
        msg = self.ci_text.get(0.0,END).strip()
        msg = '"' + msg +  '"'
        print (msg)
        if len(msg) != 0:
            self.status_text.insert(INSERT,msg)
            self.status_text.insert(INSERT,'\n\n')
            ret = self.ci(msg)
            self.status_text.insert(INSERT,ret)
        else:
            self.status_text.insert(INSERT, 'Why are you so busy\n')

    def btn_up(self):
        self.status_text.insert(INSERT,self.up())


if __name__ == '__main__':

    app = GUI()
    mainloop()
