"""
Collection of useful read & write functions
for era-interim reanalysis data
"""

def translate_var_CESM_to_erai(var):
    """
    translates CESM variable names
    into era-interim reanalysis names
    """
    if var == 'T':
        new_var = 't'
    elif var == 'Q':
        new_var = 'q'
    elif var == 'V':
        new_var = 'v'
    elif var == 'U':
        new_var = 'u'
    elif var == 'Z3':
        new_var = 'z'
    elif var == 'FLDS':
        new_var = 'strd'
    else:
        new_var = var
    return new_var


def read_yt_zm_ml_daily(var,level,dir_in,dim):
    """                                                                                  
    read daily zonal-mean yt data on a given model level
    across multiple years  
    """

    import numpy         as np
    import xarray        as xr
    from   ds21grl.misc  import month_to_dayofyear,leap_year_test

    data = np.zeros((dim.years.size,dim.nday,dim.lat.size))
    var  = translate_var_CESM_to_erai(var)
    for iyear in range(0,dim.years.size):
        for imonth in range(0,dim.months.size):

            print(dim.years[iyear],dim.months[imonth])

            timestamp              = str(dim.years[iyear]) + '-' + format(dim.months[imonth], "02")
            filename               = dir_in + 'model_level/' + var + '/' + var  + '_' + timestamp + '.nc'
            ds                     = xr.open_dataset(filename).sel(lev=level,method='nearest').mean(dim='lon')
            data_monthly           = ds[var].values
            day                    = ds['day'].values
            ds.close()

            # remove leap year day                        
            if (leap_year_test(dim.years[iyear]) == 1) & (dim.months[imonth] == 2):
                data_monthly = data_monthly[:28,:]
                day          = day[:28]

            daysofyear               = np.arange(month_to_dayofyear(imonth-1),month_to_dayofyear(imonth))
            data[iyear,daysofyear,:] = data_monthly[:,:]

    return data



def read_yt_zm_pl_daily(var,level,dir_in,dim):
    """
    read daily zonal-mean yt data on a given pressure level
    across multiple years                                                                                     
    """

    import numpy         as np
    import xarray        as xr
    from   ds21grl.misc  import month_to_dayofyear,leap_year_test

    data = np.zeros((dim.years.size,dim.nday,dim.lat.size))
    var  = translate_var_CESM_to_erai(var)
    
    for iyear in range(0,dim.years.size):
        for imonth in range(0,dim.months.size):

            print(dim.years[iyear],dim.months[imonth])

            timestamp              = str(dim.years[iyear]) + '-' + format(dim.months[imonth], "02")
            filename               = dir_in + 'pressure_level/' + var + str(level) + '/' + var  + '_' + timestamp + '.nc'
            ds                     = xr.open_dataset(filename).sel(method='nearest').mean(dim='lon')
            data_monthly           = ds[var].values
            day                    = ds['day'].values
            ds.close()

            # remove leap year day
            if (leap_year_test(dim.years[iyear]) == 1) & (dim.months[imonth] == 2):
                data_monthly = data_monthly[:28,:]
                day          = day[:28]

            daysofyear               = np.arange(month_to_dayofyear(imonth-1),month_to_dayofyear(imonth))
            data[iyear,daysofyear,:] = data_monthly[:,:]

    return data


                

def read_yt_zm_sfc_daily(var,dir_in,dim):
    """   
    read daily zonal-mean yt surface data   
    across multiple years in monthly format 
    """
    import numpy      as np
    import xarray     as xr
    from   fxn.misc   import month_to_dayofyear,leap_year_test

    data = np.zeros((dim.years.size,dim.nday,dim.lat.size))
    var  = translate_var_CESM_to_erai(var)
    
    for iyear in range(0,dim.years.size):
        for imonth in range(0,dim.months.size):

            timestamp = str(dim.years[iyear]) + '-' + format(dim.months[imonth], "02")
            print(dim.years[iyear],dim.months[imonth])

            if var == 'CFS':
                filename1     = dir_in + 'sfc/ssr/ssr_' + timestamp + '.nc'
                filename2     = dir_in + 'sfc/ssrs/ssrs_' + timestamp + '.nc'
                filename3     = dir_in + 'sfc/str/str_' + timestamp + '.nc'
                filename4     = dir_in + 'sfc/strc/strc_' + timestamp + '.nc'
                ds1           = xr.open_dataset(filename1).mean(dim='longitude')
                ds2           = xr.open_dataset(filename2).mean(dim='longitude')
                ds3           = xr.open_dataset(filename3).mean(dim='longitude')
                ds4           = xr.open_dataset(filename4).mean(dim='longitude')
                day           = ds1.day.values
                data_monthly  = ds1['ssr'].values - ds2['ssrc'].values + ds3['str'].values - ds4['strc'].values
                ds1.close()
                ds2.close()
                ds3.close()
                ds4.close()
            elif var == 'SWCFS':
                filename1     = dir_in + 'sfc/ssr/ssr_' + timestamp + '.nc'
                filename2     = dir_in + 'sfc/ssrs/ssrs_' + timestamp + '.nc'
                ds1           = xr.open_dataset(filename1).mean(dim='longitude')
                ds2           = xr.open_dataset(filename2).mean(dim='longitude')
                day           = ds1.day.values
                data_monthly  = ds1['ssr'].values - ds2['ssrc'].values
                ds1.close()
                ds2.close()
            elif var == 'LWCFS':
                filename1     = dir_in + 'sfc/str/str_' + timestamp + '.nc'
                filename2     = dir_in + 'sfc/strc/strc_' + timestamp + '.nc'
                ds1           = xr.open_dataset(filename1).mean(dim='longitude')
                ds2           = xr.open_dataset(filename2).mean(dim='longitude')
                day           = ds1.day.values
                data_monthly  = ds1['str'].values - ds2['strc'].values
                ds1.close()
                ds2.close()
            else:
                filename1     = dir_in + 'sfc/' + var + '/' + var + '_' + timestamp + '.nc'
                ds1           = xr.open_dataset(filename1).mean(dim='longitude')
                day           = ds1.day.values
                data_monthly  = ds1[var].values
                ds1.close()

            # remove leap year day 
            if (leap_year_test(dim.years[iyear]) == 1) & (dim.months[imonth] == 2):
                data_monthly = data_monthly[:28,:]
                day          = day[:28]

            daysofyear               = np.arange(month_to_dayofyear(imonth-1),month_to_dayofyear(imonth))
            data[iyear,daysofyear,:] = data_monthly[:,:]

    return data




def read_xt_ml_daily(var,level,ilat,dir_in,dim):
    """                     
    read daily xt data on a given model level     
    across multiple years                                                                                 
    """
    import numpy         as np
    import xarray        as xr
    from   ds21grl.misc  import month_to_dayofyear,leap_year_test

    data = np.zeros((dim.years.size,dim.nday,dim.lon.size))
    var  = translate_var_CESM_to_erai(var)
    
    for iyear in range(0,dim.years.size):
        for imonth in range(0,dim.months.size):

            print(dim.years[iyear],dim.months[imonth])

            timestamp              = str(dim.years[iyear]) + '-' + format(dim.months[imonth], "02")
            filename               = dir_in + 'model_level/' + var + '/' + var  + '_' + timestamp + '.nc'
            ds                     = xr.open_dataset(filename).sel(lev=level,lat=ilat,method='nearest')
            data_monthly           = ds[var].values
            day                    = ds['day'].values
            ds.close()

            # remove leap year day
            if (leap_year_test(dim.years[iyear]) == 1) & (dim.months[imonth] == 2):
                data_monthly = data_monthly[:28,:]
                day          = day[:28]

            daysofyear               = np.arange(month_to_dayofyear(imonth-1),month_to_dayofyear(imonth))
            data[iyear,daysofyear,:] = data_monthly[:,:]

    return data


def read_xt_pl_daily(var,level,ilat,dir_in,dim):
    """                                            
    read daily xt data on a given pressure level                                                                                           
    across multiple years                                                                                               
    """
    import numpy         as np
    import xarray        as xr
    from   ds21grl.misc  import month_to_dayofyear,leap_year_test

    data = np.zeros((dim.years.size,dim.nday,dim.lon.size))
    var  = translate_var_CESM_to_erai(var)

    for iyear in range(0,dim.years.size):
        for imonth in range(0,dim.months.size):

            print(dim.years[iyear],dim.months[imonth])

            timestamp              = str(dim.years[iyear]) + '-' + format(dim.months[imonth], "02")
            filename               = dir_in + 'pressure_level/' + var + str(level) + '/' + var  + '_' + timestamp + '.nc'
            ds                     = xr.open_dataset(filename).sel(latitude=ilat,method='nearest')
            data_monthly           = ds[var].values
            day                    = ds['day'].values
            ds.close()

            # remove leap year day 
            if (leap_year_test(dim.years[iyear]) == 1) & (dim.months[imonth] == 2):
                data_monthly = data_monthly[:28,:]
                day          = day[:28]

            daysofyear               = np.arange(month_to_dayofyear(imonth-1),month_to_dayofyear(imonth))
            data[iyear,daysofyear,:] = data_monthly[:,:]

    return data


    
