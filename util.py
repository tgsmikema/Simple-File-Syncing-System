# Author: Siqi Ma
# UPI: sma148

import hashlib
import os
from pathlib import Path
from datetime import datetime


def digest_gen(f_content):
    """parameter: `string` type file content"""
    hashed_string = hashlib.sha256(f_content.encode('utf-8')).hexdigest()
    return hashed_string


def read_file(f_path):
    """parameter: `path` of the file ; return: `string` of file content"""
    text_file = open(f_path, "r")
    data = text_file.read()
    text_file.close()
    return data


def write_to_file(f_path, f_content):
    """parameters: `path` of file, `string` content of message"""
    file = open(f_path, "w")
    success = file.write(f_content)
    file.close()


def get_mod_time_f(f_path):
    """get modification time of a file, return a datetime format."""
    time = os.path.getmtime(f_path)
    time = time.__trunc__()
    dt_time = datetime.fromtimestamp(time)
    dt_time = dt_time.astimezone()
    return dt_time


def convert_dt_to_ts(dt_time):
    return int(dt_time.timestamp())

