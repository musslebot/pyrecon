'''Main driver for mergeTool module.'''
#!/usr/bin/python
from pyrecon.main import openSeries
from pyrecon.classes import Section, Series
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Merge two series together.')
	parser.add_argument('input1', nargs=1, type=str, help='Path to the first series or directory')
	parser.add_argument('input2', nargs=1, type=str, help='Path to the second series or directory')
	parser.add_argument('output', nargs=1, type=str, help='Path to the directory for writing the merged series\' XML files')
	args = vars(parser.parse_args())
	# Assign argparse things to their variables
	series1 = openSeries( str(args['input1'][0]) )
	series2 = openSeries( str(args['input2'][0]) )
	directory = str(args['output'][0])
	main(series1, series2, directory)

def main(series1, series2, directory):
	print series1
	print series2
	print directory

class mergeObject:
	def __init__(self, *args, **kwargs):
		return