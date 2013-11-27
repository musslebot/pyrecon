#!/usr/bin/python
from pyrecon.tools.classes import *
import argparse

def main(seriesPath, threshold):
	series = loadSeries(seriesPath)
	print('======================')
	print('curationTool on %s')%series.name
	print('======================')
	findDuplicateTraces(series)
	findDistantTraces(series, threshold)
	findReverseTraces(series)

def findDuplicateTraces(series):
	'''Prints the duplicates found within every section of <series>'''
	print('--------------------------')
	print('Locating duplicate traces:')
	print('--------------------------')
	duplicateDict = series.locateDuplicates()
	for sec in sorted(duplicateDict):
		print('Section index: '+str(sec))
		for name in list(set([cont.name for cont in duplicateDict[sec]])):
			print('\t'+name)
		print

def findDistantTraces(series, threshold):
	'''Prints traces of the same name separated by <threshold (default: 7)> sections that do not contain that section'''
	print('-------------------------------------------------')
	print('Locating distant traces (treshold: +/-%d sections):')%threshold
	print('-------------------------------------------------')
	distantDict = series.locateDistantTraces(threshold)
	for sec in sorted(distantDict):
		print('Section index: '+str(sec))
		for name in distantDict[sec]:
			print('\t'+name)
		print

def findReverseTraces(series):
	'''Prints all the reverse traces found in a series (per section)'''
	print('------------------------')
	print('Locating reverse traces:')
	print('------------------------')
	reverseDict = series.locateReverseTraces()
	for sec in sorted(reverseDict):
		print('Section index: '+str(sec))
		for cont in reverseDict[sec]:
			print('\t'+cont.name)
		print

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Performs various functions to assist curating a series')
    parser.add_argument('series', nargs=1, type=str, help='Path to the series/sections that needs to be curated')
    parser.add_argument('threshold', nargs=1, type=int, help='Parameter for findDistantTraces, the number of sections that exist between two traces of the same name that do not contain said trace')
    args = vars(parser.parse_args())
    # Assign argparse things to their variables
    seriesPath = str(args['series'][0])
    threshold = int(args['threshold'][0])
    main(seriesPath, threshold)