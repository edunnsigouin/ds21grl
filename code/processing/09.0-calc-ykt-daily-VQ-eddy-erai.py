"""                                                                
Calculates daily zonally and vertically integrated moisture transport     
as a function of latitude and wavenumber for reanalysis data
following Graversen and Burtu (2016) QJRMS                                                   
"""

import numpy                 as np
import xarray                as xr
from  ds21grl                import dim_erai as dim
from  ds21grl.transportGB16  import calc_ykt_daily_VQ_eddy_erai,write_ykt_daily_transport
from  ds21grl.config         import dir_raw_erai,data_name,dir_processed

# INPUT -----------------------------------------------------------
data_name_local = data_name[0:1]
var             = 'VQ'
flag            = 'eddy'
write2file      = 0
# -----------------------------------------------------------------  

# define paths  
dir_in  = dir_raw_erai + '/'
dir_out = dir_processed + data_name_local[0] + '/'

# calculate moisture transport            
data = calc_ykt_daily_VQ_eddy_erai(dir_in,dim)

# write 2 file                                                                                                               
write_ykt_daily_transport(data,var,flag,dir_out,dim,write2file)


