"""
collection of useful miscellaneous functions     
"""

def get_dim_exp(exp):
    """
    outputs hard-coded data dimensions (lat-lon-lev-time)
    for a given simulation
    """
    if exp == "QSC5.TRACMIP.NH01.L.pos.Q0.300.lon0.150.lond.45.lat0.0.latd.30":
        from ds21grl import dim_aqua_short as dim
    else:
        from ds21grl import dim_aqua as dim
    
    return dim


def tic():
    # Homemade version of matlab tic function                                                                                             
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()


def toc():
    # Homemade version of matlab tic function                                                       
    import time
    if 'startTime_for_tictoc' in globals():
        print("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print("Toc: start time not set")

        
def qflux_const(exp):
    """
    predefined constants to generate qflux patterns
    """
    
    if exp == 'QSC5.TRACMIP.NH01.L.pos.Q0.150.lon0.150.lond.90.lat0.0.latd.30':
        Q0            = 150
        lon0          = 150
        lond          = 90
        lat0          = 0
        latd          = 30
        wavenum_flag  = 0
    elif exp == 'QSC5.TRACMIP.NH01.L.neg.Q0.150.lon0.150.lond.90.lat0.0.latd.30':
        Q0            =	-150
        lon0          = 150
        lond          = 90
        lat0          = 0
        latd          = 30
        wavenum_flag  = 0
    elif exp == 'QSC5.TRACMIP.NH01.U.pos.Q0.150.lon0.150.lond.90.lat0.0.latd.30':
        Q0            =	150
        lon0          = 150
        lond          = 90
        lat0          = 0
        latd          = 30
        wavenum_flag  = 0
    elif exp == 'QSC5.TRACMIP.NH01.U.neg.Q0.150.lon0.150.lond.90.lat0.0.latd.30':
        Q0            =	-150
        lon0          = 150
        lond          = 90
        lat0          = 0
        latd          = 30
        wavenum_flag  = 0
    elif exp == 'QSC5.TRACMIP.NH01.L.pos.Q0.300.lon0.150.lond.90.lat0.0.latd.30':
        Q0            =	300
        lon0          = 150
        lond          = 90
        lat0          = 0
        latd          = 30
        wavenum_flag  = 0
    elif exp == 'QSC5.TRACMIP.NH01.Lk1.Q0.75.lon0.150.lat0.0.latd.30':
        Q0            =	75
        lon0          = 150
        lond          = 0
        lat0          = 0
        latd          = 30
        wavenum_flag  = 1
    elif exp == 'QSC5.TRACMIP.NH01.U.pos.Q0.300.lon0.150.lond.90.lat0.0.latd.30':
        Q0            =	300
        lon0          = 150
        lond          = 90
        lat0          = 0
        latd          = 30
        wavenum_flag  = 0
    elif exp == 'QSC5.TRACMIP.NH01.L.pos.Q0.300.lon0.150.lond.45.lat0.0.latd.30':    
        Q0            =	300
        lon0          = 150
        lond          = 45
        lat0          = 0
        latd          = 30
        wavenum_flag  = 0
    return Q0,lon0,lond,lat0,latd,wavenum_flag



def daysinmonths(month):
    """                                                                              
    outputs number of days in a given month without leap             
    year days                  
    """
    import numpy as np

    temp = np.array([31,28,31,30,31,30,31,31,30,31,30,31])

    return temp[month-1]


def month_to_dayofyear(month):
    """
    maps months (0-11) to day of year (0-364)
    where day of year refers to last day of that month
    """
    import numpy as np
    daysinmonths = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    
    if month < 0:
        dayofyear = 0
    else:
        dayofyear = daysinmonths[:month+1].sum(axis=0)
    
    return dayofyear
    

def dayofyear_to_month(dayofyear):
    """                                                                                      
    maps day of year (1-365) onto a months (1-12)  
    """
    import numpy as np
    daysinmonths = np.array([31,28,31,30,31,30,31,31,30,31,30,31])

    dayofyear = dayofyear + 1 # convert to dayofyear (1-365) from (0-364) 

    if dayofyear > 0 and dayofyear <= 31:
        month = 1
    else:
        for i in range(1,12):
            if (dayofyear > np.sum(daysinmonths[0:i])) and (dayofyear <= np.sum(daysinmonths[0:i+1])) :
                month = i + 1

    return month



def leap_year_test(year):
    """  
    Flag if year is a leap year 
    """
    flag = 0
    if (year % 4 == 0):
        flag = 1
    elif (year % 100 == 0) and (year % 400 != 0):
        flag = 0
    return flag


def get_aqua_timestamp(iyear,ichunk,branch_flag):
    """
    outputs a timestamp string for model runs with a 
    predifined year-month-day timestamp split into
    5 x 73 day chunks for a given year
    """
    import numpy as np

    if branch_flag == 0:
        if ichunk == 0:
            timestamp = format(iyear,"04") + '-01-01-00000'
        elif ichunk == 1:
            timestamp = format(iyear,"04") + '-03-15-00000'
        elif ichunk == 2:
            timestamp = format(iyear,"04") + '-05-27-00000'
        elif ichunk == 3:
            timestamp = format(iyear,"04") + '-08-08-00000'
        elif ichunk == 4:
            timestamp = format(iyear,"04") + '-10-20-00000'
    else: # branch run chunk start days shifted by 1 day
        if ichunk == 0:
            timestamp = format(iyear,"04") + '-01-02-00000'
        elif ichunk == 1:
            timestamp = format(iyear,"04") + '-03-16-00000'
        elif ichunk == 2:
            timestamp = format(iyear,"04") + '-05-28-00000'
        elif ichunk == 3:
            timestamp = format(iyear,"04") + '-08-09-00000'
        elif ichunk == 4:
            timestamp = format(iyear,"04") + '-10-21-00000'        
            
    return timestamp


def AxRoll(x,ax,invert=False):
    """                                                             
    Re-arrange array x so that axis 'ax' is first dimension.                                                                           
    Undo this if invert=True 
    """
    import numpy as np

    if ax < 0:
        n = len(x.shape) + ax
    else:
        n = ax

    if invert is False:
        y = np.rollaxis(x,n,0)
    else:
        y = np.rollaxis(x,0,n+1)

    return y



def get_season_daily(data,season,ax):
    """
    Extracts days in season from axis with
    days 1-365
    """
    import numpy as np

    data      = AxRoll(data,ax,invert=False)
    dayofyear = np.arange(0,365,1)

    # hardcoded mask for days in season
    if season == 'NDJFM':
        dayofyear = np.roll(dayofyear,61,axis=0)
        index     = dayofyear[0:151]
    elif season == 'MJJAS':
        index     = dayofyear[120:273]
    elif season == 'ANNUAL':
        index     = dayofyear

    # extract days in season    
    data = data[index,:]
    data = AxRoll(data,ax,invert=True)
    
    return data


def get_season_monthly(data,season,ax):
    """                                                                                                                
    Extracts months correspinding to a given season from monthly
    data                                                                                               
    NOTE: ax = month dimension                                                                                 
    """
    import numpy as np

    data      = AxRoll(data,ax,invert=False)

    # hardcoded mask for days in season  
    if season == 'NDJFM':
        index     = np.array([1,2,3,11,12]) -1
    elif season == 'MJJAS':
        index     = np.arange(5,10,1) -1
    elif season == 'ANNUAL':
        index     = np.arange(1,13,1) -1

    # extract months in season                                                                                                  
    data = data[index,:]
    data = AxRoll(data,ax,invert=True)

    return data




def get_anomaly_daily_seasonal_cycle(data,dim):
    """      
    Removes the climatological daily seasonal cycle.
    NOTE: Data must have years and daysofyear as 1st and 2nd dims
    respectively
    """
    import numpy as np

    # define daily mean seasonal cycle
    scycle = data.mean(axis=0)

    # remove seasonal cycle
    for t in range(0,dim.years.size):
        data[t,:] = data[t,:] - scycle[:]
       
    return data




def get_eddy(data,ax):
    """
    Extracts deviation from zonal-mean
    ax = longitude axis
    """
    import numpy as np

    if data.ndim == 1:
        zmean = data.mean(axis=0)
        data  = data - zmean
    else:    
        data  = AxRoll(data,ax,invert=False) # shift longitude to 1st dim
        zmean = data.mean(axis=0)
        for i in range(0,data.shape[0]):
            data[i,:] = data[i,:] - zmean[:]

        data  = AxRoll(data,ax,invert=True)
    
    return data
