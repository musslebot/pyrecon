import sys, re, openpyxl
from pyrecon.tools.classes import *
import argparse

class Workbook(openpyxl.Workbook):
    def __init__(self, series=None):
        openpyxl.Workbook.__init__(self)
        
        self.series = series # Series object for this workbook
        
        self.objects = series.getObjectLists() # Names of objects in this series
        
        self.dendriteFilter = [] # Dendrites to be excluded from workbook
        
        # Traces to be excluded in workbook
        self.filter = ['d[0-9][0-9]c[0-9][0-9]',
                       '.{0,} .{0,}']
    
    def createProtrusions(self):
        protrusions = []
        for protName in self.objects[1]:
            protrusion = Protrusion(name=protName, series=self.series)
            protrusions.append(protrusion)
        self.protrusions = protrusions
        