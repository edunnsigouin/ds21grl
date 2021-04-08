"""
Calculates monthly mean xyt file across several years for 
a given surface (or vertically integrated) variable in 
a given aquaplanet simulation
"""

import numpy            as np
import xarray           as xr
from ds21grl.misc       import get_dim_exp
from ds21grl.read_aqua  import read_xyt_sfc_monthly
from ds21grl.write_data import write_xyt_sfc_monthly
from ds21grl.config     import dir_raw_aqua,dir_processed,data_name

# INPUT -----------------------------------------------------------      
data_name_local = data_name[1:10]
var_name        = ['SST','diabatic_heating'] 
write2file      = 0
# ----------------------------------------------------------------- 

for var in var_name:
    for exp in data_name_local:
        
        print('dataset: ' + exp,', variable: ' + var)

        # get dimensions
        dim = get_dim_exp(exp)
        
        # define paths
        dir_in  = dir_raw_aqua + exp + '/'
        dir_out = dir_processed + exp + '/'
        
        # read data
        data   = read_xyt_sfc_monthly(var,dir_in,dim)
        
        # write to file
        write_xyt_sfc_monthly(data,var,dir_out,dim,write2file)
