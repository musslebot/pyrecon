from lxml import etree as ET

def getTree(path):
	return ET.parse(path)