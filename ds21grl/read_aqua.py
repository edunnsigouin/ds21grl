"""
Collection of functions that read raw CESM model data
"""

def read_xyt_sfc_monthly(var,dir_in,dim):
    """                                                                                                         
    read monthly mean surface xyt data 
    across multiple years & months of the year into one array 
    """

    import numpy               as np
    import xarray              as xr
    from ds21grl           import const
    
    data = np.zeros((dim.years.size,dim.months.size,dim.lat.size,dim.lon.size))

    for iyear in range(0,dim.years.size):
        for imonth in range(0,dim.months.size):
            
            print(dim.years[iyear],dim.months[imonth])

            timestamp                = format(dim.years[iyear],"04") + '-' + format(imonth+1,"02")
            filename                 = dir_in + 'cam.h0.' + timestamp + '.nc'
            ds                       = xr.open_dataset(filename,decode_times=False)

            if var == 'diabatic_heating':
                # eqn 5 of Trenberth and Solomon 1994 ClimDyn                                   
                # from energy budget residual     
                data_monthly = ds['FSNT'].values - ds['FLNT'].values - \
                               (ds['FSNS'].values - ds['SHFLX'].values - ds['FLNS'].values) + \
                               ds['PRECC'].values*const.rhow*const.Lv + ds['PRECL'].values*const.rhow*const.Lv # convert to W/m**2
            else:
                data_monthly = ds[var].values
                
            data[iyear,imonth,:,:] = np.squeeze(data_monthly)
            ds.close()
            
    return data




def read_yt_zm_ml_daily(var,level,dir_in,dim):
    """                                      
    read daily zonal-mean yt data on a given model level          
    across multiple years in chunk format                                                                                
    """
    
    import numpy               as np
    import xarray              as xr
    from   ds21grl.misc        import get_aqua_timestamp

    data = np.zeros((dim.years.size,dim.nday,dim.lat.size))

    for iyear in range(0,dim.years.size):
        for ichunk in range(0,int(365/dim.chunk)):

            print('year: ' + str(dim.years[iyear]),',chunk: ' + str(ichunk))
            
            timestamp = get_aqua_timestamp(dim.years[iyear],ichunk,branch_flag=0)

            if var == 'T':
                filename    = dir_in + 'cam.h2.' + timestamp + '.nc'
                ds          = xr.open_dataset(filename,decode_times=False).sel(lev=level,method='nearest')
                data_chunk  = ds[var].values
                data_chunk  = np.mean(np.squeeze(data_chunk),axis=2)
                ds.close()
            elif var == 'Q':
                filename    = dir_in + 'cam.h3.' + timestamp + '.nc'
                ds          = xr.open_dataset(filename,decode_times=False).sel(lev=level,method='nearest')
                data_chunk  = ds[var].values
                data_chunk  = np.mean(np.squeeze(data_chunk),axis=2)
                ds.close()

            daysofyear               = np.arange(ichunk*dim.chunk,ichunk*dim.chunk+dim.chunk)
            data[iyear,daysofyear,:] = data_chunk[:,:]

    return data



def read_xt_ml_daily(var,level,ilat,dir_in,dim):
    """                    
    read daily zt data on a given model level and latitude  
    across multiple years in chunk format                                                                                  
    """
    import numpy               as np
    import xarray              as xr
    from ds21grl.misc          import get_aqua_timestamp

    data = np.zeros((dim.years.size,dim.nday,dim.lon.size))

    for iyear in range(0,dim.years.size):
        for ichunk in range(0,int(365/dim.chunk)):

            print('year: ' + str(dim.years[iyear]),',chunk: ' + str(ichunk))

            timestamp = get_aqua_timestamp(dim.years[iyear],ichunk,branch_flag=0)

            if var == 'V':
                filename    = dir_in + 'cam.h1.' + timestamp + '.nc'
                ds          = xr.open_dataset(filename,decode_times=False).sel(lev=level,method='nearest').sel(lat=ilat,method='nearest')
                data_chunk  = ds[var].values
                data_chunk  = np.squeeze(data_chunk)
                ds.close()

            daysofyear               = np.arange(ichunk*dim.chunk,ichunk*dim.chunk+dim.chunk)
            data[iyear,daysofyear,:] = data_chunk[:,:]

    return data






def read_yt_zm_sfc_daily(var,dir_in,dim):
    """                                                      
    read daily zonal-mean yt surface data 
    across multiple years in chunk format                                                                                     
    """    
    import numpy               as np
    import xarray              as xr
    from fxn.misc              import get_aqua_timestamp

    data = np.zeros((dim.years.size,dim.nday,dim.lat.size))

    for iyear in range(0,dim.years.size):
        for ichunk in range(0,int(365/dim.chunk)):

            print('year: ' + str(dim.years[iyear]),',chunk: ' + str(ichunk))
            
            timestamp = get_aqua_timestamp(dim.years[iyear],ichunk,branch_flag=0)

            filename  = dir_in + 'cam.h4.' + timestamp + '.nc'
            ds        = xr.open_dataset(filename,decode_times=False)
            
            if var == 'CFS':
                data_chunk  = ds.FLNSC.values - ds.FLNS.values + ds.FSNS.values - ds.FSNSC.values
            elif var == 'SWCFS':
                data_chunk  = ds.FSNS.values - ds.FSNSC.values
            elif var == 'LWCFS':
                data_chunk  = ds.FLNSC.values - ds.FLNS.values
            else:
                data_chunk  = ds[var].values
                
            data_chunk  = data_chunk.mean(axis=2)
            ds.close()
    
            daysofyear               = np.arange(ichunk*dim.chunk,ichunk*dim.chunk+dim.chunk)
            data[iyear,daysofyear,:] = data_chunk[:,:]

    return data








