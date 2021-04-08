"""
Plots figure 03: 
(a,b): yk of the change in vertically and zonally integrated moisture transport
for two aquaplanet model experiments with the control simulation climatology
overlayed 
(c,d): percent change relative to control of different variables in different 
aquaplanet simulations
"""

import numpy           as np
import xarray          as xr
from matplotlib        import pyplot as plt
from  ds21grl          import dim_aqua,dim_erai
from ds21grl           import dim_aqua as dim
from ds21grl.config    import data_name,dir_interim,dir_fig

# INPUT -----------------------------------------------------------  
season          = 'ANNUAL'
ilat            = 70
write2file      = 1
# -----------------------------------------------------------------

# read anomalous yk clim transport data for experiments L+ U+
# and total clim transport from control 
filename1      = dir_interim + data_name[2] + '/yk_zint_vint_ml_clim_anom_VQ_eddy_' + season +'_' + dim.timestamp + '.nc'
filename2      = dir_interim + data_name[4] + '/yk_zint_vint_ml_clim_anom_VQ_eddy_' + season +'_' + dim.timestamp + '.nc'
filename3      = dir_interim + data_name[1] + '/yk_zint_vint_ml_clim_VQ_eddy_' + season +'_' + dim.timestamp + '.nc'
ds1            = xr.open_dataset(filename1)
ds2            = xr.open_dataset(filename2)
ds3            = xr.open_dataset(filename3)
VQ_L           = ds1['VQ'].values
sig_L          = ds1['sig'].values
VQ_U           = ds2['VQ'].values
sig_U          = ds2['sig'].values
VQ_ctl         = ds3['VQ'].values
ds1.close()
ds2.close()
ds3.close()

# read percentage change data at 70N from different simulations
filename = dir_interim + 'ALL_EXPS/percent_change_' + str(ilat) + 'N.nc'
if season == 'ANNUAL':
    ds = xr.open_dataset(filename).sel(season=0.0,method='nearest')
elif season == 'NDJFM':
    ds = xr.open_dataset(filename).sel(season=1.0,method='nearest')
MN70     = ds['MN'].values
STD70    = ds['STD'].values
ds.close()



# plotting ----------------------------------------------------------------------

# dont plot values oustide smallest contour of control
clevs  = np.arange(0.01,0.49,0.04)
for k in range(0,dim.wavenumber.size):
    for j in range(0,dim.lat.size):
        if VQ_ctl[j,k] <= clevs[0]:
            VQ_L[j,k]  = np.nan
            sig_L[j,k] = np.nan
            VQ_U[j,k]  = np.nan
            sig_U[j,k] = np.nan

order     = np.array([1,3,5,0,2,4,6])
positions = np.array([1,2,3,4,5,6,7]) 
fontsize  = 12
clevs2    = np.arange(-100,110,10)
cmap      = 'RdBu_r'
figsize   = np.array([11,8])
fig       = plt.figure(figsize=(figsize[0],figsize[1]))
ax1       = plt.subplot(2, 2, 1)
ax2       = plt.subplot(2, 2, 2)
ax3       = plt.subplot(2, 1, 2)

plt.subplots_adjust(hspace=0.3,wspace=0.2,left=0.075,right=0.95,top=0.95,bottom=0.1)

# experiment L+
ax1.contour(dim.wavenumber,dim.lat,VQ_ctl,levels=clevs,colors='grey',linewidths=1.0,linestyles='-')
p = ax1.contourf(dim.wavenumber,dim.lat,VQ_L,levels=clevs2,cmap=cmap,extend='both')
ax1.contourf(dim.wavenumber,dim.lat,sig_L,levels=1,colors='none',hatches=["", "///"])
plt.rcParams['hatch.linewidth'] = 0.25
ax1.set_yticks(np.arange(0,100,10))
ax1.set_xticks(np.arange(1,14,1))
ax1.set_yticklabels([0,'','',30,'','',60,'','',90],fontsize=fontsize)
ax1.set_xticklabels([1,'',3,'',5,'',7,'',9,'',11,'',13],fontsize=fontsize)
ax1.set_ylabel('latitude',fontsize=fontsize)
ax1.set_xlabel('zonal wavenumber [k]',fontsize=fontsize)
ax1.set_title(r'(a) L+, $\Delta \langle \overline{[v^{*}q^{*}]} \rangle $',fontsize=fontsize)
ax1.set_ylim([0,90])
ax1.set_xlim([1,13])

cb = fig.colorbar(p, ax=ax1, orientation='vertical',ticks=clevs2[0::2],pad=0.025,aspect=15)
cb.ax.set_title(r'[$\%$]',fontsize=fontsize)
cb.ax.tick_params(labelsize=fontsize,size=0)

# experiment U+
ax2.contour(dim.wavenumber,dim.lat,VQ_ctl,levels=clevs,colors='grey',linewidths=1.0,linestyles='-')
p = ax2.contourf(dim.wavenumber,dim.lat,VQ_U,levels=clevs2,cmap=cmap,extend='both')
ax2.contourf(dim.wavenumber,dim.lat,sig_U,levels=1,colors='none',hatches=["", "///"])
plt.rcParams['hatch.linewidth'] = 0.25
ax2.set_yticks(np.arange(0,100,10))
ax2.set_xticks(np.arange(1,14,1))
ax2.set_yticklabels([0,'','',30,'','',60,'','',90],fontsize=fontsize)
ax2.set_xticklabels([1,'',3,'',5,'',7,'',9,'',11,'',13],fontsize=fontsize)
ax2.set_ylabel('latitude',fontsize=fontsize)
ax2.set_xlabel('zonal wavenumber [k]',fontsize=fontsize)
ax2.set_title(r'(b) U+, $\Delta \langle \overline{[v^{*}q^{*}]} \rangle $',fontsize=fontsize)
ax2.set_ylim([0,90])
ax2.set_xlim([1,13])

cb = fig.colorbar(p, ax=ax2, orientation='vertical',ticks=clevs2[0::2],pad=0.025,aspect=15)
cb.ax.set_title(r'[$\%$]',fontsize=fontsize)
cb.ax.tick_params(labelsize=fontsize,size=0)


# all experiments
for i in range(0,7):
    ax3.errorbar(positions[i]-0.25,MN70[0,order[i]],yerr=2*STD70[0,order[i]],fmt='o',c='k',elinewidth=2)
    ax3.errorbar(positions[i]-0.15,MN70[1,order[i]],yerr=2*STD70[1,order[i]],fmt='o',c='tab:gray',elinewidth=2)
    ax3.errorbar(positions[i]-0.05,MN70[2,order[i]],yerr=2*STD70[2,order[i]],fmt='o',c='tab:blue',elinewidth=2)
    ax3.errorbar(positions[i]+0.05,MN70[3,order[i]],yerr=2*STD70[3,order[i]],fmt='o',c='tab:green',elinewidth=2)
    ax3.errorbar(positions[i]+0.15,MN70[4,order[i]],yerr=2*STD70[4,order[i]],fmt='o',c='tab:red',elinewidth=2)
    ax3.errorbar(positions[i]+0.25,MN70[5,order[i]],yerr=2*STD70[5,order[i]],fmt='o',c='tab:pink',elinewidth=2)
                                                                                                          
label1 = r'$\Delta \langle \overline{[v^{*}q^{*}]} \rangle $'
label2 = r'$\Delta \langle \overline{[v^{*^{\prime}}q^{*^{\prime}}]} \rangle $'
label3 = r'$\Delta \overline{[q]}_{850hPa}$'
label4 = r'(7.3$\%/K)*\Delta \overline{[T]}_{850hPa}$'
label5 = r'$\Delta [v^{*}_{rms}]_{850hPa}$'
label6 = r'$\Delta [v^{*^{\prime}}_{rms}]_{850hPa}$'

ax3.errorbar([],[],[],fmt='o',c='k',elinewidth=2,label=label1)
ax3.errorbar([],[],[],fmt='o',c='tab:gray',elinewidth=2,label=label2)
ax3.errorbar([],[],[],fmt='o',c='tab:blue',elinewidth=2,label=label3)
ax3.errorbar([],[],[],fmt='o',c='tab:green',elinewidth=2,label=label4)
ax3.errorbar([],[],[],fmt='o',c='tab:red',elinewidth=2,label=label5)
ax3.errorbar([],[],[],fmt='o',c='tab:pink',elinewidth=2,label=label6)
ax3.legend(loc='upper left',ncol=3,frameon=False,fontsize=fontsize)

ax3.axhline(y=0, color='k', linestyle='-',linewidth=1)
ax3.set_xticks(positions)
ax3.set_xticklabels(['L-','U-',r'L$_{k1}$','L+','U+','2L+','2U+'],fontsize=fontsize)
ax3.set_yticks(np.arange(-50,80,10))
ax3.set_yticklabels(['','-40','','-20','','0','','20','','40','','60',''],fontsize=fontsize)
ax3.set_title('(c)',fontsize=fontsize)
ax3.set_xlabel('experiment',fontsize=fontsize)
ax3.set_ylabel(r'change at 70$^{\circ}$N [$\%$]',fontsize=fontsize)
ax3.set_ylim([-50,70])


if write2file == 1:
    plt.savefig(dir_fig + 'fig_03.pdf')

plt.show()


