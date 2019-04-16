import sys
import re

sys.path.append(re.sub('\W\w+(\.\w+)?$','',sys.argv[0]))

from pprint import pprint
pprint(sys.path)
