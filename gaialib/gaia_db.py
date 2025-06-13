import sys
import os
import string
import numpy
import fitsio
import pandas as pd

## Written by Nao Suzuki
# 2022-07-21 (Thu) 

class GAIAXP:
      def __init__(self,fitsfilename):
          self.fitsfilename=fitsfilename
          h=fitsio.read_header(self.fitsfilename,ext=0)
          xptable=fitsio.read(self.fitsfilename, ext=2)
          self.source_id_list=xptable['source_id'][:]
          self.ra_list       =xptable['RA'][:]
          self.dec_list      =xptable['DEC'][:]
          self.thing_id_list =xptable['thing_id'][:]
          self.g_mag_list    =xptable['g_mag'][:]
          self.bp_mag_list   =xptable['bp_mag'][:]
          self.rp_mag_list   =xptable['rp_mag'][:]
          self.bprp_mag_list =xptable['bp_rp'][:]
          self.parallax_list =xptable['parallax'][:]

# This method does not work for big integers : For unknown reasons, big integer is altered
#
#          column_names=['source_id','RA','DEC','thing_id','g_mag',\
#                   'bp_mag','rp_mag','bp_rp','parallax']
#          df_list=[self.source_id_list,self.ra_list,self.dec_list,\
#                   self.thing_id_list,self.g_mag_list,self.bp_mag_list,\
#                   self.rp_mag_list,self.bprp_mag_list,self.parallax_list]
#          df=pd.DataFrame(df_list).transpose()
#          df.columns=column_names

# This method works!   2022-07-26
          df=pd.DataFrame(list(zip(self.source_id_list,self.ra_list,self.dec_list,\
                   self.thing_id_list,self.g_mag_list,self.bp_mag_list,\
                   self.rp_mag_list,self.bprp_mag_list,self.parallax_list)),\
                   columns=['source_id','RA','DEC','thing_id','g_mag',\
                   'bp_mag','rp_mag','bp_rp','parallax'])

          self.df=df

      def readall(self):
          h=fitsio.read_header(self.fitsfilename,ext=0)
          self.nspec=h['NAXIS2']
          self.coeff0=h['COEFF0']
          self.coeff1=h['COEFF1']
          self.npix=h['NAXIS1']
          self.wave=10.0**(self.coeff0+self.coeff1*numpy.arange(self.npix))
          self.wave_plus =10.0**(self.coeff0+self.coeff1*(numpy.arange(self.npix)+0.5))
          self.wave_minus=10.0**(self.coeff0+self.coeff1*(numpy.arange(self.npix)-0.5))
          self.dwave=self.wave_plus-self.wave_minus
          self.wid=int(h['coeff0']/0.0001)+numpy.arange(self.npix)*int(h['coeff1']/0.0001)

          self.fits=fitsio.FITS(self.fitsfilename)
          self.imageflux=self.fits[0][:,:]
          self.imagefluxerr=self.fits[1][:,:]

      def read(self,source_id):
          self.source_id=source_id
          row_number=self.df[self.df['source_id']==source_id].index[0]
          self.flux   =self.imageflux[row_number,:]
          self.fluxerr=self.imagefluxerr[row_number,:]

      def photopoints20(self):
          # Find 20 photometric points from GAIA XP spectrum
          # We have 251 spectral points = 11pix*1 + 12pix*19 = 20 points
          self.ptx=numpy.zeros(20)
          self.pty=numpy.zeros(20)
          self.ptyerr=numpy.zeros(20)
          self.ptmask=numpy.zeros(20,dtype=numpy.int32)
          self.ptwid=numpy.zeros(20,dtype=numpy.int32)

          # S/N > 5 criterion for good flux value
          gaia_mask=numpy.where(self.flux/self.fluxerr>5.0,1.0,0)
          # Flux area = flux * dwave
          gaia_maskedflux=self.flux*gaia_mask*self.dwave
          gaia_maskedwave=self.dwave*gaia_mask

          # Calculate the first point
          self.ptx[0]=self.wave[5] ; self.ptwid[0]=self.wid[5]
          if(numpy.sum(gaia_mask[0:10])>0.0):
            self.pty[0]=numpy.sum(gaia_maskedflux[0:10])/numpy.sum(gaia_maskedwave[0:10])
            self.ptwid[0]=self.wid[5]
            self.ptmask[0]=1
            # Error is estimated from the average S/N
            self.ptyerr[0]=self.pty[0]/numpy.average(self.flux[0:10]/self.fluxerr[0:10])
          #else:
          #  self.pty[0]=0.0
          #  self.ptmask[0]=0

          # Calculate 19 points
          for j in range(1,20):
            self.ptx[j]=self.wave[11+j*12]
            self.ptwid[j]=self.wid[11+j*12]
            if(numpy.sum(gaia_mask[(11+j*12):(11+(j+1)*12)])>0.0):
               self.pty[j]=numpy.sum(gaia_maskedflux[(11+j*12):(11+(j+1)*12)])/numpy.sum(gaia_maskedwave[(11+j*12):(11+(j+1)*12)])
               self.ptyerr[j]=self.pty[j]/numpy.average(self.flux[(11+j*12):(11+(j+1)*12)]/self.fluxerr[(11+j*12):(11+(j+1)*12)])
               self.ptmask[j]=1
            else:
               self.ptmask[j]=0

