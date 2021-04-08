"""
Calculates yt correlation of a zonally averaged variable at a given level with
vertically and zonally integrated eddy moisture transport at a given latitude.
Significance following Ebisuzaki 97 JCLIM.

NOTE: significance code is slow. Best to calculate one variable/wavenumber range at a time.
"""                                                                 

import numpy             as np
import xarray            as xr
from  ds21grl.misc       import get_dim_exp,get_anomaly_daily_seasonal_cycle,tic,toc
from ds21grl.ebisuzaki97 import cross_correlate_ndim_sig,write_yt_daily
from ds21grl.config      import data_name,dir_processed,dir_interim

# INPUT ----------------------------------------------------------- 
data_name_local  = data_name[1:2]                                # data set names
var_name         = ['T850_ml','FLDS_sfc','LWCFS_sfc']            # variable names and type of vertical level of zonal-mean data
k_range          = np.array([[1,40],[1,3],[4,40]])               # select wavenumber range for moisture transport 
ilat             = 70                                            # latitude of transport for correlation
maxlag           = 10                                            # max +- days for lag correlation
sigthresh        = 99                                            # threshold of significance
nbs              = 5000                                          # number of bootstrapped samples for significance
write2file       = 0
# -----------------------------------------------------------------

for exp in data_name_local:
    for var in var_name:
        for k in range(0,k_range.shape[0]):
        
            print('dataset: ' + exp,',variable: ' + var,',wavenumber range: ' + \
                  str(k_range[k,0]) + '-' + str(k_range[k,-1]))

            # get dimensions
            dim = get_dim_exp(exp)
            
            # define paths
            dir_in  = dir_processed + exp + '/'
            dir_out = dir_interim + exp + '/'

            # read moisture transport data
            filename = dir_in + 'ykt_zint_vint_ml_daily_VQ_eddy_' + dim.timestamp + '.nc'
            waves    = dim.wavenumber[k_range[k,0]:k_range[k,-1]+1]
            ds       = xr.open_dataset(filename).sel(lat=ilat,wavenumber=waves,method='nearest').sum(dim='wavenumber')
            data1    = ds['VQ'].values
            ds.close()

            # read zonal-mean data
            filename = dir_in + 'yt_zm_daily_' + var + '_' + dim.timestamp + '.nc'
            data2    = xr.open_dataarray(filename).values

            # get anomalies relative to daily-mean seasonal cycle
            data1 = get_anomaly_daily_seasonal_cycle(data1,dim)
            data2 = get_anomaly_daily_seasonal_cycle(data2,dim)

            # calculate correlation + significance for all lags at each latitude
            data1 = np.squeeze(np.reshape(data1,(dim.nday*dim.years.size,1)))                                                       
            data2 = np.reshape(data2,(dim.nday*dim.years.size,dim.lat.size))
            corr  = np.zeros([2*maxlag+1,dim.lat.size])         
            sig   = np.zeros([2*maxlag+1,dim.lat.size])
            lag   = np.zeros([2*maxlag+1])
            for j in range(0,dim.lat.size):
                print('latitude: ' + str(dim.lat[j]))
                tic()                                                                                  
                [corr[:,j],sig[:,j],lag] = cross_correlate_ndim_sig(data1,data2[:,j],maxlag,nbs,sigthresh,ax=0) 
                toc()
        
            # write 2 file
            string1  = 'VQ_k' + str(waves[0]) + '-' + str(waves[-1]) + '_' + str(ilat) + 'N'
            string2  = 'with_zm_' + var
            filename = 'yt_corr_nbs' + str(nbs) + '_' + string1 + '_' + string2 + '_' + dim.timestamp + '.nc'
            write_yt_daily(corr,sig,lag,filename,dir_out,dim,write2file)

