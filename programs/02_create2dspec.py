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
   for i in range(len(csvfilelist)):
   #for i in range(2):
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
   coeff0=2.5186+1.0  ; coeff1=0.002

   #gaia_source = df.iloc[[i]] # Select row with index 0
   count=0
   for i in range(len(csvfilelist)):
   #for i in range(2):
      df=pd.read_csv(csvfilelist[i])
      idlist=df['source_id']
      xp_spectra, sampling = calibrate(df,sampling=sampling, save_file=False)
      for j in range(len(df)):
         imageflux[count+j,:]   =xp_spectra['flux'][j]*1.0e17
         imagefluxerr[count+j,:]=xp_spectra['flux_error'][j]*1.0e17
         source_id_list[count+j]=df['source_id'].iloc[j]
      count+=len(df)
      print('writing fits',i)
      del df

   hdu1=fits.PrimaryHDU(imageflux)
   hdu2=fits.ImageHDU(imagefluxerr)

   #prihdr=hdulist[0].header
   col1=fits.Column(name='source_id',format='K',array=source_id_list)
   cols=fits.ColDefs([col1])
   #tbhdu=fits.new_table(cols)
   tbhdu=fits.BinTableHDU.from_columns(cols)
   hdulist=fits.HDUList([hdu1,hdu2,tbhdu])
   hdr=hdulist[0].header
   hdr.set('COEFF0',coeff0)
   hdr.set('COEFF1',coeff1)
   hdr['comment']='Created by Nao Suzuki 2022-07-07'
   hdr['comment']='1st EXT=Flux, 2nd EXT=Flux Err, 3rd source_id'
   hdr['comment']='GAIA DR3 XP spectra x SDSS DR17 Stars'
   hdr['comment']='Wavelength=1.0**(COEFF0+COEFF1*i)'
   #hdulist=fits.HDUList([hdu1])
#  hdulist=fits.HDUList([hdu1,hdu2])
   hdulist.writeto('gaiaxpspec.fits')

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
