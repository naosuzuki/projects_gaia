import pandas as pd

# DESI DR1
csvfile1='../csvfiles/gaiadr3_desidr1_star1.csv'
csvfile2='../csvfiles/gaiadr3_desidr1_star2.csv'

# DESI DR2
csvfile1='../csvfiles/gaiadr3_desidr2_star1.csv'
csvfile2='../csvfiles/gaiadr3_desidr2_star2.csv'
csvfile3='../csvfiles/gaiadr3_desidr2_star3.csv'
csvfile4='../csvfiles/gaiadr3_desidr2_star4.csv'
csvfile5='../csvfiles/gaiadr3_desidr2_star5.csv'

# DESI DR2 pix
csvfile1='../csvfiles/gaiadr3_desidr2pix_star1.csv'
csvfile2='../csvfiles/gaiadr3_desidr2pix_star2.csv'
csvfile3='../csvfiles/gaiadr3_desidr2pix_star3.csv'
csvfile4='../csvfiles/gaiadr3_desidr2pix_star4.csv'
csvfile5='../csvfiles/gaiadr3_desidr2pix_star5.csv'

def concat_desi_dr2(csvfile1,csvfile2,csvfile3,csvfile4,csvfile5):
   dftmp1=pd.read_csv(csvfile1)
   df1=dftmp1[['phot_g_mean_mag','bp_rp','parallax','parallax_over_error',\
            'non_single_star','phot_variable_flag','ruwe',\
            'phot_variable_flag']]

   dftmp2=pd.read_csv(csvfile2)
   df2=dftmp2[['phot_g_mean_mag','bp_rp','parallax','parallax_over_error',\
            'non_single_star','phot_variable_flag','ruwe',\
            'phot_variable_flag']]

   dftmp3=pd.read_csv(csvfile3)
   df3=dftmp3[['phot_g_mean_mag','bp_rp','parallax','parallax_over_error',\
            'non_single_star','phot_variable_flag','ruwe',\
            'phot_variable_flag']]

   dftmp4=pd.read_csv(csvfile4)
   df4=dftmp4[['phot_g_mean_mag','bp_rp','parallax','parallax_over_error',\
            'non_single_star','phot_variable_flag','ruwe',\
            'phot_variable_flag']]

   dftmp5=pd.read_csv(csvfile5)
   df5=dftmp5[['phot_g_mean_mag','bp_rp','parallax','parallax_over_error',\
            'non_single_star','phot_variable_flag','ruwe',\
            'phot_variable_flag']]

   df6=pd.concat([df1, df2, df3, df4, df5], ignore_index=True)
   df6.to_csv('../csvfiles/gaiadr3_desidr2_star.csv')
   
def concat_desi_dr1(csvfile1,csvfile2):
   dftmp1=pd.read_csv(csvfile1)
   df1=dftmp1[['phot_g_mean_mag','bp_rp','parallax','parallax_over_error',\
            'non_single_star','phot_variable_flag','ruwe',\
            'phot_variable_flag']]

   dftmp2=pd.read_csv(csvfile2)
   df2=dftmp2[['phot_g_mean_mag','bp_rp','parallax','parallax_over_error',\
            'non_single_star','phot_variable_flag','ruwe',\
            'phot_variable_flag']]

   df3=pd.concat([df1, df2], ignore_index=True)
   df3.to_csv('../csvfiles/gaiadr3_desidr1_star.csv')

concat_desi_dr2(csvfile1,csvfile2,csvfile3,csvfile4,csvfile5)
