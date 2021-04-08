"""
Plots figure 01: Annual-mean xy SST anomalies relative to control 
with the anomalous qflux overlayed
"""

import numpy           as np
import xarray          as xr
from matplotlib        import pyplot as plt
import cartopy.util    as cutil
import cartopy.crs     as ccrs
from ds21grl           import dim_aqua        as dim
from ds21grl.config    import dir_interim,data_name,dir_fig

# INPUT -----------------------------------------------------------      
data_name_local = data_name[2:9]
var             = 'SST'
season          = 'ANNUAL'
write2file      = 1
# ----------------------------------------------------------------- 

# read anomalies, signficance and q-fluxes 
nexps = len(data_name_local)
data  = np.zeros([dim.lat.size,dim.lon.size,nexps])
sig   = np.zeros([dim.lat.size,dim.lon.size,nexps])
qflux = np.zeros([dim.lat.size,dim.lon.size,nexps])
for i in range(0,nexps):
    dir_in         = dir_interim + data_name_local[i] + '/'
    filename       = 'xy_sfc_clim_anom_' + var + '_' + season + '_' + dim.timestamp + '.nc'
    ds             = xr.open_dataset(dir_in + filename)
    data[:,:,i]    = ds[var].values
    sig[:,:,i]     = ds['sig'].values
    ds.close()
    
    filename       = 'qflux_anom.nc'
    ds             = xr.open_dataset(dir_in + filename)
    qflux[:,:,i]   = -1*ds['qflux'].values
    ds.close()

# plot 
fontsize                = 11
figsize                 = np.array([10,10]) 
clevs_qflux             = np.concatenate((np.arange(-300,0,30),np.arange(30,300,30)))
clevs                   = np.arange(-10,11,1)
clevs                   = np.tile(clevs,(nexps,1))
clevs[1,:]              = clevs[0,:]*3 # one experiment with larger contour levels
cmap                    = 'RdBu_r'
[data,temp]             = cutil.add_cyclic_point(data,coord=dim.lon,axis=1)
[sig,temp]              = cutil.add_cyclic_point(sig,coord=dim.lon,axis=1)
[qflux,dim.lon]         = cutil.add_cyclic_point(qflux,coord=dim.lon,axis=1)

fig,axes = plt.subplots(nrows=4,ncols=2,figsize=(figsize[0],figsize[1]),\
                        subplot_kw={'projection': ccrs.PlateCarree(central_longitude=225.0)})
axes     = axes.ravel()

for i in range(0,nexps):
    axes[i].set_extent([0, 359.9, -30, 30], ccrs.PlateCarree())
    axes[i].contour(dim.lon,dim.lat,qflux[:,:,i],levels=clevs_qflux,colors='fuchsia',linewidths=1.75,transform=ccrs.PlateCarree())
    p = axes[i].contourf(dim.lon,dim.lat,data[:,:,i],levels=clevs[i,:],cmap=cmap,extend='both',transform=ccrs.PlateCarree())
    axes[i].contourf(dim.lon,dim.lat,sig[:,:,i],levels=1,colors='none',hatches=["", "///"],transform=ccrs.PlateCarree())
    plt.rcParams['hatch.linewidth'] = 0.25
    axes[i].set_yticks(np.arange(-30,45,15))                                                                                  
    axes[i].set_xticks(np.arange(-180,240,60))                                                     
    axes[i].set_yticklabels(np.arange(-30,45,15),fontsize=fontsize)                                       
    axes[i].set_xticklabels(np.arange(-180,240,60),fontsize=fontsize)
    axes[i].set_ylabel('latitude',fontsize=fontsize)                                      
    axes[i].set_xlabel('longitude',fontsize=fontsize)                                                    
    axes[i].set_aspect('auto')                                                                            

    cb = fig.colorbar(p, ax=axes[i], orientation='vertical',ticks=clevs[i,0::4].astype(int),pad=0.025,aspect=10)
    cb.ax.set_title('[K]',fontsize=fontsize)
    cb.ax.tick_params(labelsize=fontsize,size=0)

axes[0].set_title('(a) L+',fontsize=fontsize)
axes[1].set_title('(b) L-',fontsize=fontsize)
axes[2].set_title('(c) U+',fontsize=fontsize)
axes[3].set_title('(d) U-',fontsize=fontsize)
axes[4].set_title('(e) 2L+',fontsize=fontsize)
axes[5].set_title(r'(f) L$_{k1}$',fontsize=fontsize)
axes[6].set_title('(g) 2U+',fontsize=fontsize)
axes[7].set_visible(False)

plt.subplots_adjust(hspace=0.4,wspace=0.15,left=0.075,right=0.975,top=0.975,bottom=0.075)

if write2file == 1:
    plt.savefig(dir_fig + 'fig_01.pdf')

plt.show()


