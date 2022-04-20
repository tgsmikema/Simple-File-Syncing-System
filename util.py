# Author: Siqi Ma
# UPI: sma148

import hashlib
import os
from pathlib import Path
from datetime import datetime


def gen_digest(f_content):
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


def get_f_mod_time(f_path):
    """get modification time of a file, return a datetime format."""
    time = os.path.getmtime(f_path)
    time = time.__trunc__()
    dt_time = datetime.fromtimestamp(time)
    dt_time = dt_time.astimezone()
    return dt_time


def set_f_mod_time(f_path, dt_time):
    dt_mod_time = dt_time.timestamp()
    os.utime(f_path, (dt_mod_time, dt_mod_time))


def convert_dt_to_ts(dt_time):
    return int(dt_time.timestamp())


def get_mod_time_string(f_path):
    dt_time = get_f_mod_time(f_path)
    dt_string = dt_time.strftime("%Y-%m-%d %H:%M:%S %z")
    return dt_string


def convert_mod_str_to_dt(dt_str):
    dt_obj = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S %z')
    return dt_obj


def gen_f_status_list(f_path):
    """generate file status list including """
    status_list = [get_mod_time_string(f_path), gen_digest(read_file(f_path))]
    return status_list
