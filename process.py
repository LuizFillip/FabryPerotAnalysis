from core import FabryPerot
import os 
import datetime as dt
from utils import file_attrs, datetime_to_float 
import pandas as pd
    
    
def running_avg(df, 
                Dir = "zonal", 
                sample = "30min"):
    
    coords = {"zon": ("west", "east"), 
             "mer": ("north", "south")}
    
    up, down = coords[Dir] 

    fp = df.loc[(df["dir"] == up) | 
                (df["dir"] == down), "vnu"]
    
    chunk = fp.resample(sample).mean().to_frame()
    
    return chunk.rename(columns = {"vnu": Dir})

def concat_dir(df):
    
    out = []
    for coord in ["zon", "mer"]:
        out.append(running_avg(df, Dir = coord))
    f = pd.concat(out, axis = 1)
    f.index.name = "time"
    return f



def run_for_all_days(infile, save = True):
    
    _, _, files = next(os.walk(infile))

    out = []
    
    for filename in files:
    
        date = file_attrs(filename).date
        print("processing...", date)
        fp = FabryPerot(infile + filename).wind
        out.append(concat_dir(fp))
     
    df = pd.concat(out)
    if save:
        df.to_csv("database/processed_2013.txt", index = True)
    return df



def main():
    infile = "database/2013/"

    df = run_for_all_days(infile)
    

