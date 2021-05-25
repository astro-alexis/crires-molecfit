import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import sys

fi = sys.argv[1] # input file you want to convert
output = sys.argv[2] # name for output file

hd = fits.open(fi) # open data fits file
primary_hdu = hd[0]  # keep primary HDU with header
hdul = fits.HDUList([primary_hdu]) # initialize output HDU list with primary HDU
hdulwinc = fits.HDUList([primary_hdu]) # initialise wave include HDU list
wmin,wmax,map2chip = [], [], [] # initialize empty arrays
jjj = 1 # initialize counter for order/detector

for idet in range(3): # loop on detectors
    chip = 'CHIP'+str(idet+1)+'.INT1' # set up chip name
    data = hd[chip].data # isolate data for given detector
    cp = np.sort([i[0:6] for i in data.dtype.names if "WL" in i]) # find all orders
    for iord in range(len(cp)): # loop on orders
        cpw,cps,cpe = cp[iord]+'WL', cp[iord]+'SPEC', cp[iord]+'ERR'  # set up column name for WAVE SPEC and ERR
        w,s,e = hd[chip].data[cpw], hd[chip].data[cps],hd[1].data[cpe] # isolate WAVE SPEC and ERR
        col1 = fits.Column(name='WAVE', format='D', array=w) # create fits column for WAVE
        col2 = fits.Column(name='SPEC', format='D', array=s) # create fits column for SPEC
        col3 = fits.Column(name='ERR', format='D', array=e) # create fits column for ERR
        table_hdu = fits.BinTableHDU.from_columns([col1, col2, col3]) # create fits table HDU with WAVE SPEC ERR
        hdul.append(table_hdu) # append table HDU to output HDU list
        wmin.append(np.min(w)*0.001) # append wmin for given order to wmin array
        wmax.append(np.max(w)*0.001) # append wmax for giver order to wmax array
        map2chip.append(jjj) # append order counter to map2chip
        jjj+=1

col1winc = fits.Column(name='LOWER_LIMIT', format='D', array=wmin)
col2winc = fits.Column(name='UPPER_LIMIT', format='D', array=wmax)
col3winc = fits.Column(name='MAPPED_TO_CHIP', format='I', array=map2chip)
table_hdu_winc = fits.BinTableHDU.from_columns([col1winc, col2winc,col3winc])
hdulwinc.append(table_hdu_winc)
hdul.writeto(output, overwrite=True)
hdulwinc.writeto('WAVE_INCLUDE.fits', overwrite=True)
