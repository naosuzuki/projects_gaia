import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy

# 2025-06-19 update
# 2025-06-17 rewritten at FSU

def plot_HRdiagramSNR(csvfile):
   df=pd.read_csv(csvfile)
   print(df)
   print(len(df))
   df1=df[(df['parallax_over_error']>=20.0) & (df['parallax']>0.0)]
   #df1=df[(df['parallax_over_error']>=100.0) & (df['parallax']>0.0)]
   df2=df1[['phot_g_mean_mag','bp_rp','parallax','parallax_over_error']]
   print(len(df1))
   print(df2)
   x=df2['bp_rp'].to_numpy()
   gmag=df2['phot_g_mean_mag'].to_numpy()
   parallax=df2['parallax'].to_numpy()
   y=gmag+5.0*numpy.log10(parallax)-10.0
   z=df2['parallax_over_error']
   print(x,y)
   print('parallax=',parallax)
   print('gmag=',gmag)

   # Plotting the HR diagram
   #plt.figure(figsize=(8, 6))
   #plt.figure(figsize=(6, 9))
   plt.rcParams['font.family'] = 'Times New Roman'
   plt.figure(figsize=(8.5, 11))
# Invert Y-axis: brighter stars are at the top
   plt.gca().invert_yaxis()
   plt.xlim(-1.2,5.2)
   plt.ylim(17.4,-4.5)
   plt.xticks(fontsize=16)
   plt.yticks(fontsize=16)
   #sc = plt.scatter(df['bp_rp'], df['abs_g'], c=df['snr'], cmap='viridis', s=20, edgecolor='k')
   #sc = plt.scatter(x, y, c=z, cmap='viridis', s=0.01, edgecolor='k')
   #sc = plt.scatter(x, y, c=z, cmap='rainbow', s=0.01, edgecolor='k', vmin=0.0,vmax=100.0)
   sc = plt.scatter(x, y, c=z, cmap='rainbow', s=0.01, vmin=20.0,vmax=50.0)


# Add colorbar for SNR
   cbar = plt.colorbar(sc)
   cbar.set_label('Signal-to-Noise Ratio (SNR)',fontsize=16)

# Labels and title
   plt.xlabel('BP - RP Color',fontsize=16)
   plt.ylabel('Absolute Magnitude M$_{G}$',fontsize=16)
   plt.title('Hertzsprung–Russell Diagram (colored by SNR)',fontsize=16)

   plt.tight_layout()
   plt.savefig('hr20.png')

csvfile='../csvfiles/gaiadr3_sdssdr8_star.csv'
csvfile='../csvfiles/gaiadr3_sdssdr17_star.csv'
plot_HRdiagramSNR(csvfile)
