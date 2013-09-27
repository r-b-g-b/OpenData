'''School performance data'''
import os, re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
import itertools
from mpl_toolkits.basemap import Basemap

basedir = '/Users/robert/Documents/Code/OpenData'

df = pd.read_csv('/Users/robert/Documents/Code/OpenData/Achievement_Results_for_State_Assessments_in_Mathematics___School_Year_2008-09.csv')
ustates = np.unique(df.stnam)

colnames = df.columns[6:]
# groups = np.unique([i.split('_')[0] for i in colnames])
# grades = ['00', '03', '04', '05', '06', '07', '08', 'HS']
groups = ['MWH', 'MBL']
grades = ['00']
ratio_mean = []
ratio_sem = []
for ustate in ustates:
	df1 = df[df['stnam']==ustate]

	for (gp, gr) in itertools.product(groups, grades):
		numval = '%s_MTH%snumvalid_0809' % (gp, gr)
		pctprof = '%s_MTH%spctprof_0809' % (gp, gr)
		# if df1[numval]>1:
		data = [parse_pct(i) for i in df1[pctprof]]
		df1[pctprof+'_float'] = data

	y = (df1.MWH_MTH00pctprof_0809_float / df1.MBL_MTH00pctprof_0809_float)
	ratio_mean.append(y.mean())
	ratio_sem.append(st.sem(y))

ix = np.argsort(ratio_mean)
for i in ix:
	print ustates.iloc[i], ratio_mean[i]
	
def parse_pct(in1):

	in1 = np.str(in1)
	if in1=='PS' or in1=='.' or in1=='n/a' or in1=='nan':
		return np.nan
	if in1.find('-')>-1:
		in2 = np.float32(in1.split('-'))
		return np.mean(in2)
	else:
		in2 = filter(lambda x: x.isdigit(), in1)
		return np.float32(in2)

for i in df.columns:
	studenttype, tmp, yr = i.split('_')
	grade = tmp[3:5]
	dataname = tmp[5:]
