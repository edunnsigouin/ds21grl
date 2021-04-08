"""
Renames files from an aquaplanet branch run so that 
they have timestamp that starts on day 1 and year 1 
instead of day 2 and year 51 
"""

import numpy             as np
import xarray            as xr
from ds21grl             import dim_aqua  as dim
from ds21grl.misc        import tic,toc,get_aqua_timestamp
from ds21grl.config      import dir_raw_aqua,data_name
import os            

tic()

# INPUT -----------------------------------------------------------       
exp        = data_name[0]
years_new  = np.arange(1,51,1)
years_old  = np.arange(51,101,1)
write2file = 0
# -----------------------------------------------------------------  

for iyear in range(0,years_new.size):
    for ichunk in range(0,int(365/dim.chunk)):
        
        timestamp_new   = get_aqua_timestamp(years_new[iyear],ichunk,branch_flag=0)
        timestamp_old   = get_aqua_timestamp(years_old[iyear],ichunk,branch_flag=1)

        #print(timestamp_new,' ',timestamp_old)
        
        filename_h1_new = dir_raw_aqua + exp + '/' + exp + '.cam.h1.' + timestamp_new + '.nc'
        filename_h1_old = dir_raw_aqua + exp + '/' + exp + '.cam.h1.' + timestamp_old + '.nc'
        filename_h2_new = dir_raw_aqua + exp + '/' + exp + '.cam.h2.' + timestamp_new + '.nc'
        filename_h2_old = dir_raw_aqua + exp + '/' + exp + '.cam.h2.' + timestamp_old + '.nc'
        filename_h3_new = dir_raw_aqua + exp + '/' + exp + '.cam.h3.' + timestamp_new + '.nc'
        filename_h3_old = dir_raw_aqua + exp + '/' + exp + '.cam.h3.' + timestamp_old + '.nc'
        filename_h4_new = dir_raw_aqua + exp + '/' + exp + '.cam.h4.' + timestamp_new + '.nc'
        filename_h4_old = dir_raw_aqua + exp + '/' + exp + '.cam.h4.' + timestamp_old + '.nc'

        if write2file == 1:
            os.rename(filename_h1_old,filename_h1_new)
            os.rename(filename_h2_old,filename_h2_new)
            os.rename(filename_h3_old,filename_h3_new)
            os.rename(filename_h4_old,filename_h4_new)

    for imonth in range(1,13):
        timestamp_new   = format(years_new[iyear],"04") + '-' + format(imonth,"02")
        timestamp_old   = format(years_old[iyear],"04") + '-' + format(imonth,"02")

        #print(timestamp_new,' ',timestamp_old)
        
        filename_h0_new = dir_raw_aqua + exp + '/' + exp + '.cam.h0.' + timestamp_new + '.nc'
        filename_h0_old = dir_raw_aqua + exp + '/' + exp + '.cam.h0.' + timestamp_old + '.nc'

        if write2file == 1:
            os.rename(filename_h0_old,filename_h0_new)

toc()

