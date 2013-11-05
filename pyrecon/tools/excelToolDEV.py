import sys, re, openpyxl
from pyrecon.tools.classes import *
import argparse

class Workbook(openpyxl.Workbook):
    def __init__(self, series=None):
        openpyxl.Workbook.__init__(self)
        
        self.series = series # Series object for this workbook
        self.objects = series.getObjectLists() # Names of objects in this series
        
    def createProtrusions(self):
        protrusions = []
        for protName in self.objects[1]:
            protrusion = Protrusion(name=protName, series=self.series)
            protrusion.findChildren()
            protrusions.append(protrusion)
        self.protrusions = protrusions
    
    
        