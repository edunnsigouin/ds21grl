"""
Calculates daily zonally and vertically integrated moisture transport                                                        
as a function of latitude and wavenumber for a given aquaplanet simulation
following Graversen and Burtu (2016) QJRMS

WARNING: running this code takes a while (~30s per 73 day chunk file or 
~2.5 min per year on NIRD machine). Best to run one simulation at a time.
"""

import numpy                 as np
import xarray                as xr
from  ds21grl.misc           import get_dim_exp
from  ds21grl.transportGB16  import calc_ykt_daily_VQ_eddy_aqua,write_ykt_daily_transport
from  ds21grl.config         import dir_raw_aqua,data_name,dir_processed 

# INPUT -----------------------------------------------------------                                              
data_name_local = data_name[1:10]
var             = 'VQ'
flag            = 'eddy'
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
    data = calc_ykt_daily_VQ_eddy_aqua(dir_in,dim)

    # write 2 file
    write_ykt_daily_transport(data,var,flag,dir_out,dim,write2file)

    

