"""
Plots figure S5:
yt correlation of zonal-mean downward long wave radiation at the surface (top) 
and longwave cloud radiative forcing at the surface (bottom) 
with vertically and zonally integrated eddy moisture transport at 70N for 
(left) reanalysis data (left) and aquaplanet control simulation data (right).
"""

import numpy           as np
import xarray          as xr
from matplotlib        import pyplot as plt
from  ds21grl          import dim_aqua,dim_erai
from ds21grl.config    import data_name,dir_interim,dir_fig

# INPUT -----------------------------------------------------------   
write2file = 1
# ----------------------------------------------------------------- 

# read correlation data for downwar longwave radiation
filename1   = dir_interim + data_name[0] + '/yt_corr_nbs5000_VQ_k1-40_70N_with_zm_FLDS_sfc_' + dim_erai.timestamp + '.nc'
filename2   = dir_interim + data_name[1] + '/yt_corr_nbs5000_VQ_k1-40_70N_with_zm_FLDS_sfc_' + dim_aqua.timestamp + '.nc'
ds1         = xr.open_dataset(filename1)
ds2         = xr.open_dataset(filename2)
corr_erai_1 = ds1['corr'].values
corr_aqua_1 = ds2['corr'].values
sig_erai_1  = ds1['sig'].values
sig_aqua_1  = ds2['sig'].values
lag         = ds1['lag'].values
ds1.close()
ds2.close()

# read correlation data for longwave cloud forcing                                 
filename1   = dir_interim + data_name[0] + '/yt_corr_nbs5000_VQ_k1-40_70N_with_zm_LWCFS_sfc_' + dim_erai.timestamp + '.nc'
filename2   = dir_interim + data_name[1] + '/yt_corr_nbs5000_VQ_k1-40_70N_with_zm_LWCFS_sfc_' + dim_aqua.timestamp + '.nc'
ds1         = xr.open_dataset(filename1)
ds2         = xr.open_dataset(filename2)
corr_erai_2 = ds1['corr'].values
corr_aqua_2 = ds2['corr'].values
sig_erai_2  = ds1['sig'].values
sig_aqua_2  = ds2['sig'].values
lag         = ds1['lag'].values
ds1.close()
ds2.close()


# Plot
corr_aqua_1    = np.flip(np.swapaxes(corr_aqua_1,0,1),axis=1)
corr_aqua_2    = np.flip(np.swapaxes(corr_aqua_2,0,1),axis=1)
corr_erai_1    = np.flip(np.swapaxes(corr_erai_1,0,1),axis=1)
corr_erai_2    = np.flip(np.swapaxes(corr_erai_2,0,1),axis=1)
sig_aqua_1     = np.flip(np.swapaxes(sig_aqua_1,0,1),axis=1)
sig_aqua_2     = np.flip(np.swapaxes(sig_aqua_2,0,1),axis=1)
sig_erai_1     = np.flip(np.swapaxes(sig_erai_1,0,1),axis=1)
sig_erai_2     = np.flip(np.swapaxes(sig_erai_2,0,1),axis=1)
clevs          = np.arange(-0.45,0.50,0.05)
cmap           = 'RdBu_r'
figsize        = np.array([11,8])
fontsize       = 12
fig,axes       = plt.subplots(nrows=2,ncols=2,figsize=(figsize[0],figsize[1]))
axes           = axes.ravel()

plt.subplots_adjust(hspace=0.3,wspace=0.225,left=0.1,right=0.975,top=0.9,bottom=0.1)

# erai FLDS
p = axes[0].contourf(lag,dim_erai.lat,corr_erai_1,levels=clevs,cmap=cmap,extend='both')
axes[0].contourf(lag,dim_erai.lat,sig_erai_1,levels=1,colors='none',hatches=["", "///"])
plt.rcParams['hatch.linewidth'] = 0.25
axes[0].set_yticks(np.arange(0,100,10))
axes[0].set_xticks(np.arange(lag[0],lag[-1]+1,1))
axes[0].set_yticklabels([0,'','',30,'','',60,'','',90],fontsize=fontsize)
axes[0].set_xticklabels([-10,'','','','',-5,'','','','',0,'','','','',5,'','','','',10],fontsize=fontsize)
axes[0].set_ylabel('latitude',fontsize=fontsize)
axes[0].set_xlabel('lag (days)',fontsize=fontsize)
axes[0].set_title('(a)',fontsize=fontsize)   
axes[0].set_ylim([0,90])                                                                                              
axes[0].set_xlim([lag[0],lag[-1]])

cb = fig.colorbar(p, ax=axes[0], orientation='vertical',ticks=clevs[1::4],pad=0.025,aspect=15)
cb.ax.set_title('[r]',fontsize=fontsize)
cb.ax.tick_params(labelsize=fontsize,size=0)

# erai LWCF_sfc
p = axes[2].contourf(lag,dim_erai.lat,corr_erai_2,levels=clevs,cmap=cmap,extend='both')
axes[2].contourf(lag,dim_erai.lat,sig_erai_2,levels=1,colors='none',hatches=["", "///"])
plt.rcParams['hatch.linewidth'] = 0.25
axes[2].set_yticks(np.arange(0,100,10))
axes[2].set_xticks(np.arange(lag[0],lag[-1]+1,1))
axes[2].set_yticklabels([0,'','',30,'','',60,'','',90],fontsize=fontsize)
axes[2].set_xticklabels([-10,'','','','',-5,'','','','',0,'','','','',5,'','','','',10],fontsize=fontsize)
axes[2].set_ylabel('latitude',fontsize=fontsize)
axes[2].set_xlabel('lag (days)',fontsize=fontsize)
axes[2].set_title('(c)',fontsize=fontsize)	
axes[2].set_ylim([0,90])
axes[2].set_xlim([lag[0],lag[-1]])

cb = fig.colorbar(p, ax=axes[2], orientation='vertical',ticks=clevs[1::4],pad=0.025,aspect=15)
cb.ax.set_title('[r]',fontsize=fontsize)
cb.ax.tick_params(labelsize=fontsize,size=0)


# aqua FLDS
p = axes[1].contourf(lag,dim_aqua.lat,corr_aqua_1,levels=clevs,cmap=cmap,extend='both')
axes[1].contourf(lag,dim_aqua.lat,sig_aqua_1,levels=1,colors='none',hatches=["", "///"])
plt.rcParams['hatch.linewidth'] = 0.25
axes[1].set_yticks(np.arange(0,100,10))
axes[1].set_xticks(np.arange(lag[0],lag[-1]+1,1))
axes[1].set_yticklabels([0,'','',30,'','',60,'','',90],fontsize=fontsize)
axes[1].set_xticklabels([-10,'','','','',-5,'','','','',0,'','','','',5,'','','','',10],fontsize=fontsize)
axes[1].set_ylabel('latitude',fontsize=fontsize)
axes[1].set_xlabel('lag (days)',fontsize=fontsize)
axes[1].set_title('(b)',fontsize=fontsize)	
axes[1].set_ylim([0,90])
axes[1].set_xlim([lag[0],lag[-1]])

cb = fig.colorbar(p, ax=axes[1], orientation='vertical',ticks=clevs[1::4],pad=0.025,aspect=15)
cb.ax.set_title('[r]',fontsize=fontsize)
cb.ax.tick_params(labelsize=fontsize,size=0)


# aqua LWCF_sfc 
p = axes[3].contourf(lag,dim_aqua.lat,corr_aqua_2,levels=clevs,cmap=cmap,extend='both')
axes[3].contourf(lag,dim_aqua.lat,sig_aqua_2,levels=1,colors='none',hatches=["", "///"])
plt.rcParams['hatch.linewidth'] = 0.25
axes[3].set_yticks(np.arange(0,100,10))
axes[3].set_xticks(np.arange(lag[0],lag[-1]+1,1))
axes[3].set_yticklabels([0,'','',30,'','',60,'','',90],fontsize=fontsize)
axes[3].set_xticklabels([-10,'','','','',-5,'','','','',0,'','','','',5,'','','','',10],fontsize=fontsize)
axes[3].set_ylabel('latitude',fontsize=fontsize)
axes[3].set_xlabel('lag (days)',fontsize=fontsize)
axes[3].set_title('(d)',fontsize=fontsize)
axes[3].set_ylim([0,90])
axes[3].set_xlim([lag[0],lag[-1]])

cb = fig.colorbar(p, ax=axes[3], orientation='vertical',ticks=clevs[1::4],pad=0.025,aspect=15)
cb.ax.set_title('[r]',fontsize=fontsize)
cb.ax.tick_params(labelsize=fontsize,size=0)


# extra labels
axes[0].text(-0.19,0.5,r'corr $\langle [v^{*} q^{*}] \rangle_{70N}$ & $[DLWR]_{sfc}$',fontsize=fontsize*1.25,fontweight='normal',\
             va='bottom', ha='center',rotation='vertical',rotation_mode='anchor',transform=axes[0].transAxes)

axes[0].text(0.5,1.1,'reanalysis',fontsize=fontsize*1.25,fontweight='normal', va='bottom', ha='center',rotation='horizontal',\
             rotation_mode='anchor',transform=axes[0].transAxes)

axes[1].text(0.5,1.1,'control',fontsize=fontsize*1.25,fontweight='normal',va='bottom', ha='center',rotation='horizontal',\
             rotation_mode='anchor',transform=axes[1].transAxes)

axes[2].text(-0.19,0.5,r'corr $\langle [v^{*} q^{*}] \rangle_{70N}$ & $[LWCRF]_{sfc}$',fontsize=fontsize*1.25,fontweight='normal',\
             va='bottom', ha='center',rotation='vertical',rotation_mode='anchor',transform=axes[2].transAxes)

if write2file == 1:
    plt.savefig(dir_fig + 'fig_S5.pdf')
    
plt.show()


