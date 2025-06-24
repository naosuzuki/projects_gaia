import pandas as pd

csvfile1='../csvfiles/gaiadr3_desidr1_star1.csv'
csvfile2='../csvfiles/gaiadr3_desidr1_star2.csv'
   
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
