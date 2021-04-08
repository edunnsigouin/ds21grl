"""
Collection of functions to write data into netcdf files 
"""

def write_xyt_sfc_monthly(data,var,dir_out,dim,write2file):
    """           
    write monthly mean surface xyt data
    across multiple years & months of the year
    into one long file
    """

    import numpy               as np
    import xarray              as xr

    if write2file == 1:

        output    = xr.DataArray(data.astype(np.float32), dims=['year','month','lat','lon'],\
                                 coords={'year':dim.years,'month':dim.months,'lat': dim.lat,'lon':dim.lon})

        if var == 'SST':
            output.attrs['units']         = 'K'
            output.attrs['standard_name'] = 'sea surface temperature'
        if var == 'diabatic_heating':
            output.attrs['units']         = 'W/m**2'
            output.attrs['standard_name'] = 'vertically integrated diabatic heating'

        output    = output.to_dataset(name=var)
        filename  = dir_out + 'xyt_sfc_monthly_' + var + '_' + dim.timestamp + '.nc'
        output.to_netcdf(filename)

    return


def write_xy_sfc_clim(data,var,season,dir_out,dim,write2file):
    """   
    write xy climatology of a surface variable into a file 
    """
    import numpy               as np
    import xarray              as xr

    if write2file == 1:

        output = xr.Dataset(data_vars={var: (('lat','lon'), data.astype(np.float32))},
                            coords={'lat': dim.lat,'lon': dim.lon})
        if var == 'SST':
            output.SST.attrs['units']         = 'K'
            output.SST.attrs['standard_name'] = 'sea surface temperature'
        if var == 'diabatic_heating':
            output.diabatic_heating.attrs['units']         = 'W/m**2'
            output.diabatic_heating.attrs['standard_name'] = 'vertically integrated diabatic heating'

        filename  = dir_out + 'xy_sfc_clim_' + var + '_' + season + '_' + dim.timestamp + '.nc'
        output.to_netcdf(filename)

    return



def write_xy_sfc_clim_anom(data,sig,var,season,dir_out,dim,write2file):
    """                    
    write xy anomaly climatology of a surface variable into a file  
    """
    import numpy               as np
    import xarray              as xr

    if write2file == 1:

        output = xr.Dataset(data_vars={var: (('lat','lon'), data.astype(np.float32)),
                                       'sig': (('lat','lon'), sig.astype(np.float32))},
                            coords={'lat': dim.lat,'lon': dim.lon})
        if var == 'SST':
            output.SST.attrs['units']         = 'K'
            output.SST.attrs['standard_name'] = 'sea surface temperature'
        if var == 'diabatic_heating':
            output.diabatic_heating.attrs['units']         = 'W/m**2'
            output.diabatic_heating.attrs['standard_name'] = 'vertically integrated diabatic heating'

        output.sig.attrs['units']         = 'unitless'
        output.sig.attrs['standard_name'] = '95 percent significance = 0'

        filename  = dir_out + 'xy_sfc_clim_anom_' + var + '_' + season + '_' + dim.timestamp + '.nc'
        output.to_netcdf(filename)

    return



def write_yt_zm_ml_daily(data,var,level,dir_out,dim,write2file):
    """                         
    write daily zonal-mean yt data on a model level
    """
    import numpy               as np
    import xarray              as xr

    if write2file == 1:

        output = xr.DataArray(data.astype(np.float32),dims = ['year','day','lat'],\
                              coords={'year':dim.years,'day':np.arange(0,dim.nday,1),'lat':dim.lat})
        if var == 'T':
            output.attrs['units']         = 'K'
            output.attrs['standard_name'] = 'temperature'
        elif var == 'Q':
            output.attrs['units']         = 'kg/kg'
            output.attrs['standard_name'] = 'specific humidity'

        output         = output.to_dataset(name=var)
        outputfilename = dir_out + 'yt_zm_daily_' + var + str(level) + '_ml_' + dim.timestamp + '.nc'
        output.to_netcdf(outputfilename)

    return


def write_yt_zm_pl_daily(data,var,level,dir_out,dim,write2file):
    """                             
    write daily zonal-mean yt data on a model level
    """
    import numpy               as np
    import xarray              as xr

    if write2file == 1:

        output = xr.DataArray(data.astype(np.float32),dims = ['year','day','lat'],\
                              coords={'year':dim.years,'day':np.arange(0,dim.nday,1),'lat':dim.lat})
        if var == 'T':
            output.attrs['units']         = 'K'
            output.attrs['standard_name'] = 'temperature'
	elif var == 'Q':
            output.attrs['units']         = 'kg/kg'
            output.attrs['standard_name'] = 'specific humidity'

        output         = output.to_dataset(name=var)
        outputfilename = dir_out + 'yt_zm_daily_' + var + str(level) + '_pl_' + dim.timestamp + '.nc'
        output.to_netcdf(outputfilename)

    return


def write_yt_zm_sfc_daily(data,var,dir_out,dim,write2file):
    """                                                                         
    write daily zonal-mean yt data on a given model level
    """    
    import numpy               as np
    import xarray              as xr

    if write2file == 1:

        output = xr.DataArray(data.astype(np.float32),dims = ['year','day','lat'],\
                              coords={'year':dim.years,'day':np.arange(0,dim.nday,1),'lat':dim.lat})
        if var == 'CFS':
            output.attrs['units']         = 'W/m**2'
            output.attrs['standard_name'] = 'Cloud surface radiative forcing'
        elif var == 'LWCFS':
            output.attrs['units']         = 'W/m**2'
            output.attrs['standard_name'] = 'Longwave cloud surface radiative forcing'
        elif var == 'SWCFS':
            output.attrs['units']         = 'W/m**2'
            output.attrs['standard_name'] = 'Shortwave cloud surface radiative forcing'
        elif var == 'FLDS':
            output.attrs['units']         = 'W/m**2'
            output.attrs['standard_name'] = 'Downwelling longwave flux at surface'

        output   = output.to_dataset(name=var)
        filename = dir_out + 'yt_zm_daily_' + var + '_sfc_' + dim.timestamp + '.nc'
        output.to_netcdf(filename)

    return
