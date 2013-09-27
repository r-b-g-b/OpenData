'''San Francisco Businesses'''
'''Load file'''
import os, re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import misc

import datetime
basedir = '/Users/robert/Documents/Code/OpenData'
def load():
	df = pd.read_csv(os.path.join(basedir, 'Businesses_Registered_in_San_Francisco_-_Active.csv'))
	df.rename(columns = lambda x: re.sub(' ', '_', x), inplace = True)
	df['Class_Code'] = np.int32(df.Class_Code)
	df['PBC_Code'] = np.int32(df.PBC_Code)

	'''Convert lat, long from string to float'''
	p = re.compile('\d*\.\d*')
	LocX = []; LocY = []; ix = []
	for i, j in df.iterrows():
		if pd.notnull(j['Location']):
			x, y = np.float32(p.findall(j['Location']))
			LocX.append(x); LocY.append(y)
			ix.append(i)
	df['LocX'] = pd.Series(LocX, index = ix)
	df['LocY'] = pd.Series(LocY, index = ix)

	'''Add description field from PBC code descriptions'''
	pbc2descr = dict(np.loadtxt('pbc_codes.csv', 'S', delimiter = ','))
	Descr = []
	for i in df.PBC_Code:
		try:
			Descr.append(pbc2descr[str(i)])
		except:
			Descr.append('UNKNOWN')
	df['Descript'] = Descr

	'''Add founded date from str to datetime'''
	tmp = [(i, misc.str2date(str(j['DBA_Start_Date']), delimiter = '', format = 'YYYYMMDD')) for i, j in df.iterrows()]
	ix, dates = zip(*tmp)
	df['Founded'] = pd.Series(dates, index = ix)

	return df

def plot_loc(df, ax = None, color = 'b', ms = 0.5, **kwargs):
	ax, fig = misc.axis_check(ax)
	ax.plot(-df.LocY, df.LocX, '.', color = color, ms = ms, **kwargs)
	return ax

def plot_hist2d(df, ax = None):
	ax, fig = misc.axis_check(ax)
	ax.hist2d(-df.LocY, df.LocX, bins = 1000)
	return ax

def add_categories(df):

	categories = dict(food = [3079, 5800, 5812], drink = [3095, 5813], \
		music = [4333, 5733], liquor = [2081, 2088, 3251, 5180, 5921])

	df['Category'] = 'NA'
	for key, value in categories.iteritems():
		match_ix = [ix for ix, val in df.PBC_Code.iteritems() if val in value]
		df['Category'][match_ix] = key

	return df

def parse_pbc_codes():
	'''Parse PBC codes into numbers and descriptions'''
	f = open('tax_pbc_code.csv')
	x = f.readlines()

	p = re.compile("(?<=[C|S|P] \d{2} )\d{4} [\w\s&.,\'\-\(\)%/]*(?=[C|S|P] \d{2} \d{4})")
	code = []
	descr = []
	for x_ in x:
		x_ = re.sub(',', ' ', x_)
		tmp = p.findall(x_)[0]
		code.append(np.int32(tmp.split(' ')[0]))
		descr.append(' '.join(tmp.split(' ')[1:-2]))

	f2 = open('tmp.csv', 'w')
	for i, j in zip(code, descr):
		f2.write('%s,%s\n' % (i, j))
	f2.close()



def plot_hist2d_by_decade(df):

	decades = np.arange(1940, 2020, 10)
	fig = plt.figure()
	ax = []
	for i in range(len(decades)-1):
		
		dec1 = datetime.date(decades[i], 1, 1)
		dec2 = datetime.date(decades[i+1], 1, 1)
		df_ = df[np.logical_and(df['Founded']>dec1, df['Founded']<dec2)]
		x = df_['LocX'][pd.notnull(df_['LocX'])]
		y = df_['LocY'][pd.notnull(df_['LocY'])]

		ax.append(fig.add_subplot(2, 4, i+1))
		ax[-1].hist2d(-y, x, bins = 100);
