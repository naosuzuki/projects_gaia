import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import sys

# 2025-06-19 update
# 2025-06-17 rewritten at FSU

def plot_parallax_SNR_histogram2(csvfile1,csvfile2):
   df=pd.read_csv(csvfile1)
# Extract data above Parallax SNR threshold
   df1=df[df['parallax']>0.0]
   df2=df1[['parallax','parallax_over_error']]
   snr_arr1=df2['parallax_over_error'].to_numpy()

   bins=numpy.arange(20)*10.0
   plt.rcParams["font.family"] = "Times New Roman"
   plt.title('GAIA DR3')
   plt.xlabel('GAIA DR3 SNR')
   plt.ylabel('Number of Stars')
   plt.xlim([-5,205])
   plt.tick_params(axis='both',which='both',direction='in') 
   plt.ylim([1.2,4.0e5])

   plt.hist(snr_arr1,bins,log=True,align='left',rwidth=0.9,color='r')
   plt.savefig('histexp.png')

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

def plot_HRdiagramSNR(csvfile,snr,sdssdr):
   df=pd.read_csv(csvfile)
# Extract data above Parallax SNR threshold
   df1=df[(df['parallax_over_error']>=snr) & (df['parallax']>0.0)]
   df2=df1[['phot_g_mean_mag','bp_rp','parallax','parallax_over_error']]

# Extract Color
   x=df2['bp_rp'].to_numpy()
# GAIA g-mag
   gmag=df2['phot_g_mean_mag'].to_numpy()
# Extract Parallax
   parallax=df2['parallax'].to_numpy()
# Convert g-mag to Absolute Magnitude
   y=gmag+5.0*numpy.log10(parallax)-10.0
   z=df2['parallax_over_error']

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
   sc = plt.scatter(x, y, c=z, cmap='rainbow', s=0.05, vmin=snrmin,vmax=snrmax)

# Add colorbar for SNR
   cbar = plt.colorbar(sc)
   cbar.set_label('Parallax Signal-to-Noise Ratio (SNR)',fontsize=20)

# Labels and title
   plt.xlabel('BP - RP Color',fontsize=20)
   plt.ylabel('Absolute Magnitude M$_{G}$',fontsize=20)
   plt.title('Hertzsprung–Russell Diagram \
   (colored by Parallax SNR)\nSDSS '+sdssdr+' vs. GAIA DR3 : '\
   +str(len(x))+' Stars,  SNR>'+str(snr),fontsize=20)

   plt.tight_layout()
   plt.savefig('20250619_GAIADR3vsSDSS'+sdssdr+'_SNR'+str(snr)+'.png')

snr=20 ; sdssdr='DR8'
csvfile='../csvfiles/gaiadr3_sdssdr8_star.csv'

snr=20 ; sdssdr='DR17'
csvfile='../csvfiles/gaiadr3_sdssdr17_star.csv'
plot_parallax_SNR_histogram(csvfile)
sys.exit(1)

for snr in [5,10,20,50,100,200]:
   print(snr)
   plot_HRdiagramSNR(csvfile,snr,sdssdr)
