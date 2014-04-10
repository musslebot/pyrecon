#!/usr/bin/python
from pyrecon.main import openSeries
import argparse

def main(series, threshold, duplicates=True, distant=True, reverse=True, printOut=True):
	if type(series) == type(''):
		series = openSeries(series)
	if printOut:
		print('======================')
		print('curationTool on %s')%series.name
		print('======================')
	a=''
	b=''
	c=''
	if duplicates:
		a = findDuplicateTraces(series, printOut=printOut)
	if distant:
		b = findDistantTraces(series, threshold, printOut=printOut)
	if reverse:
		c = findReverseTraces(series, printOut=printOut)
	if not printOut:
		return (a,b,c)
def findDuplicateTraces(series, printOut=True):
	'''Prints the duplicates found within every section of <series>'''
	if type(series) == type(''):
		series = openSeries(series)
	duplicateDict = series.locateDuplicates()
	if printOut:
		print('--------------------------\n'+'Locating duplicate traces:'+'--------------------------\n')
		for sec in sorted(duplicateDict):
			print('Section index: '+str(sec))
			for name in list(set([cont.name for cont in duplicateDict[sec]])):
				print('\t'+name)
			print
		return
	else:
		output = []
		output.append('--------------------------')
		output.append('Locating duplicate traces:')
		output.append('--------------------------')
		for sec in sorted(duplicateDict):
			output.append('Section index: '+str(sec))
			for name in list(set([cont.name for cont in duplicateDict[sec]])):
				output.append('\t'+name)
			output.append('\n')
		return output

def findDistantTraces(series, threshold, printOut=True):
	'''Prints traces of the same name separated by <threshold> sections that do not contain that section'''
	if type(series) == type(''):
		series = openSeries(series)
	distantDict = series.locateDistantTraces(threshold)
	if printOut:
		print('-------------------------------------------------\n'+str('Locating distant traces (threshold: +/-%d sections):'%threshold)+'-------------------------------------------------\n')
		for sec in sorted(distantDict):
			print('Section index: '+str(sec))
			for name in distantDict[sec]:
				print('\t'+name)
			print
		return
	else:
		output = []
		output.append('-------------------------------------------------')
		output.append(str('Locating distant traces (treshold: +/-%d sections):'%threshold))
		output.append('-------------------------------------------------')
		for sec in sorted(distantDict):
			output.append('Section index: '+str(sec))
			for name in distantDict[sec]:
				output.append('\t'+name)
			output.append('\n')
		return output

def findReverseTraces(series, printOut=True):
	'''Prints all the reverse traces found in a series (per section)'''
	if type(series) == type(''):
		series = openSeries(series)
	reverseDict = series.locateReverseTraces()
	if printOut:
		print('------------------------\n'+'Locating reverse traces:'+'------------------------\n')
		for sec in sorted(reverseDict):
			print('Section index: '+str(sec))
			for cont in reverseDict[sec]:
				print('\t'+cont.name)
			print
		return
	else:
		output = []
		output.append('------------------------')
		output.append('Locating reverse traces:')
		output.append('------------------------')
		for sec in sorted(reverseDict):
			output.append('Section index: '+str(sec))
			for cont in reverseDict[sec]:
				output.append('\t'+cont.name)
			output.append('\n')
		return output
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Performs various functions to assist curating a series')
    parser.add_argument('series', nargs=1, type=str, help='Path to the series/sections that needs to be curated')
    parser.add_argument('threshold', nargs=1, type=int, help='Parameter for findDistantTraces, the number of sections that exist between two traces of the same name that do not contain said trace')
    args = vars(parser.parse_args())
    # Assign argparse things to their variables
    seriesPath = str(args['series'][0])
    threshold = int(args['threshold'][0])
    main(seriesPath, threshold)