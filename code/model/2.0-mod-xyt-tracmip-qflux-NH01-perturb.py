"""
Modifies the tracmip qflux file with a pertubation pattern following 
Neal and Hoskins 2001 ASL eqn 5 or 6 (gaussian-ish or zonal wavenumber).
Also outputs a qflux file with the perturbation qflux only for use 
in paper figures
"""

import numpy         as np
import xarray        as xr
from matplotlib      import pyplot as plt
import shutil
from ds21grl.misc    import qflux_const
from ds21grl.config  import dir_forcing_aqua,data_name,dir_interim

# INPUT -----------------------------------------------------------   
data_name_local = [data_name[2],data_name[3],data_name[6],data_name[7],data_name[9]]
ctl             = data_name[1]
write2file      = 0
# ----------------------------------------------------------------- 

for exp in data_name_local:

    print(exp)

    # get dimensions of qflux file from tracmip ctl
    filename  = dir_forcing_aqua + ctl + '/qflux.nc'
    ds        = xr.open_dataset(filename)
    lat       = ds.lat.values
    lon       = ds.lon.values
    time      = ds.time.values
    ds.close()

    # get constants to create qflux perturbation for a given experiment
    [Q0,lon0,lond,lat0,latd,wavenum_flag] = qflux_const(exp)

    # create meridional pattern
    temp1            = np.zeros((12,lat.size,lon.size))
    index            = np.where((lat >= lat0 - latd) & (lat  <= lat0 + latd))[0]
    for j in range(index[0],index[-1]+1,1):
        temp1[:,j,:] = np.cos((np.pi/2)*(lat[j]-lat0)/latd)**2

    # create zonal pattern
    temp2     = np.zeros((12,lat.size,lon.size))
    if wavenum_flag == 0: # NH01 eqn 5
        if (lon0 - lond >= 0) and (lon0 + lond <= lon[-1]): # between 0-360 deg
            index = np.where((lon >= lon0 - lond) & (lon <= lon0 + lond))[0]
        elif (lon0 - lond < 0): # less than 0 deg
            index = np.where((lon <= lon0 + lond) | (lon >= 360 + lon0 - lond))[0]
        elif (lon0 + lond > lon[-1]): # more than 358.5 deg
            index = np.where((lon <= lond - 360 + lon0) | (lon >= lon0 - lond))[0]
        temp2[:,:,index] = np.cos((np.pi/2)*(lon[index]-lon0)/lond)**2
    else: # NH01 eqn 6
        index            = np.arange(0,lon.size)
        temp2[:,:,index] = np.cos(np.deg2rad(lon[index])-np.deg2rad(lon0))
    
    # create total xy pattern
    qflux = Q0*temp1*temp2

    if write2file == 1:        
        # write forcing file (tracmip + perturbation)
        newfilename = dir_forcing_aqua + exp + '/qflux.nc'
        shutil.copyfile(filename, newfilename)
        ds        = xr.open_dataset(newfilename)
        temp      = xr.DataArray(qflux, coords={'time': time, 'lat': lat, 'lon': lon},dims=['time', 'lat', 'lon'])
        ds['qdp'] = ds['qdp'] + -1*temp # model qflux must have opposite sign!
        ds.qdp.to_netcdf(newfilename,mode='a')
        ds.close()

        # write perturbation only to use for paper figures
        newfilename = dir_interim + exp + '/qflux_anom.nc'
        output      = xr.DataArray(-1*qflux.mean(axis=0).astype(np.float32),dims = ['lat','lon'],coords={'lat':lat,'lon':lon})
        output.attrs['units']         = 'Wm**-2'
        output.attrs['standard_name'] = 'ocean heat flux convergence (q-flux) anomaly relative to control'
        output                        = output.to_dataset(name='qflux')
        output.to_netcdf(newfilename)

