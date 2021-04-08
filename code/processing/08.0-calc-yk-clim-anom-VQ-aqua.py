"""
Calculates anomalous climatological yk of vertically and zonally 
integrated moisture transport for a given aquaplanet simulation
relative to the control simulation.

NOTE: doesn't work for stationary wave component, only eddies and 
transients
"""

import numpy               as np
import xarray              as xr
from scipy                 import stats
from ds21grl.transportGB16 import write_yk_clim_anom_transport
from ds21grl.misc          import get_dim_exp,get_season_daily
from ds21grl.config        import dir_processed,dir_interim,data_name

# INPUT -----------------------------------------------------------  
data_name_local = data_name[2:10]
var             = 'VQ'
flag            = 'eddy' 
season_name     = ['ANNUAL','NDJFM']
write2file      = 0
# -----------------------------------------------------------------

for exp in data_name_local:
    for season in season_name:

        print('dataset: ' + exp,', season: ' + season)

        # get dimensions        
        dim     = get_dim_exp(exp)
        dim_ctl = get_dim_exp(data_name[1])
        
        # define paths                                                         
        dir_in_exp = dir_processed + exp + '/'
        dir_in_ctl = dir_processed + data_name[1] + '/'
        dir_out    = dir_interim + exp + '/'

        # read data 
        filename   = dir_in_exp + 'ykt_zint_vint_ml_daily_' + var + '_' + flag + '_' + dim.timestamp + '.nc'
        ds         = xr.open_dataset(filename)
        data       = ds[var].values
        ds.close()

        # read control data
        filename   = dir_in_ctl + 'ykt_zint_vint_ml_daily_' + var + '_' + flag + '_' + dim_ctl.timestamp + '.nc'
        ds         = xr.open_dataset(filename)
        data_ctl   = ds[var].values
        ds.close()

        # get seasonal days and average experiment for each year 
        data      = get_season_daily(data,season,ax=1)
        data_ctl  = get_season_daily(data_ctl,season,ax=1)
        data      = data.mean(axis=1)

        # get control climatology
        data_ctl  = data_ctl.mean(axis=1).mean(axis=0)

        # get significance of anomalies &       
        # flag pvalues less that 5%                                                                                              
        for yr in range(0,dim.years.size):
            data[yr,:] = data[yr,:] - data_ctl[:]
        [tstat,sig]  = stats.ttest_1samp(data,0,axis=0)
        index1       = sig <= 0.05
        index2       = sig > 0.05
        sig[index1]  = 0
        sig[index2]  = 1

        # define clim anomaly and normalize by control clim 
        data = 100*(data.mean(axis=0)/data_ctl)

        # write2file                                                                                         
        write_yk_clim_anom_transport(data,sig,var,flag,season,dir_out,dim,write2file)

