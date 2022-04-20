import os
import util


class File:

    def __init__(self, posix_path):
        self.posix_path = posix_path
        self.file_name = os.path.basename(posix_path)
        self.mod_time_str = util.get_f_mod_time_string(posix_path)
        self.mod_time_dt = util.get_f_mod_time(posix_path)
        self.digest = util.gen_digest(util.read_file(posix_path))
        self.mod_time_tstamp = util.convert_dt_to_ts(self.mod_time_dt)

