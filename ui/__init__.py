# -*- coding: utf-8 -*-
import os, sys
reload(sys)
sys.setdefaultencoding("utf-8")

from about import *
from main import *
from myapplication import *

script_path = sys.argv[0]
path = os.path.dirname(os.path.abspath(script_path))