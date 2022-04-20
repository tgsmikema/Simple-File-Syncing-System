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

for file in dir_list:
    current_f = path.joinpath(file)
    file_list.append(File(current_f))


print(file_list[1].digest)