import os
from datetime import datetime
import hashlib
import shutil

path = os.getcwd() + "/" + "README.md"

time = os.path.getmtime(path)

time = time.__trunc__()

dt_c = datetime.fromtimestamp(time)

print(dt_c.astimezone())

dt = datetime.fromtimestamp(os.path.getmtime(path))

print(dt)

hashed_string = hashlib.sha256("ssss".encode('utf-8')).hexdigest()
print(hashed_string)

print()
