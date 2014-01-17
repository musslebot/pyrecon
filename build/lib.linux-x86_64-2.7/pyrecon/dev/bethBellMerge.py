from pyrecon.tools.mergeTool import *
def bethBellMerge(path_FPNCT_BB, path_FPNCT_JNB): #===
    # First load FPNCT_BB and delete everything except those in saveList
    saveList = [re.compile('[d][0-9]{0,2}vftz[0-9]{0,2}[a-z]?$', re.I), # d##vftz##_
                re.compile('[d][0-9]{0,2}vftzcfa[0-9]{0,2}[a-z]?$', re.I), # d##vftzcfa##_
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}[a-z]?$', re.I), # d##ax##_
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}dcv[0-9]{0,2}[a-z]?$', re.I), # d##ax##dcv##_
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}dssvdh[0-9]{0,2}[a-z]?$', re.I), # d##ax##dssvdh##_
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}dssvrh[0-0]{0,2}[a-z]?$', re.I), # d##ax##dssvrh##_
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}dssvrhclose[0-9]{0,2}[a-z]?$', re.I), # d##ax##dssvrhclose##_
                re.compile('[d][0-9]{0,2}c[0-9]{0,2}[a-z]?$', re.I), # d##c##_
                re.compile('[d][0-9]{0,2}c[0-9]{0,2}scale[0-9]{0,2}[a-z]?$', re.I), # d##c##scale##_
                re.compile('[d][0-9]{0,2}cfa[0-9]{0,2}[a-z]?$', re.I)] # d##cfa##_
    ser1 = loadSeries(path_FPNCT_BB)
    for section in ser1.sections:
        savedContours = []
        for contour in section.contours:
            for prog in saveList:
                if len(prog.findall(contour.name)) != 0:
                    savedContours.append(contour)
                    break
        section.contours = savedContours
    
    # Now load FPNCT_JNB and delete everything in delList
    delList = [re.compile('[d][0-9]{0,2}c[0-9]{0,2}[a-z]?$', re.I), # d##c##_
               re.compile('[d][0-9]{0,2}cfa[0-9]{0,2}[a-z]?$', re.I)] # d##cfa##_
    
    ser2 = loadSeries(path_FPNCT_JNB)
    for section in ser2.sections:
        deletedContours = []
        for contour in section.contours:
            for prog in delList:
                if len(prog.findall(contour.name)) != 0:
                    deletedContours.append(contour.name)
                    break
        section.contours = [cont for cont in section.contours if cont.name not in deletedContours]
    
    ser3 = mergeSeries(ser1, ser2, name='FPNCT_merge')
    # imageOverride set to 2; imageOverride 1 has different image and domain1 transforms
    ser3.sections = mergeAllSections(ser1, ser2, name='FPNCT_merge', imageOverride=2)
    
    # OUTPUT
    ser3.writeseries('/home/michaelm/Documents/Test Series/bb/FPNCT_merge/')
    ser3.writesections('/home/michaelm/Documents/Test Series/bb/FPNCT_merge/')
    