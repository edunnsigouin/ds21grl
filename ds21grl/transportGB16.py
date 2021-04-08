"""
Collection of functions to calculate daily zonally and vertically
integrated energy transport as a function of ykt as in 
Graversen and Burtu 2016 QJRMS
"""


def compute_dp_ml(PS,dim):
    """  
    calculates the difference in pressure across a hybrid-sigma model level.
    output dp in Pa units     
    """
    import numpy as np

    # compute pressure on hybrid level interfaces  
    pressure = np.zeros((dim.ilev.size,) + PS.shape)
    for k in range(0,dim.ilev.size):
        pressure[k,:] = dim.P0*dim.hyai[k] + dim.hybi[k]*PS[:]

    # take the difference between pressure at interfaces
    dp = np.zeros((dim.lev.size,) + PS.shape)
    for k in range(0,dim.ilev.size):
        if k > 0:
            dp[k-1,:] = pressure[k,:] - pressure[k-1,:]

    return dp



def compute_fft_amp(data,ax,wavenumber):
    """       
    Calculates sin and cos fourier amplitude coefficients 
    """
    import numpy       as np
    from  ds21grl.misc import AxRoll

    data = AxRoll(data,ax,invert=False) # switch axis for fft to first 

    xxx  = np.fft.fft(data,axis=0)/data.shape[0]
    A    = 2*np.real(xxx)
    B    = -2*np.imag(xxx)

    A    = A[wavenumber,:]
    B    = B[wavenumber,:]

    A    = AxRoll(A,-1,invert=True)
    B    = AxRoll(B,-1,invert=True) # switch back fft axis to orginal axis

    return A,B



def calc_ykt_transport(MF,energy,dim):
    """
    Calculates zonally and vertically integrated transport
    as a function of zonal wavenumber 
    NOTE: Hard-coded for mass flux (MF) and energy dims: (time,level,lat,lon)      
    """
    import numpy   as np
    from  ds21grl  import const

    [MF_A,MF_B]         = compute_fft_amp(MF,3,dim.wavenumber)
    [energy_A,energy_B] = compute_fft_amp(energy,3,dim.wavenumber)
    transport           = MF_A*energy_A + MF_B*energy_B
    transport           = transport.sum(axis=1)
    d                   = 2*np.pi*const.Re*np.cos(np.radians(dim.lat))
    for j in range(0,dim.lat.size):
        # zonal-mean
        transport[:,j,0] = transport[:,j,0]*d[j]/4
        # eddies  
        transport[:,j,1:] = transport[:,j,1:]*d[j]/2

    return transport



def calc_ykt_daily_VQ_eddy_aqua(dir_in,dim):
    """
    Calculates zonally and vertically integrated moisture transport  
    as a function of zonal wavenumber for all eddies (transient + stw).
    This is a wrapper for the main transport calculation function
    """
    import numpy as np
    import xarray as xr
    from  ds21grl              import const
    from  ds21grl.misc         import tic,toc,get_aqua_timestamp

    # Initialize
    VQ = np.zeros((dim.years.size,dim.nday,dim.lat.size,dim.wavenumber.size))

    # loop through all data chunks
    for iyear in range(0,dim.years.size):
        for ichunk in range(0,int(365/dim.chunk)):

            print('year: ' + str(dim.years[iyear]) + ', chunk: ' + str(ichunk))
            tic()
            
            # read data
            timestamp  = get_aqua_timestamp(dim.years[iyear],ichunk,branch_flag=0)
            filename1  = dir_in + 'cam.h1.' + timestamp + '.nc'
            filename2  = dir_in + 'cam.h3.' + timestamp + '.nc'
            filename3  = dir_in + 'cam.h3.' + timestamp + '.nc'
            ds1        = xr.open_dataset(filename1,decode_times=False)
            ds2        = xr.open_dataset(filename2,decode_times=False)
            ds3        = xr.open_dataset(filename3,decode_times=False)
            V          = ds1.V.values
            Q          = ds2.Q.values
            PS         = ds3.PS.values
            dim.hyai   = ds1.hyai.values
            dim.hybi   = ds1.hybi.values
            dim.P0     = ds1.P0.values
            dim.lev    = ds1.lev.values
            dim.ilev   = ds1.ilev.values
            ds1.close()
            ds2.close()
            ds3.close()

            # define energy + mass flux terms
            Q  = const.Lv*Q
            dp = compute_dp_ml(PS,dim)
            dp = np.swapaxes(dp,0,1) # shift dims of dp same as V
            V  = V*dp/const.go

            # calc transport
            VQ_chunk = calc_ykt_transport(V,Q,dim)

            # dump into long time series array and convert to PW                            
            daysofyear               = np.arange(ichunk*dim.chunk,ichunk*dim.chunk+dim.chunk)
            VQ[iyear,daysofyear,:,:] = VQ_chunk[:,:,:]/10**15

            toc()

    return VQ



def calc_ykt_daily_VQ_eddy_erai(dir_in,dim):
    """                                                                                                               
    Calculates zonally and vertically integrated moisture transport                         
    as a function of zonal wavenumber for all eddies (transient + stw).  
    This is a wrapper for the main transport calculation function   
    """
    import numpy as np
    import xarray as xr
    from  ds21grl              import const
    from  ds21grl.misc         import tic,toc,leap_year_test,month_to_dayofyear

    # Initialize                
    VQ = np.zeros((dim.years.size,dim.nday,dim.lat.size,dim.wavenumber.size))

    for iyear in range(0,dim.years.size):
        for imonth in range(0,dim.months.size):

            tic()
    
            # read data for each month
            timestamp = str(dim.years[iyear]) + '-' + format(dim.months[imonth], "02")
            filename1 = dir_in + '/model_level/v/v_' + timestamp + '.nc'
            filename2 = dir_in + '/model_level/q/q_' + timestamp + '.nc'
            filename3 = dir_in + '/sfc/lnsp/lnsp_' + timestamp + '.nc'
            ds1       = xr.open_dataset(filename1)
            ds2       = xr.open_dataset(filename2)
            ds3       = xr.open_dataset(filename3)
            day       = ds1.day.values
            dim.P0    = ds1.P0.values
            dim.hyai  = ds1.hyai.values/dim.P0 # set units same as model
            dim.hybi  = ds1.hybi.values
            dim.lev   = ds1.lev.values
            dim.ilev  = ds1.ilev.values
            V         = ds1.v.values
            Q         = ds2.q.values
            PS        = np.exp(ds3.lnsp.values)
            ds1.close()
            ds2.close()
            ds3.close()
            
            # remove leap year day
            if (leap_year_test(dim.years[iyear]) == 1) & (dim.months[imonth] == 2):
                V    = V[:28,:,:,:]
                Q    = Q[:28,:,:,:]
                PS   = PS[:28,:,:]
                day  = day[:28]

            # define energy + mass flux terms
            Q  = const.Lv*Q
            dp = compute_dp_ml(PS,dim)
            dp = np.swapaxes(dp,0,1) # shift dims of dp same as
            V  = V*dp/const.go

	    # calc transport
            VQ_month = calc_ykt_transport(V,Q,dim)
            
            # dump into long time series array and convert to PW                                             
            daysofyear               = np.arange(month_to_dayofyear(imonth-1),month_to_dayofyear(imonth))
            VQ[iyear,daysofyear,:,:] = VQ_month[:,:,:]/10**15

            toc()

    return VQ
    


def calc_ykt_monthly_VQ_stw_aqua(dir_in,dim):
    """                                                               
    Calculates zonally and vertically integrated moisture transport   
    as a function of zonal wavenumber for stationary waves.                                                                        
    This is a wrapper for the main transport calculation function
    where the input data is the monthly climatological mass flux and
    specific humidity.
    """
    
    import numpy as np
    import xarray as xr
    from  ds21grl              import const
    from  ds21grl.misc         import tic,toc,get_aqua_timestamp,daysinmonths

    # initialize
    V = np.zeros((dim.months.size,dim.lev.size,dim.lat.size,dim.lon.size))
    Q = np.zeros((dim.months.size,dim.lev.size,dim.lat.size,dim.lon.size))

    # calculate monthly mean mass flux and specific humidity
    for iyear in range(0,dim.years.size):
        for ichunk in range(0,int(365/dim.chunk)):

            print('year: ' + str(dim.years[iyear]) + ', chunk: ' + str(ichunk))

            tic()

            # read data             
            timestamp = get_aqua_timestamp(dim.years[iyear],ichunk,branch_flag=0)
            filename1 = dir_in + 'cam.h1.' + timestamp + '.nc'
            filename2 = dir_in + 'cam.h3.' + timestamp + '.nc'
            filename3 = dir_in + 'cam.h3.' + timestamp + '.nc'
            ds1       = xr.open_dataset(filename1)
            ds2       = xr.open_dataset(filename2)
            ds3       = xr.open_dataset(filename3)
            V_chunk   = ds1.V.values
            Q_chunk   = ds2.Q.values
            PS_chunk  = ds3.PS.values
            dim.hyai  = ds1.hyai.values
            dim.hybi  = ds1.hybi.values
            dim.lev   = ds1.lev.values
            dim.ilev  = ds1.ilev.values
            month     = ds1['time.month'].values - 1
            ds1.close()
            ds2.close()
            ds3.close()

            # define energy + mass flux terms
            Q_chunk  = const.Lv*Q_chunk
            dp       = compute_dp_ml(PS_chunk,dim)
            dp       = np.swapaxes(dp,0,1) # shift dims of dp same as V  
            V_chunk  = V_chunk*dp/const.go

            # calculate monthly mean stationary wave components
            for t in range(0,dim.chunk):
                V[month[t],:,:,:] = V[month[t],:,:,:] + V_chunk[t,:,:,:]/dim.years.size/daysinmonths(month[t])
                Q[month[t],:,:,:] = Q[month[t],:,:,:] + Q_chunk[t,:,:,:]/dim.years.size/daysinmonths(month[t])

            toc()

    # calc transport using climatological monthly mean mass flux and latent energy
    VQ = calc_ykt_transport(V,Q,dim)
    VQ = VQ/10**15 # convert to PW  

    return VQ



def calc_ykt_daily_VQ_trans(dir_in,dim):
    """
    Calculates daily zonally and vertically integrated transient moisture transport 
    as a function of latitude and wavenumber for a given aquaplanet simulation
    following Graversen and Burtu (2016) QJRMS.
    The transient component is calculated by removing the monthly climatological
    stationary wave component from the daily eddy transport.      
    """
    import numpy        as np
    import xarray       as xr
    from  ds21grl.misc  import dayofyear_to_month
    
    # read stationary wave transport data                     
    filename   = dir_in + 'ykt_zint_vint_ml_monthly_VQ_stw_' + dim.timestamp + '.nc'
    ds         = xr.open_dataset(filename)
    VQ_stw     = ds.VQ.values
    ds.close()
    
    # read eddy transport data
    filename  = dir_in + 'ykt_zint_vint_ml_daily_VQ_eddy_' + dim.timestamp + '.nc'
    ds        = xr.open_dataset(filename)
    VQ        = ds.VQ.values
    ds.close()

    # remove time-mean stationary wave component for each month
    for yr in range(0,dim.years.size):
        print('year: ' + str(dim.years[yr]))
        for t in range(0,dim.nday):
            # don't include wave 0 since its not a stationary 'wave'                                                                         
            VQ[yr,t,:,1:] = VQ[yr,t,:,1:] - VQ_stw[dayofyear_to_month(t)-1,:,1:]
        
    return VQ



def write_ykt_daily_transport(data,var,flag,dir_out,dim,write2file):
    """ 
    Writes daily ykt data into a file
    """
    import numpy  as np
    import xarray as xr

    if write2file == 1:
        output = xr.Dataset(data_vars={var: (('year','day','lat','wavenumber'),data.astype(np.float32))},
                            coords={'year': dim.years,'day': np.arange(0,dim.nday),'lat': dim.lat,'wavenumber': dim.wavenumber})
        if var == 'VQ':
            output.VQ.attrs['units'] = 'PW'
            
        filename = dir_out + 'ykt_zint_vint_ml_daily_' + var + '_' + flag + '_' + dim.timestamp + '.nc'
        output.to_netcdf(filename)

    return



def write_ykt_monthly_clim_transport(data,var,flag,dir_out,dim,write2file):
    """
    Writes monthly climatological ykt data into a file 
    """
    import numpy  as np
    import xarray as xr

    if write2file == 1:
        output = xr.Dataset(data_vars={var: (('month','lat','wavenumber'),data.astype(np.float32))},
                            coords={'month': dim.months,'lat': dim.lat,'wavenumber': dim.wavenumber})
        if var == 'VQ':
            output.VQ.attrs['units'] = 'PW'
            
        filename = dir_out + 'ykt_zint_vint_ml_monthly_' + var + '_' + flag + '_' + dim.timestamp + '.nc'
        output.to_netcdf(filename)

    return



def write_yk_clim_transport(data,var,flag,season,dir_out,dim,write2file):
    """                                                                                
    Writes climatological yk data into a file                                                       
    """
    import numpy  as np
    import xarray as xr

    if write2file == 1:
        output = xr.Dataset(data_vars={var: (('lat','wavenumber'),data.astype(np.float32))},
                            coords={'lat': dim.lat,'wavenumber': dim.wavenumber})
        if var == 'VQ':
            output.VQ.attrs['units'] = 'PW'

        filename = dir_out + 'yk_zint_vint_ml_clim_' + var + '_' + flag + '_' + season + '_' + dim.timestamp + '.nc'
        output.to_netcdf(filename)

    return



def write_yk_clim_anom_transport(data,sig,var,flag,season,dir_out,dim,write2file):
    """
    Writes anomalous climatological yk data into a file
    """
    import numpy  as np
    import xarray as xr

    if write2file == 1:
        output = xr.Dataset(data_vars={var: (('lat','wavenumber'), data.astype(np.float32)),
                                    'sig': (('lat','wavenumber'), sig.astype(np.float32))},
                            coords={'lat': dim.lat,'wavenumber': dim.wavenumber})
        if var == 'VQ':
            output.VQ.attrs['units'] = 'PW'
            
        output.sig.attrs['units']         = 'unitless'
        output.sig.attrs['standard_name'] = '95 percent significance = 0'

        filename = dir_out + 'yk_zint_vint_ml_clim_anom_' + var + '_' + flag + '_' + season + '_' + dim.timestamp + '.nc'
        output.to_netcdf(filename)

    return
