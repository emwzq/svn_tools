import  re
import  sys
sys.path.append(re.sub('\W\w+(\.\w+)?$','',sys.argv[0]))

from tkinter import *
from tkinter.scrolledtext import ScrolledText


def cmd():
    print('undefined button command')

def new_cmd():
    print('i am new command!')

class myButton(Frame):
    def __init__(self,master,text,command=cmd,row=0,column=0,rowspan=1,columnspan=1):
        self.name=Button(master, text=text, \
               font=("黑体", 16), \
               command=command)

        self.name.grid(row=row, \
                          rowspan=rowspan,\
                          column=column,\
                          columnspan=columnspan\
                          )
        self.text = text

class myLabel(Frame):
    def __init__(self,master,text,row=0,column=0,rowspan=1,columnspan=1):
        self.name=Label(master, text=text, \
               font=("黑体", 16)
               )
        self.name.grid(row=row, \
                          rowspan=rowspan,\
                          column=column,\
                          columnspan=columnspan\
                          )

class myText(Frame):
    def __init__(self,master,width=32,height=16,row=0,column=0,rowspan=1,columnspan=1):
        self.name = ScrolledText(master,
                                 font=("黑体",16),
                                 width=width,
                                 height=height,
                                    bg='DarkSeaGreen')
        self.name.grid(row=row, \
                          rowspan=rowspan,\
                          column=column,\
                          columnspan=columnspan \
                          )

    def insert(self,LOC,string,end='\n'):
        self.name.insert(LOC, string+end)

    def delete(self,start_loc,end_loc):
        self.name.delete(start_loc, end_loc)





if __name__=='__main__':
    top = Tk()
    #test_button = myButton(top,'测试按钮',new_cmd)
    #test_label  = myLabel (top, '测试Label',row=1,column=1)
    test_text = myText(top,  width=64,height=16,row=1, rowspan=20,column=1,columnspan=20)

    for i in range(20):
        myButton(top,str(i),row=i,column=0)

    for i in range(20):
        myButton(top,str(i),row=0,column=i)
        test_text.insert(INSERT,str(i))

    mainloop()