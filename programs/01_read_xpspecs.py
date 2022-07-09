import numpy
from gaiaxpy import calibrate
from gaiaxpy import convert
from gaiaxpy import plot_spectra
import sys
import pandas as pd
import fitsio

def read_xpspectra(csvfile):
   df=pd.read_csv(csvfile)
   print(df.loc[0])
   source_id_list=df['source_id']
   slist=source_id_list.to_numpy()
   print(source_id_list)
   print(slist)
   sys.exit(1)

   npix=251
   imageflux   =numpy.zeros((len(df),npix),dtype=numpy.float32)
   imagefluxerr=numpy.zeros((len(df),npix),dtype=numpy.float32)

#  wavelength range 330-1050 nm
#  wave_min=10.0**2.5186             =330.05
#  wave_max=10.0**(2.5186+0.002*251) =1048.57
   sampling =numpy.zeros(npix)
   for i in range(npix):
      sampling[i]=10**(2.5186+0.002*i)
   
   gaia_source = df.iloc[[i]] # Select row with index 0
   xp_spectra, sampling = calibrate(df,sampling=sampling, save_file=False)
   for i in range(len(df)):
     imageflux[i,:]   =xp_spectra['flux'][i]*1.0e17
     imagefluxerr[i,:]=xp_spectra['flux_error'][i]*1.0e17
   fitsio.write('gaiaxp.fits',imageflux)

csvfile='../data/gaiadr3xp_sdssdr17_01.csv'
read_xpspectra(csvfile)
