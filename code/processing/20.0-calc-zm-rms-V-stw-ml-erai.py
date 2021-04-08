"""
Calculates zonal-mean rms of seasonal or annual mean stationary waves using meridional wind on a given model
level for reanalysis data
Note that here stationary waves are defined for every season/year instead of once 
over all years/seasons as is done in the paper.
"""

import numpy              as np
import xarray             as xr
from   ds21grl            import dim_erai as dim
from   ds21grl.misc       import get_eddy,daysinmonths,get_season_daily
from   ds21grl.read_erai  import read_xt_ml_daily
from   ds21grl.config     import data_name,dir_raw_erai,dir_interim

# INPUT ----------------------------------------------------------- 
data_name_local = data_name[0:1]
season_name     = ['ANNUAL','NDJFM']
var             = 'V'
level           = 850
ilat            = 70
write2file      = 0
# -----------------------------------------------------------------    

rms     = np.zeros((len(season_name)))
iseason = 0               
for season in season_name:

    print('season: ' + season,',var: ' + var)

    # define paths 
    dir_in  = dir_raw_erai + '/'
    dir_out = dir_interim + data_name_local[0] + '/'

    # read data
    data = read_xt_ml_daily(var,level,ilat,dir_in,dim)

    # get eddies 
    data = get_eddy(data,ax=-1)

    # extract season 
    data = get_season_daily(data,season,ax=1)
    
    # get stws for each season
    data = data.mean(axis=1)

    # calc zonal-mean rms 
    rms[iseason] = np.mean(np.sqrt(np.mean(data**2,axis=0)),axis=-1)
    iseason      = iseason + 1 
                       
# write to file 
if write2file == 1:
    output = xr.Dataset(data_vars={'rms_stw':  (('season'), rms.astype(np.float32))},
                        coords={'season': np.arange(0,len(season_name))})
    output.rms_stw.attrs['units']   = 'm/s'
    filename = 'zm_rms_' + var + str(level) + '_stw_ml_' + str(ilat) + 'N_' + dim.timestamp + '.nc'
    output.to_netcdf(dir_out + filename)

            
