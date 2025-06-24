import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import sys
from datetime import date

#today_str = date.today().strftime("%Y-%m-%d")
#today_str = date.today().strftime("%Y%m%d")
#print(today_str)
#sys.exit(1)

# 2025-06-21 DESI DR1 
# 2025-06-19 update
# 2025-06-17 rewritten at FSU

def plot_parallax_SNR_histogram2(csvfile1,csvfile2):
   df=pd.read_csv(csvfile1)
# Extract data above Parallax SNR threshold
   df1=df[df['parallax']>0.0]
   df2=df1[['parallax','parallax_over_error']]
   snr_arr1=df2['parallax_over_error'].to_numpy()

   df3=pd.read_csv(csvfile2)
# Extract data above Parallax SNR threshold
   df4=df3[df3['parallax']>0.0]
   df5=df4[['parallax','parallax_over_error']]
   snr_arr2=df5['parallax_over_error'].to_numpy()

   bins=numpy.arange(20)*10.0
   bin_width = bins[1] - bins[0]
   plt.rcParams["font.family"] = "Times New Roman"
   plt.title('GAIA DR3 vs. SDSS Spectra')
   plt.xlabel('GAIA DR3 Parallax SNR')
   plt.ylabel('Number of Stars')
   plt.xlim([-5,205])
   plt.tick_params(axis='both',which='both',direction='in') 
   plt.ylim([1.2,4.0e5])

   plt.hist(snr_arr1,bins=bins-bin_width/5,log=True,align='mid',width=bin_width/2,color='b',alpha=0.5,label='SDSS DR8')
   plt.hist(snr_arr2,bins=bins+bin_width/5,log=True,align='mid',width=bin_width/2,color='r',alpha=0.5,label='SDSS DR17')
   plt.legend()
   plt.savefig('20250619_GAIADR3vsSDSS_histogram.png')

def plot_parallax_SNR_histogram(csvfile):
   df=pd.read_csv(csvfile)
# Extract data above Parallax SNR threshold
   df1=df[df['parallax']>0.0]
   df2=df1[['parallax','parallax_over_error']]
   snr_arr=df2['parallax_over_error'].to_numpy()

   bins=numpy.arange(20)*10.0
   plt.rcParams["font.family"] = "Times New Roman"
   plt.title('GAIA DR3')
   plt.xlabel('GAIA DR3 SNR')
   plt.ylabel('Number of Stars')
   plt.xlim([-5,205])
   plt.tick_params(axis='both',which='both',direction='in') 
   plt.ylim([1.2,4.0e5])
   plt.hist(snr_arr,bins,log=True,align='left',rwidth=0.9,color='r')
   plt.savefig('histexp.png')

def plot_HRdiagramSNR(csvfile,snr,sdssdr,flag_binary):
   df=pd.read_csv(csvfile)
# Extract data above Parallax SNR threshold
# SNR Condition
# Binary Exclusion is added on 6/20/2025
   df1=df[(df['parallax_over_error']>=snr) & (df['parallax']>0.0) \
   & (df['non_single_star']==False) & (df['ruwe']<1.4) \
   & (df['phot_variable_flag']!='VARIABLE')]
# Extract 4 columns
   df2=df1[['phot_g_mean_mag','bp_rp','parallax','parallax_over_error']]

# Binary Star Data
   df3=df[(df['parallax_over_error']>=snr) & (df['parallax']>0.0) \
   & ((df['non_single_star']==True) | (df['ruwe']>1.4))]
   df4=df3[['phot_g_mean_mag','bp_rp','parallax','parallax_over_error']]

# Variable Star Data
   df5=df[(df['parallax_over_error']>=snr) & (df['parallax']>0.0) \
   & (df['phot_variable_flag']=='VARIABLE')]
   df6=df5[['phot_g_mean_mag','bp_rp','parallax','parallax_over_error']]

# Extract Color
   x=df2['bp_rp'].to_numpy()
   x2=df4['bp_rp'].to_numpy()
   x3=df6['bp_rp'].to_numpy()
# GAIA g-mag
   gmag=df2['phot_g_mean_mag'].to_numpy()
   gmag2=df4['phot_g_mean_mag'].to_numpy()
   gmag3=df6['phot_g_mean_mag'].to_numpy()
# Extract Parallax
   parallax=df2['parallax'].to_numpy()
   parallax2=df4['parallax'].to_numpy()
   parallax3=df6['parallax'].to_numpy()
# Convert g-mag to Absolute Magnitude
   y=gmag+5.0*numpy.log10(parallax)-10.0
   y2=gmag2+5.0*numpy.log10(parallax2)-10.0
   y3=gmag3+5.0*numpy.log10(parallax3)-10.0
# Parallax SNR
   z=df2['parallax_over_error']
   z2=df4['parallax_over_error']
   z3=df6['parallax_over_error']

   # Plotting the HR diagram
   plt.rcParams['font.family'] = 'Times New Roman'
   plt.figure(figsize=(8.5, 11))
# Invert Y-axis: brighter stars are at the top
   plt.gca().invert_yaxis()
# X-Y range
   plt.xlim(-1.2,5.2)
   plt.ylim(17.4,-4.5)
   plt.xticks(fontsize=20)
   plt.yticks(fontsize=20)
   plt.tick_params(direction='in') 
   if(snr==5): snrmin=5.0   ; snrmax=50.0
   if(snr==10): snrmin=10.0 ; snrmax=50.0
   if(snr==20): snrmin=20.0 ; snrmax=50.0
   if(snr==50): snrmin=50.0 ; snrmax=200.0
   if(snr==100): snrmin=100.0 ; snrmax=200.0
   if(snr==200): snrmin=200.0 ; snrmax=500.0
   if(flag_binary==False):
      sc = plt.scatter(x, y, c=z, cmap='rainbow', s=0.05, vmin=snrmin,vmax=snrmax)
   elif(flag_binary==True):
      sc = plt.scatter(x2, y2, c=z2, cmap='rainbow', s=0.5, vmin=snrmin,vmax=snrmax)
      if(len(x3)>1):
        plt.scatter(x3, y3, c=z3, cmap='rainbow', s=50.0, marker='o', facecolors='none', vmin=snrmin,vmax=snrmax)

# Add colorbar for SNR
   cbar = plt.colorbar(sc)
   cbar.set_label('Parallax Signal-to-Noise Ratio (SNR)',fontsize=20)

# Labels and title
   plt.xlabel('BP - RP Color',fontsize=20)
   plt.ylabel('Absolute Magnitude M$_{G}$',fontsize=20)

# Today's String YYYYMMDD
   today_str = date.today().strftime("%Y%m%d")
   if(flag_binary==False):
     plt.title('Hertzsprung–Russell Diagram \
     (colored by Parallax SNR)\n'+sdssdr+' vs. GAIA DR3 : '\
     +str(len(x))+' Stars,  SNR>'+str(snr),fontsize=20)
     plt.tight_layout()
     sdss_dr=sdssdr.replace(" ","")
     plt.savefig(today_str+'a_GAIADR3vs'+sdss_dr+'_SNR'+str(snr)+'.png')
   elif(flag_binary==True):
     plt.title('Hertzsprung–Russell Diagram \
     (colored by Parallax SNR)\n'+sdssdr+' vs. GAIA DR3: '\
     +str(len(x2))+' Binaries, '+str(len(x3))+' Variables, SNR>'+str(snr),fontsize=20)
     plt.tight_layout()
     sdss_dr=sdssdr.replace(" ","")
     plt.savefig(today_str+'b_GAIADR3vs'+sdss_dr+'_SNR'+str(snr)+'.png')
   plt.clf()
   plt.close()

#SDSS DR8
csvfile1='../csvfiles/gaiadr3_sdssdr8_star.csv'
csvfile1='../csvfiles/gaiadr3_desidr1_star1.csv'
csvfile1='../csvfiles/gaiadr3_desidr1_star.csv'

#SDSS DR17
csvfile2='../csvfiles/gaiadr3_sdssdr17_star.csv'
csvfile2='../csvfiles/gaiadr3_desidr1_star2.csv'

# Draw SNR Histogram
plot_parallax_SNR_histogram2(csvfile1,csvfile2)

for snr in [5,10,20,50,100,200]:
   print(snr)
   sdssdr='SDSS DR8'
   sdssdr='DESI DR1a'
   sdssdr='DESI DR1'
   flag_binary=True
   plot_HRdiagramSNR(csvfile1,snr,sdssdr,flag_binary)
   flag_binary=False
   plot_HRdiagramSNR(csvfile1,snr,sdssdr,flag_binary)
   #sys.exit(1)
   sdssdr='SDSS DR17'
   sdssdr='DESI DR1b'
   flag_binary=True
   #plot_HRdiagramSNR(csvfile2,snr,sdssdr,flag_binary)
   flag_binary=False
   #plot_HRdiagramSNR(csvfile2,snr,sdssdr,flag_binary)
