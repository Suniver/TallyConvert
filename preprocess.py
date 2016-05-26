# coding = gbk
# module name : preprocess
import os
import glob
import re

def getTallyFileName():

    originalTallyFileNameList = sorted(glob.glob('*.Tally'),key=os.path.getmtime)
    existsTallyFile = originalTallyFileNameList != []
    
    while not existsTallyFile:
        print 'Warning!! Do not exist a *.Tally file!'
        print 'Put your *.Tally file in the same directory this python script'
        raw_input('If you have put your file in the right directory, press enter')
        originalTallyFileNameList = sorted(glob.glob('*.Tally'),key=os.path.getmtime)
        existsTallyFile = originalTallyFileNameList != []
    
    return originalTallyFileNameList[0]

def JudgePredictor(TallyFile):
    iteration = 0
    existPredictor = False
    
    for line in TallyFile:
        
        iteration += 1
        if iteration ==2:
            break
        
        findPredictor = re.findall(r'Predictor',line) !=[]
        if findPredictor:
            existPredictor = True
            
    return existPredictor
    
def getMeshIDcount(TallyFile):
    iteration = 0
    MeshIDcount = 1
    
    for line in TallyFile:
        
        iteration += 1
        if iteration == 4:
            break
        
        findMeshIDcount = re.findall('\d Mesh tally in total', line) != []
        if findMeshIDcount:
            MeshIDcount = int(re.findall('(\d) Mesh tally in total', line)[0])
            
    return MeshIDcount
    
def getTotalTimeStep(TallyFile):
    iteration = 0
    TotalTimeStep = 1
    
    for line in TallyFile:
    
        iteration += 1
        if iteration == 4:
            break
            
        findTotalTimeStep = re.findall('\d+/(\d+)',line) !=[]
        if findTotalTimeStep:
            TotalTimeStep = int(re.findall('\d+/(\d+)',line)[0])
            
    return TotalTimeStep
    
def getXYZMeshes(TallyFile, MeshIDchoice, existPredictor):
    
    StartFlag = False
    PrintFlag = False
    Xmax = 0
    Ymax = 0
    Zmax = 0
    
    if existPredictor:
        Head = 'Current burnup step\(Predictor\)'
    else:
        Head = 'Current burnup step:'
    
    for line in TallyFile:
    
        findHead = re.findall(Head,line) !=[]
        endHead = re.findall('in total =+',line) != []
        
        findIDstart = re.findall('ID = %s'%(MeshIDchoice),line) !=[]
        findEndFlag = (re.findall('Cstally printing is switched off',line) !=[])\
                or (re.findall('-+\s+ID = %s'%( MeshIDchoice+1 ), line) != [])
        
        if findHead:
            StartFlag = True
            PrintFlag = True
        if StartFlag and endHead:
            PrintFlag = False
        if StartFlag and findIDstart:
            PrintFlag = True
        if StartFlag and findEndFlag:
            PrintFlag = False
            StartFlag = False
            break
        if PrintFlag:
            if re.findall('(\d+)\s+\d+\s+\d+\s+',line) != []:
                Xmax = max(Xmax, int(re.findall('(\d+)\s+\d+\s+\d+\s+',line)[0]))
                Ymax = max(Ymax, int(re.findall('\d+\s+(\d+)\s+\d+\s+',line)[0]))
                Zmax = max(Zmax, int(re.findall('\d+\s+\d+\s+(\d+)\s+',line)[0]))
            
    return [Xmax, Ymax, Zmax]