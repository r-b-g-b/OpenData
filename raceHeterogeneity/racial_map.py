import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

'''843,286 lines'''

# with open(geo_fname, 'r') as f:
# 	line = f.readline()

'''
File linking fields [0:4]
0 	File Identification 		FILEID 	6 	A/N
1	State/U.S. Abbreviation (USPS) 	STUSAB 	2 	A
2	Characteristic Iteration 		CHARITER 	3 	A/N
3	Characteristic Iteration File Sequence Number 	CIFSN 	2 	A/N
4	Logical Record Number 		LOGRECNO 	7 	N

P3. 8 columns [4:12]
P4. 3 columns [12:15]
P5. 17 columns [15:32]
'''

def plotEastBay(ax=None):
	if ax is None: fig, ax = plt.subplots()
	df = pd.read_csv('raceData.csv')
	df_geo = pd.read_csv('LatLon.csv')
	lat_lim = (37.839583384232007, 37.90618479880775)
	lon_lim = (-122.30799920903472, -122.23802834898422)
	ix = np.vstack((df_geo.lat<lat_lim[1], df_geo.lat>lat_lim[0], df_geo.lon<lon_lim[1], df_geo.lon>lon_lim[0])).all(0)
	df_geo = df_geo[ix]


	for i, row in df_geo.iterrows():
		if i in df.index:
			hi = df.ix[i]['HI']
			color = plt.cm.jet(int(256-(1.78*(hi-0.44)*256)))
			ax.plot(row['lon'], row['lat'], '.', ms=5, color = color)

def loadGeoData(skiprows=0, nrows = 10):

	linelen = 501
	geo_fname = 'cageo2010.csv'
	with open(geo_fname, 'r') as f:
		f.seek(linelen*skiprows)
		logrecno, lat, lon = [], [], []
		if nrows is None:
			for line in f:
				logrecno.append(int(line[18:25]))
				lat.append(float(line[336:347]))
				lon.append(float(line[347:359]))			
		else:
			for i in xrange(nrows):
				line = f.readline()
				logrecno.append(int(line[18:25]))
				lat.append(float(line[336:347]))
				lon.append(float(line[347:359]))

	return pd.DataFrame({'lat': lat, 'lon': lon}, index=logrecno)

	# geo_fname = 'cageo2010.csv'
	# widths = [6, 2, 3, 2, 3, 2, 7, 1, 1, 2, 3, 2, 2, 5, 2, 2, 5, 2, 2, 6, 1, 4, 2, 5, 2, 2, 4, 5, 2, 1, 3, 5, 2, 6, 1, 5, 2, 5, 2, 5, 3, 5, 2, 5, 3, 1, 1, 5, 2, 1, 1, 2, 3, 3, 6, 1, 3, 5, 5, 2, 5, 5, 5, 14, 14, 90, 1, 1, 9, 9, 11, 12, 2, 1]
	# names = ['']*len(widths)
	# names[6] = 'LOGRECNO'
	# names[70] = 'lat'
	# names[71] = 'lon'
	# usecols = range(len(widths))
	# df_geo = pd.read_fwf(geo_fname, widths=widths, header = None, skiprows=skiprows, nrows=nrows, names=names)
	# 
	# return df_geo

def saveCensusData():

	df_dat = df.filter(regex='^num')
	ix = df_dat.values.sum(1)>0
	df = df[ix]

	df['numOther2'] = df.numAmIn+df.numPacIs+df.numOther+df.numTwo
	del df['numAmIn'], df['numPacIs'], df['numOther'], df['numTwo']
	
	df = addHomogeneityIndex(df)
	df.to_csv('raceData.csv')

def loadRawCensusData(nrows=10, skiprows=0):
	args = {}
	if nrows is not None:
		args.update({'nrows': nrows})
	if skiprows is not None:
		args.update({'skiprows': skiprows})

	usecols = [4, 18, 19, 20, 21, 22, 23, 24, 25]
	names = ['LOGRECNO', 'numWhite', 'numBlack', 'numAmIn', 'numAsian', 'numPacIs', 'numOther', 'numTwo', 'numHisp']

	fname = 'ca000032010.csv'

	df = pd.read_csv(fname, usecols=usecols, header=None, **args)
	df.columns = names

	return df

def addHomogeneityIndex(df):

	df['HI'] = calcHomogeneityIndex(df)
	return df

def calcHomogeneityIndex(df):
	df_dat = df.filter(regex='^num')
	homogeneity_ix = np.empty(len(df_dat))
	for i, (key, values) in enumerate(df_dat.iterrows()):
		x = values.values / values.values.sum().astype(float)
		homogeneity_ix[i] = np.linalg.norm(x)

	return homogeneity_ix
