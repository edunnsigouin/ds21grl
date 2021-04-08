"""
Changes aquaplanet simulation file names to remove experiment name tag, 
e.g., from exp.cam.h1.timestamp.nc to cam.h1.timestamp.nc
"""

import numpy             as np
import xarray            as xr
from ds21grl             import dim_aqua  as dim
from ds21grl.misc        import tic,toc,get_aqua_timestamp
from ds21grl.config      import dir_raw_aqua,data_name
import os

tic()

# INPUT ----------------------------------------------------------- 
exp        = data_name[1]
years      = np.arange(1,51,1)
write2file = 0
# -----------------------------------------------------------------  

for iyear in range(0,years.size):
    for ichunk in range(0,int(365/dim.chunk)):
        
        timestamp = get_aqua_timestamp(years[iyear],ichunk,branch_flag=0)
        print(timestamp)
        
        filename_h1_new = dir_raw_aqua + exp + '/' + 'cam.h1.' + timestamp + '.nc'
        filename_h1_old = dir_raw_aqua + exp + '/' + exp + '.cam.h1.' + timestamp + '.nc'
        filename_h2_new = dir_raw_aqua + exp + '/' + 'cam.h2.' + timestamp + '.nc'
        filename_h2_old = dir_raw_aqua + exp + '/' + exp + '.cam.h2.' + timestamp + '.nc'
        filename_h3_new = dir_raw_aqua + exp + '/' + 'cam.h3.' + timestamp + '.nc'
        filename_h3_old = dir_raw_aqua + exp + '/' + exp + '.cam.h3.' + timestamp + '.nc'
        filename_h4_new = dir_raw_aqua + exp + '/' + 'cam.h4.' + timestamp + '.nc'
        filename_h4_old = dir_raw_aqua + exp + '/' + exp + '.cam.h4.' + timestamp + '.nc'

        if write2file == 1:
            os.rename(filename_h1_old,filename_h1_new)
            os.rename(filename_h2_old,filename_h2_new)
            os.rename(filename_h3_old,filename_h3_new)
            os.rename(filename_h4_old,filename_h4_new)

    for imonth in range(1,13):
        timestamp       = format(years[iyear],"04") + '-' + format(imonth,"02")
        filename_h0_new = dir_raw_aqua + exp + '/' + 'cam.h0.' + timestamp + '.nc'
        filename_h0_old = dir_raw_aqua + exp + '/' + exp + '.cam.h0.' + timestamp + '.nc'

        if write2file == 1:
            os.rename(filename_h0_old,filename_h0_new)

toc()
