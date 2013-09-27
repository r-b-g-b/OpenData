'''SFPD data'''
import os, re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import misc

basedir = '/Users/robert/Documents/Code/OpenData'
def matchdrug(descript):
	'''Descide which drug was involved'''
	drug_regexp = dict(Amphetamine = '\sAMPHETAMINE', Base = 'BASE/ROCK', Cocaine = '(?<!ROCK )COCAINE', \
		Hallucinogen = 'HALLUCINO', Heroin = 'HEROIN', Marijuana = 'MARIJUANA', \
		Meth = 'METH', Methadone = 'METHADONE', Opiates = 'OPI[A|U]')

	match = 'NA'
	for i, j in drug_regexp.iteritems():
		if len(re.findall(j, descript))>0:
			match = i
	return match

def load():

	df = pd.read_csv(os.path.join('SFPD_Incidents_-_Previous_Three_Months.csv'))

	# '''make bag of words from description field'''
	# df1 = df[df.Category=='DRUG/NARCOTIC']
	# words1 = ' '.join(df.Descript)
	# words = words1.split(' ')
	# uwords = np.unique(words)

	'''Add drug field to data frame'''
	drug = []
	for i in df.Descript:
		drug.append(matchdrug(i))
	df['Drug'] = drug

	return df

def plot_loc_by_drug(df):

	udrug = ['Cocaine', 'Marijuana']
	colors = 'br'
	fig = plt.figure();
	ax = fig.add_subplot(111);
	for i, drug in enumerate(udrug):
		df_ = df[df.Drug==drug]
		ax.plot(df_.X, df_.Y, '.', ms = 2, color = colors[i], label = drug)
		# ax.set_aspect('equal')
	ax.legend();

def hist2_loc_by_drug(df):

	df = df[df.Drug!='NA']
	fig = plt.figure();
	udrug = np.unique(df.Drug)
	for i, drug in enumerate(udrug):
		ax = fig.add_subplot(2, 4, i+1)
		df_ = df[df.Drug==drug]
		ax.hist2d(df_.X, df_.Y, bins = 100)
		ax.set_title(drug)
		ax.set_xticklabels('')
		ax.set_yticklabels('')
		# ax.set_aspect('equal')


def plot_drugs_by_dist(df):
	fig = plt.figure();
	ax = []
	udist = np.unique(df.PdDistrict)
	for i, dist in enumerate(udist):
		df_ = df[df.PdDistrict==dist]
		ax.append(fig.add_subplot(2, 5, i+1))
		df_.Drug.value_counts()[:5].plot(kind = 'bar', ax = ax[-1])
		ax[-1].set_title(dist)

	misc.sameyaxis(ax)


