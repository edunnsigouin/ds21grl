"""
Plots fig S1:
Specifically, it plots the 6 quantities shown in 
figure 3c except for experiments L+ and L45+ for 
Annual and NDJFM data 
"""

import numpy           as np
import xarray          as xr
from matplotlib        import pyplot as plt
from  ds21grl          import dim_aqua,dim_erai
from ds21grl           import dim_aqua as dim
from ds21grl.config    import data_name,dir_interim,dir_fig

# INPUT ----------------------------------------------------------- 
ilat            = 70
write2file      = 1
# -----------------------------------------------------------------       

# initialize      
MN  = np.zeros((6,4)) 
STD = np.zeros((6,4))

# read percentage change data at 70N from L+ and L+ sensitivity experiments 
filename = dir_interim + 'ALL_EXPS/percent_change_' + str(ilat) + 'N.nc'
ds1      = xr.open_dataset(filename).sel(exp=0.0,season=0.0,method='nearest')
ds2      = xr.open_dataset(filename).sel(exp=7.0,season=0.0,method='nearest')
ds3      = xr.open_dataset(filename).sel(exp=0.0,season=1.0,method='nearest')
ds4      = xr.open_dataset(filename).sel(exp=7.0,season=1.0,method='nearest')
MN[:,0]  = ds1['MN'].values
STD[:,0] = ds1['STD'].values
MN[:,1]  = ds2['MN'].values
STD[:,1] = ds2['STD'].values
MN[:,2]  = ds3['MN'].values
STD[:,2] = ds3['STD'].values
MN[:,3]  = ds4['MN'].values
STD[:,3] = ds4['STD'].values
ds1.close()
ds2.close()
ds3.close()
ds4.close()


# plotting 
positions = np.array([1,2,3,4])
fontsize  = 12
figsize   = np.array([10,5])

plt.figure(figsize=(figsize[0],figsize[1]))
plt.subplots_adjust(hspace=0.3,wspace=0.2,left=0.075,right=0.95,top=0.95,bottom=0.1)

for i in range(0,4):
    plt.errorbar(positions[i]-0.25,MN[0,i],yerr=2*STD[0,i],fmt='o',c='k',elinewidth=2)
    plt.errorbar(positions[i]-0.15,MN[1,i],yerr=2*STD[1,i],fmt='o',c='tab:gray',elinewidth=2)
    plt.errorbar(positions[i]-0.05,MN[2,i],yerr=2*STD[2,i],fmt='o',c='tab:blue',elinewidth=2)
    plt.errorbar(positions[i]+0.05,MN[3,i],yerr=2*STD[3,i],fmt='o',c='tab:green',elinewidth=2)
    plt.errorbar(positions[i]+0.15,MN[4,i],yerr=2*STD[4,i],fmt='o',c='tab:red',elinewidth=2)
    plt.errorbar(positions[i]+0.25,MN[5,i],yerr=2*STD[5,i],fmt='o',c='tab:pink',elinewidth=2)
                                                                                                          
label1 = r'$\Delta \langle \overline{[v^{*}q^{*}]} \rangle $'
label2 = r'$\Delta \langle \overline{[v^{*^{\prime}}q^{*^{\prime}}]} \rangle $'
label3 = r'$\Delta \overline{[q]}_{850hPa}$'
label4 = r'(7.3$\%/K)*\Delta \overline{[T]}_{850hPa}$'
label5 = r'$\Delta [v^{*}_{rms}]_{850hPa}$'
label6 = r'$\Delta [v^{*^{\prime}}_{rms}]_{850hPa}$'

plt.errorbar([],[],[],fmt='o',c='k',elinewidth=2,label=label1)
plt.errorbar([],[],[],fmt='o',c='tab:gray',elinewidth=2,label=label2)
plt.errorbar([],[],[],fmt='o',c='tab:blue',elinewidth=2,label=label3)
plt.errorbar([],[],[],fmt='o',c='tab:green',elinewidth=2,label=label4)
plt.errorbar([],[],[],fmt='o',c='tab:red',elinewidth=2,label=label5)
plt.errorbar([],[],[],fmt='o',c='tab:pink',elinewidth=2,label=label6)
plt.legend(loc='upper left',ncol=3,frameon=False,fontsize=fontsize)

plt.axhline(y=0, color='k', linestyle='-',linewidth=1)
plt.xticks(positions,[r'$\lambda_{d}=\pi/2$,$Q_{0}=150$,ANN',r'$\lambda_{d}=\pi/4$,$Q_{0}=300$,ANN',r'$\lambda_{d}=\pi/2$,$Q_{0}=150$,NDJFM',r'$\lambda_{d}=\pi/4$,$Q_{0}=300$,NDJFM'],fontsize=10)
plt.yticks(np.arange(-10,45,5),['-10','','0','','10','','20','','30','','40'],fontsize=fontsize)
plt.xlabel('experiment L+',fontsize=fontsize)
plt.ylabel(r'change at 70$^{\circ}$N [$\%$]',fontsize=fontsize)
plt.ylim([-10,40])


if write2file == 1:
    plt.savefig(dir_fig + 'fig_S1.pdf')

plt.show()


