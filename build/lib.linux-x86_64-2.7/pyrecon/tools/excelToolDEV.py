import sys, re, openpyxl
from pyrecon.tools.classes import *
import argparse
from operator import attrgetter
from collections import OrderedDict
path_to_series = '/home/michaelm/Documents/Test Series/BBCHZ/BBCHZ.ser'
save_path = '/home/michaelm/Documents/Test Series/'

def main(path_to_series, save_path):
    series = loadSeries(path_to_series)
    wkbk = Workbook(series=series)
    wkbk.getDendrites()
    wkbk.getProtrusions()
    wkbk.listProtrusionChildren()
    wkbk.writeProtrusionsPerDendrite()
    wkbk.writeProtrusionChildrenToProtrusions()

class Workbook(openpyxl.Workbook):
    def __init__(self, series=None):
        openpyxl.Workbook.__init__(self)
        
        self.series = series # Series object for this workbook
        self.objects = series.getObjectLists() # Names of objects in this series
        self.filterType = ['c'] # Ignore these rTypes
    def listProtrusionChildren(self):
        childList = []
        for protrusion in self.protrusions:
            for child in protrusion.children:
                childList.append(child)
        self.protrusionChildren = sorted(list(set(childList)))
    def getProtrusions(self):
        '''Gathering protrusions/children from series'''
        protrusions = []
        for protName in self.objects[1]:
            protrusion = rObject(name=protName, series=self.series)
            protrusions.append(protrusion)
        self.protrusions = protrusions
    def getDendrites(self):
        dendrites = []
        for dendName in self.objects[0]:
            dendrite = rObject(name=dendName, series=self.series)
            dendrites.append(dendrite)
        self.dendrites = dendrites
    def writeProtrusionsPerDendrite(self):
        '''Creates a column of protrusions, in order by start section.
        All other data objects are aligned with their protrusion's row'''

        # Create worksheet for each dendrite
        for dendrite in self.dendrites:
            row = 0
            column = 0
            self.create_sheet(title=dendrite.name)
            sheet = self.get_sheet_by_name(dendrite.name)
            
            # Create a row for each protrusion in that dendrite
            for protrusion in sorted(self.protrusions, key=attrgetter('start','name')): #Sort by start # (by prot# if same start#)
                column = 0
                # Check if needs to be in this dendrite sheet
                if protrusion.dendrite == dendrite.name:
                    sheet.cell(row=row, column=column).value = protrusion.name
                    column+=1
                    # Write prot data
                    for data_item in protrusion.data:
                        sheet.cell(row=row, column=column).value = protrusion.data[data_item]
                        column+=1
                    row += 1+protrusion.getSpacing()                
    
    def writeProtrusionChildrenToProtrusions(self):
        # Grab existing wrksht for each dendrite
        for dendrite in self.dendrites:
            sheet = self.get_sheet_by_name(dendrite.name)
            
            # Get list of protrusions in this dendrite
            protList = [prot for prot in self.protrusions if dendrite.name in prot.name]
            # Get list of all protrusion children in this dendrite
            childList = []
            for prot in protList:
                for child in prot.children:
                    childList.append(child)
            childList = sorted(list(set(childList)))
           
            # Go through childList
            row = 0
            column = 5
            for child in childList:
                # find prots with this child
                for prot in protList:
                    if child in prot.children:
                        # update row to correct prot
                        for row in range(sheet.get_highest_row()):
                            if sheet.cell(row=row, column=0).value == prot.name:
                                row = row
                                break 
                        for subChild in prot.children[child]:
                            subChildObj = rObject(name=subChild, series=self.series)
                            for data_item in subChildObj.data:
                                sheet.cell(row=row, column=column).value = subChildObj.name
                                column+=1
                                sheet.cell(row=row, column=column).value = subChildObj.data[data_item]
          
        # Save workbook        
        self.save(save_path+self.series.name+'.xlsx')
                        
                
main(path_to_series,save_path)