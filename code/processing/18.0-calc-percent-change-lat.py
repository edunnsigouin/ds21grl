"""
Calculates postprocessed data for fig 03c and fig S4c. 
Specifically, the script calculates the percent change from 
the control simulation of various quantities at a given latitude:
1) vertically and meridionally integrated eddy moisture transport
2) vertically and meridionally integrated transient eddy moisture transport
3) zonal-mean specific humidity at 850hPa
4) zonal-mean temperature at 850hPa mulitplied by Clausius-Clapeyron rate
calculated from the control run
5) zonal-mean V eddy rms at 850 hPa
6) zonal-mean V transient eddy rms at 850 hPa 
"""

import numpy           as np
import xarray          as xr
from scipy             import stats
from   ds21grl         import const
from ds21grl.misc      import get_dim_exp,get_season_daily
from ds21grl.config    import dir_processed,dir_interim,data_name

# INPUT -----------------------------------------------------------      
data_name_local = data_name[2:10]
season_name     = ['ANNUAL','NDJFM']
k_range         = np.arange(1,41,1)
ilat            = 70
write2file      = 0
# ----------------------------------------------------------------- 

# initialize output array
MN  = np.zeros((6,len(data_name_local),len(season_name)))
STD = np.zeros((6,len(data_name_local),len(season_name)))

iexp    = 0
for exp in data_name_local:
    iseason = 0
    for season in season_name:

        print('dataset: ' + exp,', season: ' + season)

        # get dimensions
        dim     = get_dim_exp(exp)
        dim_ctl = get_dim_exp(data_name[1])
        
        # define paths                                                                                                                  
        dir_in_exp = dir_processed + exp + '/'
        dir_in_ctl = dir_processed + data_name[1] + '/'
            
        # 1) calculate percentage change of eddy and transient eddy moisture transport

        # read exp and control data
        filename1    = dir_in_exp + 'ykt_zint_vint_ml_daily_VQ_eddy_' + dim.timestamp + '.nc'
        filename2    = dir_in_exp + 'ykt_zint_vint_ml_daily_VQ_trans_' + dim.timestamp + '.nc'
        filename3    = dir_in_ctl + 'ykt_zint_vint_ml_daily_VQ_eddy_' + dim_ctl.timestamp + '.nc'
        filename4    = dir_in_ctl + 'ykt_zint_vint_ml_daily_VQ_trans_' + dim_ctl.timestamp + '.nc'
        ds1          = xr.open_dataset(filename1).sel(lat=ilat,wavenumber=k_range,method='nearest').sum(dim='wavenumber')
        ds2          = xr.open_dataset(filename2).sel(lat=ilat,wavenumber=k_range,method='nearest').sum(dim='wavenumber')
        ds3          = xr.open_dataset(filename3).sel(lat=ilat,wavenumber=k_range,method='nearest').sum(dim='wavenumber')
        ds4          = xr.open_dataset(filename4).sel(lat=ilat,wavenumber=k_range,method='nearest').sum(dim='wavenumber')
        VQ_eddy      = ds1['VQ'].values
        VQ_trans     = ds2['VQ'].values
        VQ_eddy_ctl  = ds3['VQ'].values
        VQ_trans_ctl = ds4['VQ'].values
        ds1.close()
        ds2.close()
        ds3.close()
        ds4.close()

        # get season
        VQ_eddy      = get_season_daily(VQ_eddy,season,ax=1)
        VQ_trans     = get_season_daily(VQ_trans,season,ax=1)
        VQ_eddy_ctl  = get_season_daily(VQ_eddy_ctl,season,ax=1)
        VQ_trans_ctl = get_season_daily(VQ_trans_ctl,season,ax=1)

        # get seasonal-means for each year 
        VQ_eddy  = VQ_eddy.mean(axis=1)
        VQ_trans = VQ_trans.mean(axis=1)

        # get control climatology
        VQ_eddy_ctl  = VQ_eddy_ctl.mean(axis=1).mean(axis=0)
        VQ_trans_ctl = VQ_trans_ctl.mean(axis=1).mean(axis=0)

        # get yearly anomalies relative to control clim
        # and normalize 
        VQ_eddy  = 100*(VQ_eddy - VQ_eddy_ctl)/VQ_eddy_ctl
        VQ_trans = 100*(VQ_trans - VQ_trans_ctl)/VQ_trans_ctl


        
        # 2) calculate percent change in specific humidity and expected
        # change based on local C-C temperature change

        # read exp and control data   
        filename1    = dir_in_exp + 'yt_zm_daily_Q850_ml_' + dim.timestamp + '.nc'
        filename2    = dir_in_exp + 'yt_zm_daily_T850_ml_' + dim.timestamp + '.nc'
        filename3    = dir_in_ctl + 'yt_zm_daily_Q850_ml_' + dim_ctl.timestamp + '.nc'
        filename4    = dir_in_ctl + 'yt_zm_daily_T850_ml_' + dim_ctl.timestamp + '.nc'
        ds1          = xr.open_dataset(filename1).sel(lat=ilat,method='nearest')
        ds2          = xr.open_dataset(filename2).sel(lat=ilat,method='nearest')
        ds3          = xr.open_dataset(filename3).sel(lat=ilat,method='nearest')
        ds4          = xr.open_dataset(filename4).sel(lat=ilat,method='nearest')
        Q            = ds1['Q'].values
        T            = ds2['T'].values
        Q_ctl        = ds3['Q'].values
        T_ctl        = ds4['T'].values
        ds1.close()
        ds2.close()
        ds3.close()
        ds4.close()

        # get season
        Q     = get_season_daily(Q,season,ax=1)
        T     = get_season_daily(T,season,ax=1)
        Q_ctl = get_season_daily(Q_ctl,season,ax=1)
        T_ctl = get_season_daily(T_ctl,season,ax=1)

        # get seasonal-means for each year
        Q = Q.mean(axis=1)
        T = T.mean(axis=1)

        # get control climatology
        Q_ctl = Q_ctl.mean(axis=1).mean(axis=0)
        T_ctl = T_ctl.mean(axis=1).mean(axis=0)

        # get yearly anomalies relative to control clim 
        # and normalize                                                                                         
        Q = 100*(Q - Q_ctl)/Q_ctl
        T = T - T_ctl # units of K

        # calculate clausius-Clapeyron rate based on control 
        CC = 100*const.Lv*const.Rv**-1*T_ctl**-2
        T  = T*CC # percent change units           


        # 3) percent change of eddy and transient eddy Vrms

        # read exp and control data 
        filename1     = dir_in_exp + 'zm_rms_V850_ml_' + str(ilat) + 'N_' + season + '_' + dim.timestamp + '.nc'
        filename2     = dir_in_ctl + 'zm_rms_V850_ml_' + str(ilat) + 'N_' + season + '_' + dim_ctl.timestamp + '.nc'
        ds1           = xr.open_dataset(filename1)
        ds2           = xr.open_dataset(filename2)
        rms_eddy      = ds1['rms_eddy'].values
        rms_trans     = ds1['rms_trans'].values
        rms_eddy_ctl  = ds2['rms_eddy'].values
        rms_trans_ctl = ds2['rms_trans'].values
        ds1.close()
        ds2.close()

        # get control climatology 
        rms_eddy_ctl  = rms_eddy_ctl.mean(axis=0)
        rms_trans_ctl = rms_trans_ctl.mean(axis=0)

        # get yearly anomalies relative to control clim        
        # and normalize                                                                              
        rms_eddy  = 100*(rms_eddy - rms_eddy_ctl)/rms_eddy_ctl
        rms_trans = 100*(rms_trans - rms_trans_ctl)/rms_trans_ctl

        # 4) dump into output array
        MN[0,iexp,iseason]  = VQ_eddy.mean(axis=0)
        MN[1,iexp,iseason]  = VQ_trans.mean(axis=0)
        MN[2,iexp,iseason]  = Q.mean(axis=0)
        MN[3,iexp,iseason]  = T.mean(axis=0)
        MN[4,iexp,iseason]  = rms_eddy.mean(axis=0)
        MN[5,iexp,iseason]  = rms_trans.mean(axis=0)
        
        STD[0,iexp,iseason] = VQ_eddy.std(axis=0)
        STD[1,iexp,iseason] = VQ_trans.std(axis=0)
        STD[2,iexp,iseason] = Q.std(axis=0)
        STD[3,iexp,iseason] = T.std(axis=0)
        STD[4,iexp,iseason] = rms_eddy.std(axis=0)
        STD[5,iexp,iseason] = rms_trans.std(axis=0)

        iseason = iseason + 1
    iexp    = iexp + 1


if write2file == 1:
    
    output = xr.Dataset(data_vars={'MN':(('variable','exp','season'), MN.astype(np.float32)),
                                   'STD': (('variable','exp','season'), STD.astype(np.float32))},
                        coords={'variable': np.arange(0,6,1),'exp': np.arange(0,len(data_name_local),1),\
                                'season':np.arange(0,len(season_name),1)})

    output.MN.attrs['units']               = '%'
    output.MN.attrs['standard_name']       = 'Mean percent change of a variable'
    output.STD.attrs['units']              = '%'
    output.STD.attrs['standard_name']      = 'standard deviation of percent change of a variable'
    output.variable.attrs['units']         = 'unitless'
    output.variable.attrs['standard_name'] = '1=VQ,2=VQ_trans,3=Q,4=T,5=Vrms,6=Vrms_trans'
    output.exp.attrs['units']              = 'unitless'
    output.exp.attrs['standard_name']      = '1=L+,2=L-,3=U+,4=U-,5=2L+,6=2U+,7=Rk1'
    output.season.attrs['units']           = 'unitless'
    output.season.attrs['standard_name']   = '1=ANNUAL,2=NDJFM'

    dir_out  = dir_interim + 'ALL_EXPS' + '/'
    filename = 'percent_change_' + str(ilat) + 'N.nc'
    output.to_netcdf(dir_out + filename)

