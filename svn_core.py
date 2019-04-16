
import  subprocess
import  os
import  re
import  sys
sys.path.append(re.sub('\W\w+(\.\w+)?$','',sys.argv[0]))

# Creat set, for store ignore files and dirs
ignore_files = set()
ignore_dirs = set()

dirs_filter = [
    r'^work$',
    r'\/\..*',

    # quartus
    r'\Wdb\W',
    r'\bincremental_db\b',
    # Ncverilog
    r'\bINCA_libs\b',
    r'.*\.shm\b',
    # VCS
    r'\bcsrc\b',
    r'\bsimv.daidir\b',
    # Verdi
    r'\bverdiLog\b',

    # Python3
    r'__pycache__',
]

files_filter = [
    r'\bmovdelsim\.ini$',
    r'\..*swp',

    # quartus
    r'.*\.qws$', r'.*\.*\.rpt$', r'.*\.*\.smsg$', r'.*\.jdi$',
    r'.*\.cdf$', r'.*\.done$', r'.*\.map$', r'.*\.summary$',
    # Ncverilog
    r'.*\.key$', r'.*\.ver$',
    r'.*\.log$', r'.*\.fsdb$',
    r'\bsimv$',
    # Keil
    r'.*\.bak$', r'.*\.axf$', r'.*\.lnp$', r'.*\.plg$', r'.*\.sct$',
    r'.*\.uvopt$', r'.*\.Bak$', r'.*\.dep$', r'.*.crf$', r'.*\.d$',
    r'.*\.o$', r'.*\.lst$', r'.*\.uvgui.*$', r'.*\.plg$',
]

#####################################################################################

class Core():
    def __init__(self):
        # Creat set, for store ignore files and dirs
        self.ignore_files = set()
        self.ignore_dirs = set()

        self.untrack_dirs = []
        self.untrack_files = []
        self.del_lists = []
        self.adding_list = []

        self.set_default_ignore()
        self.read_ignore_file('.gitignore')
        self.read_ignore_file('.svnignore')

    def set_default_ignore(self):
        for i in dirs_filter:
            self.ignore_dirs.add(re.compile(i))
        for i in files_filter:
            self.ignore_files.add(re.compile(i))

    # Import ignore list from .gitignore or .svnignore
    def read_ignore_file(self,file_name):
        if os.path.exists(file_name):
            fin = open(file_name, 'rt')
            for line in fin:
                line = line.strip()
                line = re.sub('\*', '.*', line)
                if (line == '') or (line[0] == '#'):
                    continue
                if line[-1] == '/':
                    self.ignore_dirs.add( re.compile(line[:-1]) )
                else:
                    self.ignore_files.add(re.compile(line))

    def ignore_check(self,f):
        """传入文件或目录，判断是否在忽略列表，如果是忽略，返回True"""
        if os.path.isdir(f):
            for d_filter in self.ignore_dirs:
                m = d_filter.search(f)
                if m:
                    print ('\tignore dir')
                    return True
        elif os.path.isfile(f):
            basename = os.path.basename(f)
            dirname = os.path.dirname(f)
            for f_filter in self.ignore_files:
                m = f_filter.search(basename)
                if m:
                    print ('\tignore file> ' + basename)
                    return True

            for d_filter in self.ignore_dirs:
                m = d_filter.search(dirname)
                if m:
                    print ('\tignore dir> ' + dirname)
                    return True
        else:
            ignore_list = self.ignore_dirs | self.ignore_files
            for d_filter in ignore_list:
                m = d_filter.search(f)
                if m:
                    print ('\tignore unknow>' + f)
                    return True
            
        print ('\t Pass')
        return False

    def add_to_untrack_list(self,f):
        if os.path.isfile(f):
            self.untrack_files.append(f)
        else:
            self.untrack_dirs.append(f)

    def scan_dirs(self,path='.'):
        """文件搜索，输入搜索路径根目录，路径名称过滤，文件名称过滤"""
        for root, dirs, files in os.walk(path):
            """用正则表达式判断路径名是否匹配"""
            # 如果根目录不在忽略列表，则添加到版本库，并继续搜索其余文件
            #root = os.path.abspath(root)
            #if self.ignore_check(root) == False:
            #    self.add_to_untrack_list(root)
            #    for f in files:
            #        name = os.path.abspath( os.path.join(root, f) )
            #        if self.ignore_check(name) == False:
            #            self.add_to_untrack_list(name)

            for name in dirs:
                name = os.path.abspath( os.path.join(root, name) )
                if self.ignore_check(name) == False:
                    self.add_to_untrack_list(name)

            for name in files:
                name = os.path.abspath( os.path.join(root, name) )
                if self.ignore_check(name):
                    self.add_to_untrack_list(name)



    def find_untrack_file(self):
        ''' 将没有添加到版本库的文件或目录添加到 untrack list'''
        ret = subprocess.getoutput('svn st')
        print (ret)
        if ret == '':
            return
        svn_msg_list = re.split('\n', ret)
        for line in svn_msg_list:
            print ("--->",line)
            # 如果是问好，表示该项没有添加到版本库

            if line[0] == '?':
                flag, f = re.split('\s\s+', line)
                # 提取出文件名
                # 如果是文件，判断是否是忽略文件，
                # 如果不是忽略文件，直接添加到版本库
                if os.path.isfile(f):
                    if self.ignore_check(f) == False:
                        self.add_to_untrack_list(f)
                else:
                    # 是目录，并且该目录不在忽略列表，则搜索目录下的文件
                    if self.ignore_check(f) == False:
                        self.scan_dirs(f)
            # 如果是!，表示该项已经被删除
            if line[0] == '!':
                flag, f = re.split('\s\s+', line)
                self.del_lists.append(f)

    def scan(self):
        self.untrack_dirs = []
        self.untrack_files = []
        self.del_lists = []
        self.find_untrack_file()

        #for d in self.untrack_dirs:
        #    print ('untrack dir >    ',d)
        #for f in self.untrack_files:
        #    print ('untrack file >    ',f)
        #for f in self.del_lists:
        #    print ('Del list >    ',f)

    def add(self):
        s = ''
        for d in self.untrack_dirs:
            #print ('Adding dir >    ',d)
            ret = subprocess.getoutput('svn add ' + d + ' -N' + ' --force')
            s += ret
        for f in self.untrack_files:
            #print ('Adding file >    ',f)
            ret = subprocess.getoutput('svn add ' + f + ' --force')
            self.adding_list.append(f)
            s += ret
        for f in self.del_lists:
            print ('Del file >    ',f)
            ret = subprocess.getoutput('svn del ' + f + ' --force')
            s += ret
        return s


    def ci(self,msg):
        ret = subprocess.getoutput('svn ci -m ' + msg)
        return (ret)

    def up(self):
        ret = subprocess.getoutput('svn up')
        return (ret)


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
