"""
Calculates monthly mean climatology xy file for a given surface 
(or vertically integrated) variable in a given aquaplanet simulation.
"""

import numpy            as np
import xarray           as xr
from ds21grl.write_data import write_xy_sfc_clim
from ds21grl.misc       import get_dim_exp,get_season_monthly
from ds21grl.config     import dir_processed,dir_interim,data_name

# INPUT -----------------------------------------------------------      
data_name   = data_name[2:10]
var_name    = ['diabatic_heating']
season_name = ['ANNUAL']
write2file  = 0
# ----------------------------------------------------------------- 

for var in var_name:
    for exp in data_name:
        for season in season_name:

            print('dataset: ' + exp,', variable: ' + var,', season: ' + season)

            # get dimensions
            dim = get_dim_exp(exp)
        
            # define paths
            dir_in  = dir_processed + exp + '/'
            dir_out = dir_interim + exp + '/'
        
            # read data
            filename    = dir_in + 'xyt_sfc_monthly_' + var + '_' + dim.timestamp + '.nc'
            ds          = xr.open_dataset(filename)
            data        = ds[var].values
            ds.close()

            # seasonal mean
            data  = get_season_monthly(data,season,ax=1)
            data  = data.mean(axis=0).mean(axis=0)

            # write to file
            write_xy_sfc_clim(data,var,season,dir_out,dim,write2file)
