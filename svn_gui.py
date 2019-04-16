#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import  re
import  sys
sys.path.append(re.sub('\W\w+(\.\w+)?$','',sys.argv[0]))

from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox as messagebox
from  svn_core import *
import shutil
import os

class   GUI(Core):
    def __init__(self):
        super().__init__()

        self.top = Tk()

        self.btnfm=Frame(self.top)
        self.btnfm.pack(fill=X,expand=YES)

        Button(self.btnfm, text='SCAN  ', font=("黑体",16),command=self.btn_scan).grid(row=0, column=0)
        Button(self.btnfm, text='Add   ', font=("黑体",16),command=self.btn_add ).grid(row=1, column=0)
        Button(self.btnfm, text='Commit', font=("黑体",16),command=self.btn_ci  ).grid(row=2, column=0)
        Button(self.btnfm, text='Update', font=("黑体",16),command=self.btn_up  ).grid(row=3, column=0)
        Button(self.btnfm, text='INFO  ', font=("黑体", 16), command=self.info).grid(row=4, column=0)

        Button(self.btnfm, text='DEL->untrack', font=("黑体", 16), command=self.del_untrack).grid(row=5, column=0)
        Button(self.btnfm, text='DEL->ignore', font=("黑体", 16), command=self.del_ignore).grid(row=7, column=0)
        Label(self.btnfm, text='Commit message field', font=("黑体",16)).grid(row=0,column=2,columnspan=1)

        self.ci_text = ScrolledText(self.btnfm,font=("黑体",16),
                                    #width=40,
                                    height=4,
                                    bg='DarkSeaGreen')
        self.ci_text.grid(row=1,rowspan=2,column=1,columnspan=4)
        '''状态区'''
        self.status_text = ScrolledText(self.btnfm,font=("黑体",16),
                                    #width=40,
                                    height=18,
                                    bg='DarkSeaGreen')
        self.status_text.grid(row=4,rowspan=6,column=1,columnspan=5,sticky=N+E+S+W)



        '''commit text display'''
        #self.svn_text = ScrolledText(self.btnfm,font=("黑体",16),
        #                            width=32,height=18,
        #                            bg='DarkSeaGreen')
        #self.svn_text.grid(row=4,rowspan=6,column=5,columnspan=4)

        Button(self.btnfm, text='QUIT', font=("黑体", 16), command=self.top.quit).grid(row=40, column=0)
    def btn_scan(self):
        self.scan()
        self.status_text.delete(0.0,END)
        ret = subprocess.getoutput('svn st')
        if ret != '':
            svn_st = re.split('\n', ret)
            for i in svn_st:
                if self.ignore_check(i) == False:
                    self.status_text.insert(INSERT,i+'\n')

        self.status_text.insert(INSERT,'List will be added\n')
        self.status_text.insert(INSERT, '-'*30 + '\n')
        for i in self.untrack_dirs:
            self.status_text.insert(INSERT,i + '\n')
        for i in self.untrack_files:
            self.status_text.insert(INSERT, '  ' + i + '\n')

    def btn_add(self):
        self.status_text.delete(0.0,END)
        self.status_text.insert(INSERT,self.add())

    def btn_ci(self):
        msg = self.ci_text.get(0.0,END).strip()
        msg = '"' + msg +  '"'
        print (msg)
        if len(msg) != 0:
            self.status_text.insert(INSERT,msg)
            self.status_text.insert(INSERT,'\n\n\n')
            ret = self.ci(msg)
            self.status_text.insert(INSERT,ret)
        else:
            print ("Why you so busy")
            self.status_text.insert(INSERT, 'Why you so busy\n')

    def btn_up(self):
        ret = self.up()
        self.status_text.insert(INSERT,ret)
    def info(self):
        self.status_text.delete(0.0, END)
        ret = subprocess.getoutput('svn info')
        self.status_text.insert(INSERT,ret)

    def del_ignore(self):
        self.status_text.delete(0.0, END)
        ignore_list = []
        for root, dirs, files in os.walk(".", topdown=True):
            pattern = re.compile(r'(\.(svn|git)\b)|(\b__pycache__)')
            #pattern = re.compile(r'\.(svn|git)')
            for name in dirs:
                name = os.path.abspath( os.path.join(root, name) )
                if self.ignore_check(name):
                    m = pattern.search(name)
                    if m:
                        pass
                    else:
                        ignore_list.append(os.path.join(root, name))
                        #self.status_text.insert(INSERT, os.path.join(root, name) + ' is added/\n')
            for name in files:
                name = os.path.abspath( os.path.join(root, name) )
                if self.ignore_check(name):
                    m = pattern.search(name)
                    if m :
                        #self.status_text.insert(INSERT, 'm.group(' + m.group() + ')\n')
                        pass
                    else:
                        ignore_list.append(os.path.join(root, name))

        for i in ignore_list:
            self.status_text.insert(INSERT, i + '\n')

        del_all = messagebox.askyesno("delete all?", "Delete all untrack files??")
        if del_all:
            for i in ignore_list:
                self.status_text.insert(INSERT, 'delect> ' + i + '\n')
                if os.path.isdir(i):
                    shutil.rmtree(i)  # 递归删除文件夹
                else:
                    try:
                        os.remove(i)
                    except:
                        pass
        else:
            del_sig = messagebox.askyesno("delete one?", "Delete one by one??")
            if del_sig:

                for i in ignore_list:
                    del_one = messagebox.askyesno("delete?", "Delete " + i + '?')
                    if del_one:
                        if os.path.isdir(i):
                            shutil.rmtree(i)  # 递归删除文件夹
                        else:
                            try:
                                os.remove(i)
                            except:
                                pass

    def del_untrack(self):
        self.status_text.delete(0.0, END)
        untrack_list = []
        ret = subprocess.getoutput('svn st')
        if ret != '':
            svn_msg_list = re.split('\n', ret)
            for i in svn_msg_list:
                if i[0] == '?':
                    ir = re.split(' \s+',i)[1]
                    self.status_text.insert(INSERT, 'utrack> ' + ir + '\n')
                    untrack_list.append(ir)

        dd = messagebox.askyesno("Delete All?", "If Delete all files?")
        if dd:
            for i in untrack_list:
                if os.path.isdir(i):
                    shutil.rmtree(i)  # 递归删除文件夹
                else:
                    os.remove(i)
if __name__ == '__main__':

    app = GUI()
    mainloop()
