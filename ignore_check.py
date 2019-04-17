import  os
import  re
import  sys
import chardet
dirs_filter = [
    r'^work$',
    r'\/\..*',

    # quartus
    r'\bdb\b',
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

class   Ignore():
    '''忽略文件检测'''
    def __init__(self):
        self.ignore_files = set()
        self.ignore_dirs = set()

        self.set_default_ignore()
        self.read_ignore_file('.gitignore')
        self.read_ignore_file('.svnignore')

    def set_default_ignore(self):
        for i in dirs_filter:
            self.ignore_dirs.add(re.compile(i))
        for i in files_filter:
            self.ignore_files.add(re.compile(i))

    def inText_read(self,input_file):
        with open(input_file, 'rb') as f:
            f_info = chardet.detect(f.read())
            f_encoding = f_info['encoding']
        with open(input_file, encoding=f_encoding) as inFile:
            inText = inFile.read()
            return inText

    def read_ignore_file(self, file_name):
        if os.path.exists(file_name):
            inText = self.inText_read(file_name)
            fin = re.split('\r?\n',inText)
            #pring(fin)
            while '' in fin:
                fin.remove('')
            #pring(fin)
            for line in fin:
                line = re.sub('\*', '.*', line)
                #pring(line)
                if (line!='') and (line[0]!='#'):
                    if line[-1] == '/':
                        self.ignore_dirs.add(re.compile(line[:-1]))
                    else:
                        self.ignore_files.add(re.compile(line))
            #pring(self.ignore_dirs)
            #pring(self.ignore_files)

    def file_is_ignore(self, f):
        """传入文件或目录，判断是否在忽略列表，如果是忽略，返回True"""
        #pring (f)

        if os.path.isdir(f):
            #pring(f,' is dir')
            for d_filter in self.ignore_dirs:
                m = d_filter.search(f)
                if m:
                    #pring("%s is dir,   #Ignore"%f,d_filter)
                    return True
        elif os.path.isfile(f):
            #pring(f, ' is file')
            basename = os.path.basename(f)
            dirname = os.path.dirname(f)
            for f_filter in self.ignore_files:
                m = f_filter.search(basename)
                if m:
                    #pring("%s is file,   #Ignore"%f,f_filter)
                    return True

            for d_filter in self.ignore_dirs:
                m = d_filter.search(dirname)
                if m:
                    #pring("%s is file, dirname = %s  #Ignore,"%(f,dirname),d_filter)
                    return True
        else:
            #pring(f, ' is string')
            ignore_list = self.ignore_dirs | self.ignore_files
            #pring(self.ignore_dirs)
            #pring(self.ignore_files)
            #pring (ignore_list)
            for d_filter in ignore_list:
                m = d_filter.search(f)
                if m:
                    #pring('ignore unknow>' + f +' # ',d_filter)
                    return True
                #else:
                    #pring ('not match ',f,'  ', d_filter,' ', m)

        #pring (f + ' is not in ignore list')
        return False

    def find_ignore(self,files):
        out_files = []
        for i in files:
            if self.file_is_ignore(i):
                out_files.append(i)
        return out_files

    def find_not_ignore(self,files):
        out_files = []
        for i in files:
            if self.file_is_ignore(i) == False:
                out_files.append(i)
        return out_files
