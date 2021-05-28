1. Adapt the extracted spectrum for MOLECFIT and output WAVE_INCLUDE.fits, for instance:

`python3 CRIRESadaptData4Molecfit.py obs/cr2res_obs_nodding_extractedA.fits obs/Pi2Ori-210220-K2217.fits`

2. Make sure that **model.sof**, **calctrans.sof**, and **model.sof** files are correct (right SCIENCE file)

3. run **molecfit.sh**

---

If you want to plot the result from `molecfit_model`:
```
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import glob
f = 'MODEL/BEST_FIT_MODEL.fits'
hd = fits.open(f)
for i in range(len(hd)-1):
	ii = np.argsort(hd[1].data['lambda'])
	plt.plot(hd[i+1].data['lambda'][ii], hd[i+1].data['mflux'][ii], color="C0", linewidth=2)
	plt.plot(hd[i+1].data['lambda'][ii], hd[i+1].data['flux'][ii], color="C1", linewidth=1)
plt.xlabel("Wavelength [nm]")
plt.ylabel("Normalized flux")
plt.show()
```
