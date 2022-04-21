import os
from datetime import datetime
import shutil
import json
from pathlib import Path
import sys
import util
from file import File

path = Path("dir1")
dir_list = os.listdir(path)
file_list = []
dictdict = {"11": "2", "22": "222"}

print(dictdict.keys().__contains__("114"))

# util.sync_dir_and_sub_dir_no_files('dir1', 'dir2')

# sss = Path("dir1/777/hhhh/8888")
#
# print(util.get_head_of_path_no_slash(sss))
# print(util.get_tail_of_path_begin_slash(sss))
