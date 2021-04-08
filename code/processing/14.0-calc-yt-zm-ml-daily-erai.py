"""
Calculates daily zonal-mean yt of a given variable 
on a given model level for reanalysis data
"""

import numpy              as np
import xarray             as xr
from   ds21grl            import dim_erai as dim
from   ds21grl.read_erai  import read_yt_zm_ml_daily
from   ds21grl.write_data import write_yt_zm_ml_daily
from   ds21grl.config     import data_name,dir_raw_erai,dir_processed

# INPUT -----------------------------------------------------------
data_name_local = data_name[0:1]
var_name        = ['T']
level           = 850
write2file      = 0
# ----------------------------------------------------------------- 

for exp in data_name_local:
    for var in var_name:

        print('dataset: ' + exp,', variable: ' + var)

        # define paths                   
        dir_in  = dir_raw_erai
        dir_out = dir_processed + exp + '/'

        # read data           
        data = read_yt_zm_ml_daily(var,level,dir_in,dim)

        # write to file
        write_yt_zm_ml_daily(data,var,level,dir_out,dim,write2file)

 

