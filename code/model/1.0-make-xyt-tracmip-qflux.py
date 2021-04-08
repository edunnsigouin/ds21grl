"""
Makes an xyt qflux file for a CAM5 aquaplanet simulation with the pattern
taken from Voigt et al. 2016 JAMES. This is done by modifying the CAM5 default
slab ocean model file with zero qflux. 
"""

import numpy         as np
import xarray        as xr
from matplotlib      import pyplot as plt
import shutil
from ds21grl.config  import dir_forcing_aqua,data_name

# INPUT -----------------------------------------------------------   
write2file = 0
# -----------------------------------------------------------------

# define tracmip constants
po_n       = -50.1685
p1_n       = 4.9755
p2_n       = -1.4162*10**-1
p3_n       = 1.6743*10**-3
p4_n       = -6.8650*10**-6
po_s       = -56.0193
p1_s       = -6.4824
p2_s       = -2.3494*10**-1
p3_s       = -3.4685*10**-3
p4_s       = -1.7732*10**-5

# get dimensions of qflux from default file
filename = dir_forcing_aqua + data_name[1] + '/qflux.default.nc'
ds       = xr.open_dataset(filename)
qflux    = ds['qdp'].values
lat      = ds['lat'].values
lon      = ds['lon'].values
time     = ds['time'].values
ds.close()

# create tracmip qflux file
qflux = np.zeros((12,lat.size,lon.size))
for j in range(0,lat.size):
    if lat[j] > 0:
        qflux[:,j,:] = po_n + p1_n*lat[j] + p2_n*lat[j]**2 + p3_n*lat[j]**3 + p4_n*lat[j]**4 
    elif lat[j] < 0:
        qflux[:,j,:] = po_s + p1_s*lat[j] +p2_s*lat[j]**2 + p3_s*lat[j]**3 + p4_s*lat[j]**4
        
if write2file == 1:
    newfilename = dir_forcing_aqua + data_name[1] + '/qflux.nc'
    shutil.copyfile(filename, newfilename)
    ds        = xr.open_dataset(newfilename)
    temp      = xr.DataArray(qflux, coords={'time': time, 'lat': lat, 'lon': lon},dims=['time', 'lat', 'lon'])
    ds['qdp'] = ds['qdp'] + -1*temp # model qflux must have opposite sign!
    ds.qdp.to_netcdf(newfilename,mode='a')
    ds.close()




