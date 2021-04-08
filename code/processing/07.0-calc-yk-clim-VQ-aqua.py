"""
Calculates climatological yk of vertically and zonally 
integrated moisture transport for a given aquaplanet simulation
"""

import numpy                 as np
import xarray                as xr
from   ds21grl.misc          import get_dim_exp,get_season_daily,get_season_monthly
from   ds21grl.transportGB16 import write_yk_clim_transport
from   ds21grl.config        import data_name,dir_processed,dir_interim

# INPUT -----------------------------------------------------------      
data_name_local = data_name[1:10]
var             = 'VQ'
flag            = 'eddy'
season_name     = ['ANNUAL']
write2file      = 0
# ----------------------------------------------------------------- 

for exp in data_name_local:
    for season in season_name:
        
        print('dataset: ' + exp, ', season: ' + season)

        # get dimensions 
        dim = get_dim_exp(exp)
        
        # define paths
        dir_in  = dir_processed + exp + '/'
        dir_out = dir_interim + exp + '/'
    
        # read data
        if flag == 'stw':
            filename   = dir_in + 'ykt_zint_vint_ml_monthly_' + var + '_' + flag + '_' + dim.timestamp + '.nc'
            ds         = xr.open_dataset(filename)
            data       = ds[var].values
            ds.close()

            # calculate seasonal mean climatology 
            data  = get_season_monthly(data,season,ax=0)
            data  = data.mean(axis=0)
            
        else:
            filename   = dir_in + 'ykt_zint_vint_ml_daily_' + var + '_' + flag + '_' + dim.timestamp + '.nc'
            ds         = xr.open_dataset(filename)
            data       = ds[var].values
            ds.close()

            # calculate seasonal mean climatology
            data  = get_season_daily(data,season,ax=1)
            data  = data.mean(axis=1).mean(axis=0)

        # write2file
        write_yk_clim_transport(data,var,flag,season,dir_out,dim,write2file)
