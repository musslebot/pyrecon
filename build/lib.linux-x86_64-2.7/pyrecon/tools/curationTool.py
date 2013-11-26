#!/usr/bin/python
from pyrecon.tools.classes import *





def main(seriesPath):
	series = loadSeries(seriesPath)
	print('curationTool on (%s)')%series.name
	findDups(series)
	findDistantTraces(series)
	findReverseTraces(series)

def findDups(series):
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

def findDistantTraces(series, threshold=7): #===
	'''Prints traces of the same name separated by <threshold (default: 7)> sections that do not contain that section'''
	print('--------------------------------------')
	print('Locating distant traces (treshold: +/-%d):')%threshold
	print('--------------------------------------')
	distantDict = series.locateDistantTraces() #=== make sure the + and - thresholds are inclusive
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
