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

   bins=numpy.arange(55)*10.0
   plt.rcParams["font.family"] = "Times New Roman"
   plt.title('GAIA DR3')
   plt.xlabel('GAIA DR3 SNR')
   plt.ylabel('Number of Stars')
   #plt.xlim([-5,205])
   plt.xlim([-5,525])
   plt.tick_params(axis='both',which='both',direction='in') 
   #plt.ylim([1.2,4.0e5])
   plt.ylim([1.2,4.0e6])
   plt.hist(snr_arr,bins,log=True,align='left',rwidth=0.8,color='r')
   plt.savefig('histexpdesi.png')

def plot_cumulativeSNR(csvfile,sdssdr):
   df=pd.read_csv(csvfile)
# Extract data above Parallax SNR threshold
   df1=df[df['parallax']>0.0]
   df2=df1[['parallax','parallax_over_error']]
   snr_arr=df2['parallax_over_error'].to_numpy()

# Create histogram bins
   bins = numpy.arange(snr_arr.min(), snr_arr.max() + 2)  # +2 to include upper edge

# Normal histogram
   hist, bin_edges = numpy.histogram(snr_arr, bins=bins)

# Cumulative in reverse: values ≥ x
   cum_counts_reverse = numpy.cumsum(hist[::-1])[::-1]

# Plot
   plt.step(bin_edges[:-1], cum_counts_reverse, where='post')
   plt.xlabel('Parallax SNR')
   plt.ylabel('Cumulative Count (Parallax SNR ≥ x)')
   plt.title('Reverse SNR Cumulative Histogram')
   plt.grid(True)
   plt.xlim([500,200])
   plt.ylim([0,50000])
   #plt.step(sorted_arr, cum_counts, where='post')
   #plt.xlabel('SNR')
   #plt.ylabel('Cumulative Count')
# Today's String YYYYMMDD
   today_str = date.today().strftime("%Y%m%d")
   sdss_dr=sdssdr.replace(" ","")
   plt.savefig(today_str+'_GAIADR3vs'+sdss_dr+'_SNRcumulative.png')
   plt.clf()
   plt.close()

def plot_HRdiagramSNR(csvfile,snr,sdssdr,flag_binary,flag_variable):
   df=pd.read_csv(csvfile)
# Extract data above Parallax SNR threshold
#  df0: all
   df0=df[(df['parallax_over_error']>=snr) & (df['parallax']>0.0)] 
   x0=df0['bp_rp'].to_numpy() 
   gmag0=df0['phot_g_mean_mag'].to_numpy()
   parallax0=df0['parallax'].to_numpy()
   y0=gmag0+5.0*numpy.log10(parallax0)-10.0
   z0=df0['parallax_over_error']

# SNR Condition
# Binary and Variable Exclusion is added on 6/20/2025
#  df1 : Binaries and Variables are excluded
   df1=df[(df['parallax_over_error']>=snr) & (df['parallax']>0.0) \
   & (df['non_single_star']==False) & (df['ruwe']<1.4) \
   & (df['phot_variable_flag']!='VARIABLE')]
   x1=df1['bp_rp'].to_numpy() 
   gmag1=df1['phot_g_mean_mag'].to_numpy()
   parallax1=df1['parallax'].to_numpy()
   y1=gmag1+5.0*numpy.log10(parallax1)-10.0
   z1=df1['parallax_over_error']

# Binary Star Data
   df2=df[(df['parallax_over_error']>=snr) & (df['parallax']>0.0) \
   & ((df['non_single_star']==True) | (df['ruwe']>1.4))]
   x2=df2['bp_rp'].to_numpy() 
   gmag2=df2['phot_g_mean_mag'].to_numpy()
   parallax2=df2['parallax'].to_numpy()
   y2=gmag2+5.0*numpy.log10(parallax2)-10.0
   z2=df2['parallax_over_error']

# Variable Star Data
   df3=df[(df['parallax_over_error']>=snr) & (df['parallax']>0.0) \
   & (df['phot_variable_flag']=='VARIABLE')]
   x3=df3['bp_rp'].to_numpy() 
   gmag3=df3['phot_g_mean_mag'].to_numpy()
   parallax3=df3['parallax'].to_numpy()
   y3=gmag3+5.0*numpy.log10(parallax3)-10.0
   z3=df3['parallax_over_error']

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
   if(snr==400): snrmin=400.0 ; snrmax=800.0
   if(snr==500): snrmin=500.0 ; snrmax=1000.0

# Labels and title
   plt.xlabel('BP - RP Color',fontsize=20)
   plt.ylabel('Absolute Magnitude M$_{G}$',fontsize=20)

# Today's String YYYYMMDD
   today_str = date.today().strftime("%Y%m%d")
# Case 1 : All Stars
   if(flag_binary==True and flag_variable==True and len(x0)>0):
     sc = plt.scatter(x0, y0, c=z0, cmap='rainbow', s=0.05, vmin=snrmin,vmax=snrmax)
# Add colorbar for SNR
     cbar = plt.colorbar(sc)
     cbar.set_label('Parallax Signal-to-Noise Ratio (SNR)',fontsize=20)
     plt.title('Hertzsprung–Russell Diagram \
     (colored by Parallax SNR)\n'+sdssdr+' vs. GAIA DR3 : '\
     +str(len(x0))+' Stars, SNR>'+str(snr)+' \n'\
     +str(len(x2))+' Binaries and '+str(len(x3))+' Variables are Included',fontsize=20)
     plt.tight_layout()
     sdss_dr=sdssdr.replace(" ","")
     plt.savefig(today_str+'a_GAIADR3vs'+sdss_dr+'_SNR'+str(snr)+'_all.png')
# Case 2 : Only Binaries
   elif(flag_binary==True and flag_variable==False and len(x2)>0):
     sc = plt.scatter(x2, y2, c=z2, cmap='rainbow', s=0.5, vmin=snrmin,vmax=snrmax)
# Add colorbar for SNR
     cbar = plt.colorbar(sc)
     cbar.set_label('Parallax Signal-to-Noise Ratio (SNR)',fontsize=20)
     plt.title('Hertzsprung–Russell Diagram \
     (colored by Parallax SNR)\n'+sdssdr+' vs. GAIA DR3 : '+'\n'\
     +str(len(x2))+' Binary Stars, SNR>'+str(snr),fontsize=20)
     plt.tight_layout()
     sdss_dr=sdssdr.replace(" ","")
     plt.savefig(today_str+'b_GAIADR3vs'+sdss_dr+'_SNR'+str(snr)+'_binary.png')
# Case 3 : Only Variable Stars
   elif(flag_binary==False and flag_variable==True and len(x3)>0):
     sc = plt.scatter(x3, y3, c=z3, cmap='rainbow', s=0.5, vmin=snrmin,vmax=snrmax)
# Add colorbar for SNR
     cbar = plt.colorbar(sc)
     cbar.set_label('Parallax Signal-to-Noise Ratio (SNR)',fontsize=20)
     plt.title('Hertzsprung–Russell Diagram \
     (colored by Parallax SNR)\n'+sdssdr+' vs. GAIA DR3: '+'\n'\
     +str(len(x3))+' Variable Stars, SNR>'+str(snr),fontsize=20)
     plt.tight_layout()
     sdss_dr=sdssdr.replace(" ","")
     plt.savefig(today_str+'c_GAIADR3vs'+sdss_dr+'_SNR'+str(snr)+'_variable.png')
# Case 4 : Purified Stars (Excluding Binary and Variables)
   elif(flag_binary==False and flag_variable==False and len(x1)>0):
     sc = plt.scatter(x1, y1, c=z1, cmap='rainbow', s=0.05, vmin=snrmin,vmax=snrmax)
# Add colorbar for SNR
     cbar = plt.colorbar(sc)
     cbar.set_label('Parallax Signal-to-Noise Ratio (SNR)',fontsize=20)
     plt.title('Hertzsprung–Russell Diagram \
     (colored by Parallax SNR)\n'+sdssdr+' vs. GAIA DR3: '\
     +str(len(x1))+' Stars, SNR>'+str(snr)+' \n'\
     +str(len(x2))+' Binaries and '+str(len(x3))+' Variables are Excluded',fontsize=20)
     plt.tight_layout()
     sdss_dr=sdssdr.replace(" ","")
     plt.savefig(today_str+'d_GAIADR3vs'+sdss_dr+'_SNR'+str(snr)+'_good.png')
   plt.clf()
   plt.close()

#SDSS DR8
csvfile1='../csvfiles/gaiadr3_desidr1_star1.csv'
csvfile1='../csvfiles/gaiadr3_sdssdr8_star.csv'
csvfile1='../csvfiles/gaiadr3_sdssdr17_star.csv'
csvfile1='../csvfiles/gaiadr3_desidr1_star.csv'
csvfile1='../csvfiles/gaiadr3_desidr2_star.csv'
csvfile1='../csvfiles/gaiadr3_desidr2pix_star.csv'
#plot_parallax_SNR_histogram(csvfile1)
sdssdr='DESI DR1'
sdssdr='DESI DR2'
plot_cumulativeSNR(csvfile1,sdssdr)

#SDSS DR17
csvfile2='../csvfiles/gaiadr3_sdssdr17_star.csv'
csvfile2='../csvfiles/gaiadr3_desidr1_star2.csv'

# Draw SNR Histogram
#plot_parallax_SNR_histogram2(csvfile1,csvfile2)

for snr in [5,10,20,50,100,200,400,500]:
   print(snr)
   sdssdr='SDSS DR8'
   sdssdr='SDSS DR17'
   sdssdr='DESI DR1'
   sdssdr='DESI DR2'
   flag_binary=True  ; flag_variable=True
   plot_HRdiagramSNR(csvfile1,snr,sdssdr,flag_binary,flag_variable)
   flag_binary=True  ; flag_variable=False
   plot_HRdiagramSNR(csvfile1,snr,sdssdr,flag_binary,flag_variable)
   flag_binary=False ; flag_variable=True
   plot_HRdiagramSNR(csvfile1,snr,sdssdr,flag_binary,flag_variable)
   flag_binary=False ; flag_variable=False
   plot_HRdiagramSNR(csvfile1,snr,sdssdr,flag_binary,flag_variable)
   #sys.exit(1)
   #sdssdr='SDSS DR17'
   #sdssdr='DESI DR1b'
   #flag_binary=True
   #plot_HRdiagramSNR(csvfile2,snr,sdssdr,flag_binary)
   #flag_binary=False
   #plot_HRdiagramSNR(csvfile2,snr,sdssdr,flag_binary)
