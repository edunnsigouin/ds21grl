"""
Calculates anomalous monthly mean climatology xy file for a given surface 
(or vertically integrated) variable in a given aquaplanet simulation.
Anomalies are defined relative to the control simulation.
"""

import numpy            as np
import xarray           as xr
from scipy              import stats
from ds21grl.write_data import write_xy_sfc_clim_anom
from ds21grl.misc       import get_dim_exp,get_season_monthly
from ds21grl.config     import dir_processed,dir_interim,data_name

# INPUT -----------------------------------------------------------      
data_name_local = data_name[2:10]
var_name        = ['SST']
season_name     = ['ANNUAL']
write2file      = 0
# ----------------------------------------------------------------- 

for var in var_name:
    for exp in data_name_local:
        for season in season_name:

            print('dataset: ' + exp,', variable: ' + var,', season: ' + season)

            # get dimensions
            dim     = get_dim_exp(exp)
            dim_ctl = get_dim_exp(data_name[1])
            
            # define paths                   
            dir_in_exp = dir_processed + exp + '/'
            dir_in_ctl = dir_processed + data_name[1] + '/'
            dir_out    = dir_interim + exp + '/'
            
            # read experiment data                   
            filename    = dir_in_exp + 'xyt_sfc_monthly_' + var + '_' + dim.timestamp + '.nc'
            ds          = xr.open_dataset(filename)
            data        = ds[var].values
            ds.close()

            # read control data
            filename    = dir_in_ctl + 'xyt_sfc_monthly_' + var + '_' + dim_ctl.timestamp + '.nc'
            ds          = xr.open_dataset(filename)
            data_ctl    = ds[var].values
            ds.close()
            
            # get seasonal months and average experiment for each year
            data      = get_season_monthly(data,season,ax=1)
            data_ctl  = get_season_monthly(data_ctl,season,ax=1)
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
            
            # clim anomaly 
            data = data.mean(axis=0)

            # write 2 file
            write_xy_sfc_clim_anom(data,sig,var,season,dir_out,dim,write2file)
