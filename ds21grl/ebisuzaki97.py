"""
Collection of functions to calculate lag correlations
and significance following Ebisuzaki 97 JCLIM
"""


def phaseran(recblk, nsurr,ax):
    """ Phaseran by Carlos Gias: http://www.mathworks.nl/matlabcentral/fileexchange/32621-phase-randomization/content/phaseran.m
    Args:
        recblk (2D array): Row: time sample. Column: recording.
            An odd number of time samples (height) is expected.
            If that is not the case, recblock is reduced by 1 sample before the surrogate data is created.
            The class must be double and it must be nonsparse.
        nsurr (int): is the number of image block surrogates that you want to generate.
    Returns:
        surrblk: 3D multidimensional array image block with the surrogate datasets along the third dimension
    Reference:
        Prichard, D., Theiler, J. Generating Surrogate Data for Time Series with Several Simultaneously Measured Variables (1994)
        Physical Review Letters, Vol 73, Number 7
    NOTE: Extended to xy data and converted to python by Etienne Dunn-Sigouin 
    """
    import numpy      as np
    from ds21grl.misc import AxRoll
    
    # make sure time dimension is axis=0
    recblk = AxRoll(recblk,ax)
    
    # Get time length
    nfrms = recblk.shape[0]

    # force data to have odd time length
    if nfrms % 2 == 0:
        nfrms  = nfrms-1
        recblk = recblk[0:nfrms]
        
    # define fft frequency intervals
    len_ser = int((nfrms-1)/2)
    interv1 = np.arange(1, len_ser+1)
    interv2 = np.arange(len_ser+1, nfrms)

    # Fourier transform of the original dataset
    fft_recblk = np.fft.fft(recblk,axis=0)

    # Create nsurr timeseries of random numbers (0,1)
    # Also tile fft array for later
    if np.ndim(recblk) == 1:
        ph_rnd          = np.random.rand(len_ser,nsurr)
        fft_recblk_surr = np.tile(fft_recblk[None,:],(nsurr,1))
    elif np.ndim(recblk) == 2:    
        ph_rnd          = np.random.rand(len_ser,recblk.shape[1],nsurr)
        fft_recblk_surr = np.tile(fft_recblk[None,:],(nsurr,1,1))
    elif np.ndim(recblk) == 3:
        ph_rnd          = np.random.rand(len_ser,recblk.shape[1],recblk.shape[2],nsurr)
        fft_recblk_surr = np.tile(fft_recblk[None,:],(nsurr,1,1,1))
    fft_recblk_surr = np.moveaxis(fft_recblk_surr,0,-1)

    # Create the random phases for all the time series
    ph_interv1 = np.exp(2*np.pi*1j*ph_rnd)
    ph_interv2 = np.conj(np.flipud(ph_interv1))

    # Randomize all the time series simultaneously 
    fft_recblk_surr[interv1,:] = fft_recblk_surr[interv1,:] * ph_interv1
    fft_recblk_surr[interv2,:] = fft_recblk_surr[interv2,:] * ph_interv2

    # Inverse transform
    surrblk = np.real(np.fft.ifft(fft_recblk_surr,axis=0))
        
    return surrblk



def remove_mean(data,ax):
    """
    function that removes mean defined across
    given axis from entire data array
    """
    import numpy      as np
    from ds21grl.misc import AxRoll
    
    if np.ndim(data) == 1:
        data = data - np.mean(data)
    else:
        data = AxRoll(data,ax)
        mean = np.mean(data,axis=ax)
        for i in range(0,data.shape[ax]):
            data[i,:] = data[i,:] - mean[:]
        data = AxRoll(data,ax,invert=True)
    
    return data



def cross_correlate_ndim(x,y,maxlag,ax):
    """ 
    Calculates lag cross-correlation  
    between two n dim arrays along a specified axis.
    Truncates to +-maxlag
    NOTE: x and y arrays must be same dimensions
    """
    import numpy      as np
    from scipy        import signal
    from ds21grl.misc import AxRoll
    
    # put lag correlation axis on axis=0
    x = AxRoll(x,ax)
    y = AxRoll(y,ax)
    
    # center time series  
    x = remove_mean(x,0)
    y = remove_mean(y,0)
    
    # calc cross correlation
    corr  = signal.fftconvolve(x, np.flip(y,axis=0), mode='full', axes=0)
    corr  = corr/x.shape[0]/np.std(x,axis=0)/np.std(y,axis=0)

    # extract desired lags
    temp1  = np.arange(-(x.shape[0]-1),0,1)
    temp2  = np.arange(0,x.shape[0],1)
    lag    = np.concatenate((temp1, temp2), axis=0)
    index  = (lag >= -1*maxlag) & (lag <= maxlag)
    lag    = lag[index]
    if np.ndim(x) > 1:
        corr = corr[index,:]
    else:
        corr = corr[index]
        
    return corr,lag




def cross_correlate_ndim_sig(x1,x2,maxlag,nbs,sigthresh,ax):
    """                                                                                                      
    Wrapper for cross_correlate_ndim. Also calculates 
    significance following randomized phase procedure from Ebisuzaki 97. 
    Significant = 1 and not significant = 0.
    NOTE: x and y arrays must be same dimensions 
    """

    import numpy      as np
    from ds21grl.misc import AxRoll
    
    # make time dimension axis=0
    x1 = AxRoll(x1,ax)
    x2 = AxRoll(x2,ax)
    
    # force timeseries to be odd
    # (because of phaseran fxn)
    if x1.shape[ax] % 2 == 0:
        x1 = x1[0:-1]
        x2 = x2[0:-1]

    # calculate lag correlation
    [corr,lag] = cross_correlate_ndim(x1,x2,maxlag,ax)

    # calculate boostrapped time series with
    # randomized phases
    x2 = phaseran(x2,nbs,ax)    
    if np.ndim(x1) == 3:
        x1 = np.tile(x1[None,:],(nbs,1,1,1))
    elif np.ndim(x1) == 2:
        x1 = np.tile(x1[None,:],(nbs,1,1))
    elif np.ndim(x1) == 1:
        x1 = np.tile(x1[None,:],(nbs,1))
        
    x1 = np.moveaxis(x1,0,-1) # x1 must have same shape as x2
    [corr_bs,lag] = cross_correlate_ndim(x1,x2,maxlag,ax)

    # calculate significant correlations (two sided test)
    # using PDF of bootstrapped correlations
    sig         = np.zeros((corr.shape))
    ptile1      = np.percentile(corr_bs,(100-sigthresh)/2,axis=-1)
    ptile2      = np.percentile(corr_bs,sigthresh+(100-sigthresh)/2,axis=-1)
    index       = (corr > ptile1) & (corr < ptile2)
    sig[index]  = 1

    return corr,sig,lag



def write_yt_daily(corr,sig,lag,filename,dir_out,dim,write2file):
    """
    Writes yt lag correlation data to file
    """
    import numpy  as np
    import xarray as xr
    
    if write2file == 1:
        output = xr.Dataset(data_vars={'corr':  (('lag','lat'), corr.astype(np.float32)),
                                       'sig':  (('lag','lat'), sig.astype(np.float32))},
                            coords={'lag': lag,'lat': dim.lat})
        output.corr.attrs['units'] = 'unitless'
        output.sig.attrs['units']  = 'unitless'
        output.to_netcdf(dir_out + filename)
    
    return
