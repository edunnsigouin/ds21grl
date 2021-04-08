"""
Calculates daily zonally and vertically integrated transient moisture transport 
as a function of latitude and wavenumber for a given aquaplanet simulation
following Graversen and Burtu (2016) QJRMS.
The transient component is calculated by removing the monthly climatological 
stationary wave component from the daily eddy transport.
"""

import numpy                 as np
import xarray                as xr
from  ds21grl.misc           import get_dim_exp
from  ds21grl.transportGB16  import calc_ykt_daily_VQ_trans,write_ykt_daily_transport
from  ds21grl.config         import data_name,dir_processed

# INPUT -----------------------------------------------------------   
data_name_local = data_name[1:10]
var             = 'VQ'
flag            = 'trans'
write2file      = 0
# -----------------------------------------------------------------     

for exp in data_name_local:

    print('dataset: ' + exp)

    # get dimensions
    dim = get_dim_exp(exp)
        
    # define paths      
    dir_in  = dir_processed + exp + '/'
    dir_out = dir_processed + exp + '/'

    # calculate transient moisture transport
    data = calc_ykt_daily_VQ_trans(dir_in,dim)

    # write2file
    write_ykt_daily_transport(data,var,flag,dir_out,dim,write2file)
    
