"""
Calculates daily zonal-mean yt of a given variable 
on a given model level for an aquaplanet simulation
"""

import numpy              as np
import xarray             as xr
from   ds21grl.misc       import get_dim_exp
from   ds21grl.read_aqua  import read_yt_zm_ml_daily
from   ds21grl.write_data import write_yt_zm_ml_daily
from   ds21grl.config     import data_name,dir_raw_aqua,dir_processed

# INPUT -----------------------------------------------------------       
data_name_local = data_name[1:10]
var_name        = ['T','Q']
level           = 850
write2file      = 0
# -----------------------------------------------------------------  

for exp in data_name_local:
    for var in var_name:

        print('dataset: ' + exp,', variable: ' + var)

        # get dimensions
        dim = get_dim_exp(exp)
        
        # define paths 
        dir_in  = dir_raw_aqua + exp + '/'
        dir_out = dir_processed + exp + '/'

        # read data
        data = read_yt_zm_ml_daily(var,level,dir_in,dim)

        # write to file     
        write_yt_zm_ml_daily(data,var,level,dir_out,dim,write2file)



