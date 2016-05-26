# coding = gbk
# program name: TallyToTecplot

import re
import glob
import os
import sys
from splitTallyFile import splitTallyFile
import preprocess
import postprocess

os.chdir(sys.path[0])

# ===== preprocessing =====
# Get the name of the original tally file 
# and its features, including predictor method, total time steps, meshID counts
# Ask the user to input how many time steps to be extracted, 
# and which type of mesh to be extracted, then figure out the data structure of the mesh selected

originalTallyFileName = preprocess.getTallyFileName()
print 'Your *.Tally file is : %s\n'%(originalTallyFileName)

with open(originalTallyFileName,'r') as originalTallyFile:
    existPredictor = preprocess.JudgePredictor(originalTallyFile)
    originalTallyFile.seek(0)
    
    TotalTimeStep = preprocess.getTotalTimeStep(originalTallyFile)
    originalTallyFile.seek(0)
    
    MeshIDcount = preprocess.getMeshIDcount(originalTallyFile)
    originalTallyFile.seek(0)

if existPredictor:
    print 'There are predictor method in your mesh tally file\n'

print 'There are %s time steps in total in your mesh tally file'%(TotalTimeStep+1)
TimeStepsRequired = int(raw_input('How many time steps do you want to extract?:'))
print '\n'

print 'There are %s types of mesh tally in total in your mesh tally file'%MeshIDcount
MeshIDchoice = int(raw_input('Input the ID number you want to extract:'))
print ''
print 'waiting...\n'

with open(originalTallyFileName, 'r') as BurnupTallyFile:
    Xnodes, Ynodes, Znodes = preprocess.getXYZMeshes(BurnupTallyFile, MeshIDchoice, existPredictor)
    
print 'There are %s meshes in X direction of your Mesh ID'%(Xnodes)
print 'There are %s meshes in Y direction of your Mesh ID'%(Ynodes)
print 'There are %s meshes in Z direction of your Mesh ID\n'%(Znodes)

# ===== postprocessing configuration =====
# ask the user to select one postprocessor

print 'What type of data file do you want?'
print 'input a for tecplot data file'
print 'input b for table-formatted file'
print 'a or b?"'
OutputMode = raw_input('')
while OutputMode != 'a' and OutputMode != 'b':
    print 'Input Error! Input again:'
    OutputMode = raw_input('')

print '\n'

if OutputMode == 'a':
    Legend = raw_input('What type is your data? Power, Flux, or something else?:')
    print '\n'
    TecplotFileName = 'tally'
    
Normalization = False

# ===== processing =====
# split original tally file into single small tally file

with open(originalTallyFileName,'r') as BurnupTallyFile:
    
    for TimeStep in range(0, TimeStepsRequired):
        splitTallyFile(BurnupTallyFile, MeshIDchoice, TimeStep, existPredictor, TotalTimeStep)

# ===== postprocessing ======
# extract Tally average data and res data
# and write them into tecplot file or tabular file

singleTallyFileNameList = sorted(glob.glob('inp.tally*'),key=os.path.getmtime)

if OutputMode == 'a':

print 'Waiting, writing tecplot data file ...'
    
    for singleTallyFileName in singleTallyFileNameList:
        
        with open(singleTallyFileName,'r') as singleTallyFile:
            
            TimePoint = postprocess.getTimePoint(singleTallyFile)
            [TallyAve, TallyRe] = postprocess.getAveAndRe(singleTallyFile)
        
        if Normalization:
            postprocess.normalize(TallyAve)
        
        postprocess.createTecplotFile(TallyAve, TecplotFileName, singleTallyFileName, \
                                      Legend, TimePoint, Xnodes, Ynodes, Znodes)

if OutputMode == 'b':

print 'Waiting, writing tabular file ...'

    for i in range(0,len(singleTallyFileNameList)):
    
        with open(singleTallyFileNameList[i],'r') as singleTallyFile:
            
            TimePoint = postprocess.getTimePoint(singleTallyFile)
            [TallyAve, TallyRe] = postprocess.getAveAndRe(singleTallyFile)
            
        if Normalization:
            postprocess.normalize(TallyAve)
        
        postprocess.createTable(i, TallyAve, 'Ave')
        postprocess.createTable(i, TallyRe, 'Re')
        
print 'Done.'