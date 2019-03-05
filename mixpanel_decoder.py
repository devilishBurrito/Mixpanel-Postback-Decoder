import base64 as base
import pandas as pd
import re
import pdb
from tqdm import tqdm

def run(mdf, mname):

	postback = mdf.postback_url
	print(postback)

	for x in tqdm(range(len(postback))):
		original_url = postback[x]
		trimmed = str(re.findall(r'data=([^\&]*)', original_url))
		### the last part is telling str() the encoding:
		### https://stackoverflow.com/questions/37016946/remove-b-character-do-in-front-of-a-string-literal-in-python-3
		decoded = str(base.b64decode(trimmed), 'utf-8')
		mdf['decoded_postback'][x] = decoded
		mdf.to_csv(mname, sep=',', index=None, header=True)
		

def rename(mname):
	msuffix = '_DECODED.csv'
	i = mname.split('.')
	i = i[0] + msuffix
	return i

def logs_csv(out, df):
	df['decoded_postback'] = ''
	df.to_csv(out, sep=',', index=None, header=True)
	return df

def readin_name():
	mprefix = input('FILE NAME: ')
	msuffix = '.csv'
	mname = str(mprefix + msuffix)
	print ('\n' + 'Reading in file: ' + mname)
	return mname

def start():
	print ('\nWelcome to Mixpanel Decoder STREAMLINED \nPlease provide the filename below. Only CSVs are supported but do not include ".csv" when listing the file name below')
	name = readin_name()
	localFile = pd.read_csv(name)
	logFileName = rename(name)
	logFile = logs_csv(logFileName, localFile)

	run(logFile,logFileName)

start() 