"""
Calculates zonal-mean eddy rms of meridional wind on a given model
level for aquaplanet model data
"""

import numpy              as np
import xarray             as xr
from   ds21grl.misc       import get_dim_exp,get_eddy,daysinmonths,get_season_daily
from   ds21grl.read_aqua  import read_xt_ml_daily
from   ds21grl.config     import data_name,dir_raw_aqua,dir_processed

# INPUT -----------------------------------------------------------  
data_name_local = data_name[1:10]
season_name     = ['ANNUAL','NDJFM']
var             = 'V'
level           = 850
ilat            = 70
write2file      = 0
# -----------------------------------------------------------------

for exp in data_name_local:
    for season in season_name:

        print('dataset: ' + exp,',season: ' + season,',var: ' + var)

        # get dimensions
        dim = get_dim_exp(exp)
        
        # define paths
        dir_in  = dir_raw_aqua + exp + '/'
        dir_out = dir_processed + exp + '/'
        
        # read data
        data = read_xt_ml_daily(var,level,ilat,dir_in,dim)

        # get eddies
        data = get_eddy(data,ax=-1)

        # get transients by removing stationary waves
        data_trans = np.zeros((data.shape))
        for m in dim.months:
            if m == 1:
                index = np.arange(0,daysinmonths(m))
            else:
                temp  = np.arange(1,m)
                index = np.arange(np.sum(daysinmonths(temp)),np.sum(daysinmonths(temp)) + daysinmonths(m))

            data_stw = np.sum(data[:,index,:].mean(axis=0),axis=0)/daysinmonths(m)
            for yr in range(0,dim.years.size):
                for i in range(0,index.size):
                    data_trans[yr,index[i],:] = data[yr,index[i],:] - data_stw

        # extract season
        data       = get_season_daily(data,season,ax=1)
        data_trans = get_season_daily(data_trans,season,ax=1)
        
        # calc zonal-mean rms
        rms       = np.mean(np.sqrt(np.mean(data**2,axis=1)),axis=-1)
        rms_trans = np.mean(np.sqrt(np.mean(data_trans**2,axis=1)),axis=-1)
        
        # write to file
        if write2file == 1:
            output = xr.Dataset(data_vars={'rms_eddy':  (('year'), rms.astype(np.float32)),
                                           'rms_trans':  (('year'), rms_trans.astype(np.float32))},
                                coords={'year': dim.years})
            output.rms_eddy.attrs['units']   = 'm/s'
            output.rms_trans.attrs['units']  = 'm/s'
            filename = 'zm_rms_' + var + str(level) + '_ml_' + str(ilat) + 'N_' + season + '_' + dim.timestamp + '.nc'
            output.to_netcdf(dir_out + filename)



