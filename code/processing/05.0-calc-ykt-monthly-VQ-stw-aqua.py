"""
Calculates monthly climatological zonally and vertically integrated moisture 
transport for stationary waves as a function of latitude and wavenumber for 
a given aquaplanet simulation following Graversen and Burtu (2016) QJRMS.  
Stationary waves are calculated using climatological monthly mass flux and 
specific humidity.

WARNING: running this code takes a while (~8s per 73 day chunk file or 
~35s per year on NIRD machine). Best to run one simulation at a time.  
"""

import numpy                 as np
import xarray                as xr
from  ds21grl.misc           import get_dim_exp
from  ds21grl.transportGB16  import calc_ykt_monthly_VQ_stw_aqua,write_ykt_monthly_clim_transport
from  ds21grl.config         import dir_raw_aqua,dir_processed,data_name

# INPUT -----------------------------------------------------------    
data_name_local = data_name[1:10]
var             = 'VQ'
flag            = 'stw'
write2file      = 0
# -----------------------------------------------------------------

for exp in data_name_local:

    print('dataset: ' + exp)

    # get dimensions
    dim = get_dim_exp(exp)
        
    # define paths 
    dir_in  = dir_raw_aqua + exp + '/'
    dir_out = dir_processed + exp + '/'

    # calculate moisture transport
    data = calc_ykt_monthly_VQ_stw_aqua(dir_in,dim)

    # write 2 file 
    write_ykt_monthly_clim_transport(data,var,flag,dir_out,dim,write2file)
    

