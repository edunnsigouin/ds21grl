"""
Plots fig S2:
Specifically, zonal-mean root-mean-square of stationary wave meridional wind 
at 850 hPa for both reanalysis and aquaplanet simulation data for ANNUAL and NDJFM.
NOTE: since the reviewer asked for a measure of interannual variability in 
stationary wave amplitude, here we calculate stationary waves as the annual or
seasonal mean for each year and then calculate the rms over all years. 
"""

import numpy           as np
import xarray          as xr
from matplotlib        import pyplot as plt
from  ds21grl          import dim_aqua,dim_erai
from ds21grl.config    import data_name,dir_interim,dir_fig

# INPUT -----------------------------------------------------------  
ilat            = 70
write2file      = 1
# -----------------------------------------------------------------

# read rms data from experiments L+, 2L+, Lk1 and erai
filename1      = dir_interim + data_name[0] + '/zm_rms_V850_stw_pl_70N_' + dim_erai.timestamp + '.nc'
filename2      = dir_interim + data_name[2] + '/zm_rms_V850_stw_ml_70N_' + dim_aqua.timestamp + '.nc'
filename3      = dir_interim + data_name[6] + '/zm_rms_V850_stw_ml_70N_' + dim_aqua.timestamp + '.nc'
filename4      = dir_interim + data_name[7] + '/zm_rms_V850_stw_ml_70N_' + dim_aqua.timestamp + '.nc'
ds1            = xr.open_dataset(filename1)
ds2            = xr.open_dataset(filename2)
ds3            = xr.open_dataset(filename3)
ds4            = xr.open_dataset(filename4)
rms_erai       = ds1['rms_stw'].values
rms_L          = ds2['rms_stw'].values 
rms_2L         = ds3['rms_stw'].values
rms_Lk1        = ds4['rms_stw'].values


# plotting 
positions = np.array([1,2,3,4])
fontsize  = 12
figsize   = np.array([10,5])

plt.figure(figsize=(figsize[0],figsize[1]))
plt.subplots_adjust(hspace=0.3,wspace=0.2,left=0.075,right=0.95,top=0.95,bottom=0.1)

plt.plot(positions[0],rms_erai[0],'k',marker='o',markersize=10)
plt.plot(positions[1],rms_L[0],'k',marker='o',markersize=10)
plt.plot(positions[2],rms_2L[0],'k',marker='o',markersize=10)
plt.plot(positions[3],rms_Lk1[0],'k',marker='o',markersize=10)

plt.plot(positions[0],rms_erai[1],'tab:blue',marker='o',markersize=10)
plt.plot(positions[1],rms_L[1],'tab:blue',marker='o',markersize=10)
plt.plot(positions[2],rms_2L[1],'tab:blue',marker='o',markersize=10)
plt.plot(positions[3],rms_Lk1[1],'tab:blue',marker='o',markersize=10)

    
plt.plot([],[],'k',marker='o',markersize=10,label='ANN')
plt.plot([],[],'tab:blue',marker='o',markersize=10,label='NDJFM')
plt.legend(loc='lower right',frameon=False,fontsize=fontsize,labelcolor='linecolor',markerscale=0)

plt.xticks(positions,['reanalysis','L+','2L+',r'L$_{k1}$'],fontsize=fontsize)
plt.yticks(np.arange(0,3,0.5),np.arange(0,3,0.5),fontsize=fontsize)
plt.xlabel('experiment',fontsize=fontsize)
plt.ylabel(r'$[\overline{v}^*_{rms}]_{850hPa}$',fontsize=fontsize)

plt.ylim([0,2.5])

if write2file == 1:
    plt.savefig(dir_fig + 'fig_S2.pdf')

plt.show()


