"""
Makes an xyt qflux file that has the same zonally integrated energy input 
as a reference experiment (e.g., L+) except the energy is distrubuted uniformly 
at all longitudes. This is done by modifying the reference qflux file.
Also outputs a qflux file with the perturbation qflux for use in paper figures.  
"""

import numpy         as np
import xarray        as xr
from matplotlib      import pyplot as plt
import shutil
from  ds21grl        import const
from ds21grl.config  import dir_forcing_aqua,data_name,dir_interim

# INPUT ----------------------------------------------------------- 
data_name_local = [data_name[4],data_name[5],data_name[8]]
ctl             = data_name[1]
write2file      = 0
# -----------------------------------------------------------------     

for exp in data_name_local:

    print(exp)
    
    # defines reference asymmetric case
    if exp == data_name[4]:
        exp_ref = data_name[2]
    elif exp == data_name[5]:
        exp_ref = data_name[3]
    elif exp == data_name[8]:
        exp_ref = data_name[6]

    # get reference qflux file
    filename    = dir_forcing_aqua + exp_ref + '/qflux.nc'
    ds          = xr.open_dataset(filename)
    lat         = ds.lat.values
    lon         = ds.lon.values
    time        = ds.time.values
    qflux_ref   = ds.qdp.values
    ds.close()

    # calculate zonal integral (W/latitude) and divide by # of longitude grid points and area of a given grid point
    # to redistribute W/latitude into W/m**2/latitude/longitude
    area  = 2*np.pi*const.Re**2*np.cos(np.radians(lat))
    zint  = np.sum(qflux_ref,axis=2)
    for t in range(0,zint.shape[0]):
        zint[t,:] = zint[t,:]*area          # W/latitude
        zint[t,:] = zint[t,:]/area/lon.size # W/m**2/latitude/longitude

    # redistribute energy zonally
    qflux_new = np.zeros((time.size,lat.size,lon.size))
    for i in range(0,lon.size):
        qflux_new[:,:,i] = qflux_new[:,:,i] + zint[:,:]

    if write2file == 1:
        newfilename = dir_forcing_aqua + exp + '/qflux.nc'
        shutil.copyfile(filename, newfilename)
        ds        = xr.open_dataset(newfilename)
        temp      = xr.DataArray(qflux_new, coords={'time': time, 'lat': lat, 'lon': lon},dims=['time', 'lat', 'lon'])
        ds['qdp'] = ds['qdp']*0 + temp 
        ds.qdp.to_netcdf(newfilename,mode='a')
        ds.close()

        # write perturbation only to use for paper figures
        ctlfilename = dir_forcing_aqua + ctl + '/qflux.nc'
        ds          = xr.open_dataset(ctlfilename)
        qflux_ctl   = ds['qdp'].values
        qflux_new   = qflux_new.mean(axis=0) - qflux_ctl.mean(axis=0)
        newfilename = dir_interim + exp + '/qflux_anom.nc'
        output      = xr.DataArray(qflux_new.astype(np.float32),dims = ['lat','lon'],coords={'lat':lat,'lon':lon})
        output.attrs['units']         = 'Wm**-2'
        output.attrs['standard_name'] = 'ocean heat flux convergence (q-flux) anomaly relative to control'
        output                        = output.to_dataset(name='qflux')
        output.to_netcdf(newfilename)
    


