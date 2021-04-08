"""
Plots figure 02: 
(a,b) climatological annual yk of vertically
and zonally integrated moisture transport for erai and 
an aquaplanet control simulation.
(c,d) yt correlation of vertically and zonally integrated eddy 
moisture transport at 70N with zonal-mean temperature at 850 hPa
for erai and an aquaplanet control simulation.
"""

import numpy           as np
import xarray          as xr
from matplotlib        import pyplot as plt
from  ds21grl          import dim_aqua,dim_erai
from ds21grl.config    import data_name,dir_interim,dir_fig

# INPUT ----------------------------------------------------------- 
season          = 'ANNUAL'
write2file      = 1
# ----------------------------------------------------------------- 

# read moisture transport data 
filename1      = dir_interim + data_name[0] + '/yk_zint_vint_ml_clim_VQ_eddy_' + season +'_' + dim_erai.timestamp + '.nc'
filename2      = dir_interim + data_name[1] + '/yk_zint_vint_ml_clim_VQ_eddy_' + season +'_' + dim_aqua.timestamp + '.nc'
ds1            = xr.open_dataset(filename1)
ds2            = xr.open_dataset(filename2)
VQ_erai        = ds1['VQ'].values 
VQ_aqua        = ds2['VQ'].values
ds1.close()
ds2.close()

# read correlation data
filename1   = dir_interim + data_name[0] + '/yt_corr_nbs5000_VQ_k1-40_70N_with_zm_T850_ml_' + dim_erai.timestamp + '.nc'
filename2   = dir_interim + data_name[1] + '/yt_corr_nbs5000_VQ_k1-40_70N_with_zm_T850_ml_' + dim_aqua.timestamp + '.nc'
ds1         = xr.open_dataset(filename1)
ds2         = xr.open_dataset(filename2)
corr_erai   = ds1['corr'].values
corr_aqua   = ds2['corr'].values
sig_erai    = ds1['sig'].values
sig_aqua    = ds2['sig'].values
lag         = ds1['lag'].values
ds1.close()
ds2.close()


# Plot
clevs1     = np.arange(0.01,0.45,0.04)
cmap1      = plt.cm.get_cmap("Reds")
cmap1.set_under('white')   
clevs2     = np.arange(-0.45,0.50,0.05)
cmap2      = 'RdBu_r'
corr_aqua  = np.flip(np.swapaxes(corr_aqua,0,1),axis=1)
sig_aqua   = np.flip(np.swapaxes(sig_aqua,0,1),axis=1)
corr_erai  = np.flip(np.swapaxes(corr_erai,0,1),axis=1)
sig_erai   = np.flip(np.swapaxes(sig_erai,0,1),axis=1)
figsize    = np.array([11,8])
fontsize   = 12
fig,axes   = plt.subplots(nrows=2,ncols=2,figsize=(figsize[0],figsize[1]))
axes       = axes.ravel()

plt.subplots_adjust(hspace=0.3,wspace=0.225,left=0.1,right=0.975,top=0.9,bottom=0.1)

# erai VQ
p = axes[0].contourf(dim_erai.wavenumber,dim_erai.lat,VQ_erai,levels=clevs1,cmap=cmap1,extend='both')
axes[0].set_yticks(np.arange(0,100,10))
axes[0].set_xticks(np.arange(1,14,1))
axes[0].set_yticklabels([0,'','',30,'','',60,'','',90],fontsize=fontsize)
axes[0].set_xticklabels([1,'',3,'',5,'',7,'',9,'',11,'',13],fontsize=fontsize)
axes[0].set_ylabel('latitude',fontsize=fontsize)
axes[0].set_xlabel('zonal wavenumber (k)',fontsize=fontsize)
axes[0].set_title('(a)',fontsize=fontsize)
axes[0].set_ylim([0,90])                                                                                              
axes[0].set_xlim([1,13])

cb = fig.colorbar(p, ax=axes[0], orientation='vertical',ticks=clevs1[0::2],pad=0.025,aspect=15)
cb.ax.set_title('[PW]',fontsize=fontsize)
cb.ax.tick_params(labelsize=fontsize,size=0)


# aqua VQ 
p = axes[1].contourf(dim_aqua.wavenumber,dim_aqua.lat,VQ_aqua,levels=clevs1,cmap=cmap1,extend='both')
axes[1].set_yticks(np.arange(0,100,10))
axes[1].set_xticks(np.arange(1,14,1))
axes[1].set_yticklabels([0,'','',30,'','',60,'','',90],fontsize=fontsize)
axes[1].set_xticklabels([1,'',3,'',5,'',7,'',9,'',11,'',13],fontsize=fontsize)
axes[1].set_ylabel('latitude',fontsize=fontsize)
axes[1].set_xlabel('zonal wavenumber (k)',fontsize=fontsize)
axes[1].set_title('(b)',fontsize=fontsize)
axes[1].set_ylim([0,90])
axes[1].set_xlim([1,13])

cb = fig.colorbar(p, ax=axes[1], orientation='vertical',ticks=clevs1[0::2],pad=0.025,aspect=15)
cb.ax.set_title('[PW]',fontsize=fontsize)
cb.ax.tick_params(labelsize=fontsize,size=0)


# erai correlation 
p = axes[2].contourf(lag,dim_erai.lat,corr_erai,levels=clevs2,cmap=cmap2,extend='both')
axes[2].contourf(lag,dim_erai.lat,sig_erai,levels=1,colors='none',hatches=["", "///"])
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

cb = fig.colorbar(p, ax=axes[2], orientation='vertical',ticks=clevs2[1::4],pad=0.025,aspect=15)
cb.ax.set_title('[r]',fontsize=fontsize)
cb.ax.tick_params(labelsize=fontsize,size=0)


# aqua correlation 
p = axes[3].contourf(lag,dim_aqua.lat,corr_aqua,levels=clevs2,cmap=cmap2,extend='both')
axes[3].contourf(lag,dim_aqua.lat,sig_aqua,levels=1,colors='none',hatches=["", "///"])
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

cb = fig.colorbar(p, ax=axes[3], orientation='vertical',ticks=clevs2[1::4],pad=0.025,aspect=15)
cb.ax.set_title('[r]',fontsize=fontsize)
cb.ax.tick_params(labelsize=fontsize,size=0)


# extra labels
axes[0].text(-0.19, 0.5,r'$ \langle \overline{[v^{*}q^{*}]} \rangle $',fontsize=fontsize*1.5,fontweight='normal',\
             va='bottom', ha='center',rotation='vertical',rotation_mode='anchor',transform=axes[0].transAxes)
axes[0].text(0.5, 1.1,'reanalysis',fontsize=fontsize*1.5,fontweight='normal', va='bottom', ha='center',rotation='horizontal',\
             rotation_mode='anchor',transform=axes[0].transAxes)

axes[1].text(0.5, 1.1,'control',fontsize=fontsize*1.5,fontweight='normal',va='bottom', ha='center',rotation='horizontal',\
             rotation_mode='anchor',transform=axes[1].transAxes)

axes[2].text(-0.19, 0.5,r'corr $\langle [v^{*} q^{*}] \rangle_{70N}$ & $[T]_{850hPa}$',fontsize=fontsize*1.5,fontweight='normal',\
             va='bottom', ha='center',rotation='vertical',rotation_mode='anchor',transform=axes[2].transAxes)


if write2file == 1:
    plt.savefig(dir_fig + 'fig_02.pdf')
    
plt.show()



