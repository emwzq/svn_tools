from ignore_check import *


I = Ignore()
'''
I.read_ignore_file('test_data.txt')

I.file_is_ignore('test_ignroe_check.py')
I.file_is_ignore('db')
I.file_is_ignore('verilog.log')
I.file_is_ignore('db/test.log')
'''
a = ['abc','db','123456','qwerty']
print (I.find_ignore(a) )
print (I.find_not_ignore(a) )
#I.file_is_ignore('db')