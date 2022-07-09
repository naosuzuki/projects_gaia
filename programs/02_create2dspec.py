import numpy
from gaiaxpy import calibrate
from gaiaxpy import convert
from gaiaxpy import plot_spectra
import sys
import pandas as pd
import fitsio
from astropy.io import fits

def read_xpspectra(csvfilelist):

   count=0
   #for i in range(len(csvfilelist)):
   for i in range(2):
      df=pd.read_csv(csvfilelist[i])
      print(i,len(df))
      count+=len(df)
   print(count)

   npix=251
   imageflux   =numpy.zeros((count,npix),dtype=numpy.float32)
   imagefluxerr=numpy.zeros((count,npix),dtype=numpy.float32)
   source_id_list=numpy.zeros(count,dtype=numpy.int64)

#  wavelength range 330-1050 nm
#  wave_min=10.0**2.5186             =330.05
#  wave_max=10.0**(2.5186+0.002*251) =1048.57
   sampling =numpy.zeros(npix)
   for i in range(npix):
      sampling[i]=10**(2.5186+0.002*i)
   
   #gaia_source = df.iloc[[i]] # Select row with index 0
   count=0
   #for i in range(len(csvfilelist)):
   for i in range(2):
      df=pd.read_csv(csvfilelist[i])
      idlist=df['source_id']
      xp_spectra, sampling = calibrate(df,sampling=sampling, save_file=False)
      for j in range(len(df)):
         imageflux[count+j,:]   =xp_spectra['flux'][i]*1.0e17
         imagefluxerr[count+j,:]=xp_spectra['flux_error'][i]*1.0e17
         source_id_list[count+j]=df.iloc[i,'source_id']
      count+=len(df)
      print('writing fits',i)
      del df

   hdu1=fits.PrimaryHDU(imageflux)
   hdu2=fits.ImageHDU(imagefluxerr)
   #hdulist=fits.HDUList([hdu1,hdu2,tbhdu])
   hdulist=fits.HDUList([hdu1,hdu2])
   prihdr=hdulist[0].header
   col1=fits.Column(name='source_id',format='J',array=source_id_list)
   #fitsio.write('gaiaxp.fits',imageflux)

#csvfile='../data/XP_CONTINUOUS_COMBINED.csv'
csvfilelist=['../data/gaiadr3xp_sdssdr17_01.csv',\
'../data/gaiadr3xp_sdssdr17_02.csv',\
'../data/gaiadr3xp_sdssdr17_03.csv',\
'../data/gaiadr3xp_sdssdr17_04.csv',\
'../data/gaiadr3xp_sdssdr17_05.csv',\
'../data/gaiadr3xp_sdssdr17_06.csv',\
'../data/gaiadr3xp_sdssdr17_07.csv',\
'../data/gaiadr3xp_sdssdr17_08.csv',\
'../data/gaiadr3xp_sdssdr17_09.csv',\
'../data/gaiadr3xp_sdssdr17_10.csv',\
'../data/gaiadr3xp_sdssdr17_11.csv',\
'../data/gaiadr3xp_sdssdr17_12.csv',\
'../data/gaiadr3xp_sdssdr17_13.csv']
read_xpspectra(csvfilelist)
