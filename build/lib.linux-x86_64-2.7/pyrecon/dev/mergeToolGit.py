import pyrecon.classes
import pyrecon.mergeTool
import argparse

print
print("USING PYRECONSTRUCTS MERGETOOL")

def main(ancestor, current, other):
	print("Ancestor path: "+ancestor)
	print("Current branch path: "+current)
	print("Other branch path: "+other)
	
	print
	
	file1 = open(current)
	file2 = open(other)
	for line in file1.readlines():
		if "section.dtd" in line:
			print loadSeries()
			print loadSeries()

# ARGPARSE & CALL TO MAIN() 
# if __name__ == '__main__':
parser = argparse.ArgumentParser(description='Handles conflicts for git-merge')

parser.add_argument('ancestor', nargs=1, type=str, help='Path to ancestor version')
parser.add_argument('current', nargs=1, type=str, help='Path to current branch version')
parser.add_argument('other', nargs=1, type=str, help='Path to other branch version')

args = vars(parser.parse_args())

ancestor = str(args['ancestor'][0])
current = str(args['current'][0])
other = str(args['other'][0]) 

main(ancestor, current, other)
