#! /usr/bin/python3
import  subprocess
import  re
import  sys
sys.path.append(re.sub('\W\w+(\.\w+)?$','',sys.argv[0]))
from ignore_check import *
import tkinter.messagebox as messagebox
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import shutil

from mygui import *

class Core():
    def __init__(self):
        # Creat set, for store ignore files and dirs
        self.ignore = Ignore()

        self.untrack_dirs = []
        self.untrack_files = []
        self.del_lists = []
        self.adding_list = []
        self.untrack_list = []


    def add_to_untrack_list(self,f):
        if os.path.isfile(f):
            self.untrack_files.append(f)
        else:
            self.untrack_dirs.append(f)

    def scan_dirs(self,path='.'):
        c = 0
        """文件搜索，输入搜索路径根目录，路径名称过滤，文件名称过滤"""
        for root, dirs, files in os.walk(path):
            """用正则表达式判断路径名是否匹配"""
            for name in dirs:
                name = os.path.abspath( os.path.join(root, name) )
                self.untrack_dirs.append(name)
                c +=1
            for name in files:
                name = os.path.abspath(os.path.join(root, name))
                self.untrack_files.append(os.path.abspath(name))
                c +=1
        print ("times = %d"%c)

    def find_untrack_file(self):
        ''' 将没有添加到版本库的文件或目录添加到 untrack list'''
        ret = subprocess.getoutput('svn st')
        #print (ret)
        if ret == '':
            return
        svn_msg_list = re.split('\n', ret)
        for line in svn_msg_list:
            print ("--->",line)
            words = re.split('\s\s+',line)
            # 如果是问好，表示该项没有添加到版本库
            if words[0] == '?':
                f = os.path.abspath(words[1])
                if os.path.isfile(f):
                    self.untrack_files.append(f)
                else:
                    if self.ignore.file_is_ignore(f) == False:
                        self.untrack_dirs.append(f)
                        self.scan_dirs(f)

            # 如果是!，表示该项已经被删除
            if line[0] == '!':
                f = words[1]
                self.del_lists.append(f)

    def scan(self):
        self.untrack_dirs = []
        self.untrack_files = []
        self.del_lists = []
        self.find_untrack_file()

        for d in self.untrack_dirs:
            print ('untrack dir >    ',d)
        for f in self.untrack_files:
            print ('untrack file >    ',f)
        for f in self.del_lists:
            print ('Del list >    ',f)

        print ('----------------------------------')
        self.untrack_dirs = self.ignore.find_not_ignore(self.untrack_dirs)
        self.untrack_files = self.ignore.find_not_ignore(self.untrack_files)

        for d in self.untrack_dirs:
            print ('untrack dir >    ',d)
        for f in self.untrack_files:
            print ('untrack file >    ',f)
        for f in self.del_lists:
            print ('Del list >    ',f)


    def add(self):
        s = ''
        for d in self.untrack_dirs:
            ret = subprocess.getoutput('svn add ' + d + ' -N' + ' --force')
            s += ret
        for f in self.untrack_files:
            ret = subprocess.getoutput('svn add ' + f + ' --force')
            self.adding_list.append(f)
            s += ret
        for f in self.del_lists:
            ret = subprocess.getoutput('svn del ' + f + ' --force')
            s += ret
        return s


    def ci(self,msg):
        ret = subprocess.getoutput('svn ci -m ' + msg)
        return (ret)

    def up(self):
        ret = subprocess.getoutput('svn up')
        return (ret)

    def info(self):
        self.status_text.delete(0.0, END)
        ret = subprocess.getoutput('svn info')
        self.status_text.insert(INSERT,ret)

    def del_ignore(self):
        self.status_text.delete(0.0, END)
        ignore_list = []
        for root, dirs, files in os.walk(".", topdown=True):
            pattern = re.compile(r'(\.(svn|git)\b)|(\b__pycache__)')
            for name in dirs:
                name = os.path.abspath( os.path.join(root, name) )
                m = pattern.search(name)
                if m:
                    pass
                else:
                    ignore_list.append(os.path.join(root, name))

            for name in files:
                name = os.path.abspath( os.path.join(root, name) )
                if m:
                    pass
                else:
                    ignore_list.append(os.path.join(root, name))
        ignore_list = self.ignore.find_ignore(ignore_list)

        if len(ignore_list)==0:
            self.status_text.insert(INSERT, 'no ignore file\n')
            return

        for i in ignore_list:
            self.status_text.insert(INSERT, 'delete? :'+ i + '\n')
        self.status_text.update()

        del_all = messagebox.askyesno("delete all?", "Delete all ignore files??")
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
        self.status_text.update()
        if len(untrack_list)==0:
            self.status_text.insert(INSERT, 'no utrack file\n')
            return
        dd = messagebox.askyesno("Delete All?", "If Delete all files?")
        if dd:
            for i in untrack_list:
                if os.path.isdir(i):
                    shutil.rmtree(i)  # 递归删除文件夹
                else:
                    os.remove(i)

if __name__=='__main__':
    SVN = Core()
    msg = 'Tips\n'
    msg += 'scan -- scan untrack files\n'
    msg += 'add -- add to svn\n'
    msg += 'ci -- commit\n'
    msg += 'q -- quit\n'
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
