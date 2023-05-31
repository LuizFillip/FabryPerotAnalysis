import matplotlib.pyplot as plt
import FabryPerot as fp
import os
import settings as s
import pandas as pd
import models as m




def plot_directions(
        ax, 
        path, 
        parameter = "vnu"
        ):
    
    if parameter == "vnu":
        df = fp.FPI(path).wind
    else:
        df = fp.FPI(path).temp
        
    coords = {
        "zon": ("east", "west"), 
        "mer": ("north", "south")
        }
    
    names = ["zonal", "meridional"]
    
        
    args = dict(marker = "s",
                lw = 2, 
                fillstyle = "none")
    
    for i, coord in enumerate(coords.keys()):
        
        # mean = fp.process_day(path).resample("10min").mean()
        
        # ax[i].plot(mean[coord], **args, label = "Média (10 min)")
        
        # for alt in [250, 300, 350]:
        ds = m.load_hwm(df, alt = 250, site = "car")
        
        ax[i].plot(ds[coord], lw = 2, label = "HWM-14 (250 km)")
        
        for direction in coords[coord]:
            
            ds = df.loc[(df["dir"] == direction)]
            
            ax[i].errorbar(
                ds.index, 
                ds[parameter], 
                yerr = ds[f"d{parameter}"], 
                label = direction, 
                capsize = 5
                )
        ax[i].legend(loc = "lower left", ncol = 3)
        ax[i].set(ylabel = f"Vento {names[i]} (m/s)", 
                  ylim = [-200, 200])
        ax[i].axhline(0, color = "k", linestyle = "--")




def plot_nighttime_observation(
        path, 
        parameter = "vnu"
        ):
    
    fig, ax = plt.subplots(nrows = 2, 
                           figsize = (10, 8), 
                           sharex = True, 
                           sharey = True, 
                           dpi = 300)
    
    plt.subplots_adjust(hspace = 0.1)
    
    
    plot_directions(ax, path, parameter = parameter)
    
    s.format_time_axes(
            ax[1], hour_locator = 1, 
            day_locator = 1, 
            tz = "UTC"
            )
    
    if "car" in path:    
        ax[0].set_title("Cariri")
    else:
        ax[0].set_title("Cajazeiras")
   
    return fig
        
def main():
    
    infile = "database/FabryPerot/2013/"
    files = os.listdir(infile)

    filename = files[2]
    path = os.path.join(infile, filename)
    path = 'database/FabryPerot/2012/minime01_car_20130318.cedar.005.txt'
    #path = 'database/FabryPerot/caj/minime02_caj_20130415.cedar.004.hdf5.txt'
    fig = plot_nighttime_observation(path)
    
    fig.savefig("FabryPerot/figures/20130318.png", dpi = 300)



# main()