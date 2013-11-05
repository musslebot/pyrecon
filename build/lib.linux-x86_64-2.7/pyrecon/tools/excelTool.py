#!/usr/bin/env python
import sys, re, openpyxl
from pyrecon.tools.classes import *
import argparse

def main( path_to_series, save_path ):
    # Check that variables are correct
    if save_path[-1] != '/':
        save_path += '/'
    if '.xlsx' not in save_path:
        save_path += path_to_series.replace('.ser','').split('/')[-1]
        save_path += '.xlsx'
    series = loadSeries(path_to_series)
    wkbk = excelWorkbook()
    print('Preparing dendrite hierarchy...'),
    wkbk.getDendriteDict(series)
    print('DONE')
    print('Saving workbook...'),
    wkbk.writeWorkbook()
    
    #=== openpyxl getting index error after deleting this 'Sheet'
    #try: wkbk.remove_sheet( wkbk.get_sheet_by_name('Sheet') )
    #except: print('No sheet named \'Sheet\'')
    
    wkbk.save(save_path)
    print('DONE')
    print('ALL DONE!\nSaved workbook: %s')%save_path

def getTraceTypes(dendrite_rObj):
    '''Returns a list of all the trace types in a dendrite rObject (alphabetical order)'''
    trace_types = []
    for protrusion in dendrite_rObj.children:
        for trace in protrusion.children:
            trace_types.append(trace.type)
    return sorted(list(set(trace_types)))

def getProtrusionSpacing( dendrite_rObject ):
    #=== subchildren finding sucks, fix this (cant just go off of last character)
    '''Returns a dictionary of protrusion keys and values representing how much extra spacing is needed in the sheet'''
    prot_spacing = {}
    for protrusion in dendrite_rObject.children:
        spacing = 0
        for child in protrusion:
            # If child has subchildren, adjust spacing
            if child.name[-1].isalpha() and ord(child.name[-1]) - 97 > spacing:
                spacing = ord(child.name[-1])-97
        prot_spacing[protrusion.name] = spacing
    return prot_spacing

class excelWorkbook(openpyxl.Workbook):
    def __init__(self):
        openpyxl.Workbook.__init__(self)
        
        self.dendriteFilter = []
        # traces to ignore in self.getDendriteDict()
        self.filter = ['d[0-9][0-9]c[0-9][0-9]',
                       '.{0,} .{0,}']
        self.dendriteDict = None
        
    def getDendriteDict(self, series):
       
        def shouldBeFiltered(child):
            for filt in self.filter:
                if re.compile(filt).match(child.name) != None:
                    return True
            return False
            
        # Need to filter out objects in self.filter, make copy of dict 1st
        preDendriteDict = series.getObjectHierarchy(*series.getObjectLists())
        dendrites = [preDendriteDict[dendrite] for dendrite in preDendriteDict]
        
        # Make new dict for after filter
        dendriteDict = {}
        for dendrite in dendrites:
            prots = [prot for prot in dendrite.children] # list of protrusion rObjects
            newProts = []
            for prot in prots:
                children = [child for child in prot] # list of children rObjects
                
                # check each child.name, if matches a filter -> remove for children list
                newChildren = []
                for child in children:
                    if shouldBeFiltered(child):
                        continue
                    else:
                        newChildren.append(child)
                    
                prot.children = newChildren
                newProts.append(prot)
            dendrite.children = newProts
            dendriteDict[dendrite.name] = dendrite
                
        self.dendriteDict = dendriteDict
    
    def writeProtrusions(self, dendrite_rObj, sheet):
        '''Writes data and headers for protrusions with correct with spacing'''
        prot_spacing = getProtrusionSpacing(self.dendriteDict[dendrite_rObj.name])
        prot_by_start = sorted([prot for prot in self.dendriteDict[dendrite_rObj.name].children], key=lambda rObject: rObject.start)
        
        row=0
        column=0
        # Write protrusion column headers
        sheet.cell(row=row, column=column).value = 'Protrusion Name'
        sheet.cell(row=row, column=column+1).value = 'Start'
        sheet.cell(row=row, column=column+2).value = 'End'
        sheet.cell(row=row, column=column+3).value = 'Count'
        sheet.cell(row=row, column=column+4).value = 'Surface Area'
        sheet.cell(row=row, column=column+5).value = 'Flat Area'
        sheet.cell(row=row, column=column+6).value = 'Volume'
        
        # Write protrusions and data
        for prot in prot_by_start:
            row += 1
            sheet.cell(row=row, column=column).value = prot.name
            sheet.cell(row=row, column=column+1).value = prot.start
            sheet.cell(row=row, column=column+2).value = prot.end
            sheet.cell(row=row, column=column+3).value = prot.count
            sheet.cell(row=row, column=column+4).value = prot.surfacearea
            sheet.cell(row=row, column=column+5).value = prot.flatarea
            sheet.cell(row=row, column=column+6).value = prot.volume
            row += prot_spacing[prot.name]
    
    def writeWorkbook(self):
        '''Writes data from a loaded dendrite dictionary to a worksheet'''
        # for each dendrite in the dictionary, create a sheet and fill with data
        for dendrite in self.dendriteDict:
            # Create sheet
            sheet_name = self.dendriteDict[dendrite].series.name+' '+self.dendriteDict[dendrite].name
            # Rename the sheet if series name > 10 characters long
            if len(sheet_name) > 10:
                sheet_name = self.dendriteDict[dendrite].series.name[0:5]+' '+self.dendriteDict[dendrite].name
            self.create_sheet(title=sheet_name)
            sheet = self.get_sheet_by_name(sheet_name)
            
            # Protrusion spacing
            prot_spacing = getProtrusionSpacing(self.dendriteDict[dendrite])
            
            # Write protrusion data and column headers
            self.writeProtrusions( self.dendriteDict[dendrite], sheet )
            types = getTraceTypes( self.dendriteDict[dendrite] )
            
            sorted_prots = sorted([prot for prot in self.dendriteDict[dendrite]], key=lambda rObject: rObject.start)
            
            # Write traces
            column = 8
            # Each trace type
            types = [tType for tType in types if tType not in self.filter]
            for tType in types:
                # Column headers
                sheet.cell(row=0, column=column).value = 'Object Name'
                sheet.cell(row=0, column=column+1).value = 'Start'
                sheet.cell(row=0, column=column+2).value = 'End'
                sheet.cell(row=0, column=column+3).value = 'Count'
                sheet.cell(row=0, column=column+4).value = 'Surface Area'
                sheet.cell(row=0, column=column+5).value = 'Flat Area'
                sheet.cell(row=0, column=column+6).value = 'Volume'
                if 'cfa' in tType:
                    sheet.cell(row=0,column=column+7).value = 'Total Volume'
                    
                row = 1 # reset row for each trace type
                for protrusion in sorted_prots:
                    protrusionChildren = [child for child in protrusion if re.compile(tType).match(child.name)]
                    for child in sorted(protrusionChildren, key=lambda rObject: rObject.name):
                        sheet.cell(row=row,column=column).value = child.name
                        sheet.cell(row=row,column=column+1).value = child.start
                        sheet.cell(row=row,column=column+2).value = child.end
                        sheet.cell(row=row,column=column+3).value = child.count
                        sheet.cell(row=row,column=column+4).value = child.surfacearea
                        sheet.cell(row=row,column=column+5).value = child.flatarea
                        sheet.cell(row=row,column=column+6).value = child.volume
                        if 'cfa' in tType:
                            sheet.cell(row=row,column=column+7).value = child.totalvolume
                        row+=1
                    # Add appropriate spacing
                    if len(protrusionChildren) != prot_spacing[protrusion.name]+1:
                        row+=prot_spacing[protrusion.name]+1-len(protrusionChildren)
                column+=8
                if 'cfa' in tType: # one more column shift for the totalvolume attribute
                    column+=1
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates an excel workbook containing protrusions and data, YAY!')
    parser.add_argument('series', nargs=1, type=str, help='Path to the series/sections that needs to be re-scaled')
    parser.add_argument('savepath', nargs=1, help='Directory where the excel workbook will be saved')
    args = vars(parser.parse_args())
    # Assign argparse things to their variables
    path_to_series = str(args['series'][0])
    save_path = str(args['savepath'][0])
    main(path_to_series, save_path)