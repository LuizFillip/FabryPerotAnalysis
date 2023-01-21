import os
import datetime as dt


def get_endswith_extension(infile, 
                           extention = ".txt"):
    _, _, files = next(os.walk(infile))
    txt_files = []
    for filename in files:
        if filename.endswith(extention):
            txt_files.append(filename)
    
    return txt_files


def monthToNum(shortMonth):
    return {
        'jan': 1,
        'fev': 2,
        'mar': 3,
        'abr': 4,
        'mai': 5,
        'jun': 6,
        'jul': 7,
        'ago': 8,
        'set': 9, 
        'out': 10,
        'nov': 11,
        'dez': 12
        }[shortMonth]


class file_attrs(object):
    
    def __init__(self, filename):
        
        s = filename.split('_')
        obs_list = s[-1].split('.')
        
        self.intr = s[0]
        self.site = s[1]
        self.number = obs_list[1]
        
        date_str = obs_list[0]
        self.date = dt.datetime.strptime(date_str, "%Y%m%d")
    
   