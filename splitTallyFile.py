# coding = gbk
# module name : splitTallyFile
import re
import preprocess

def splitTallyFile(TallyFile, MeshIDchoice, TimeStep, existPredictor, TotalTimeStep):
    
    # ugly function. 5 parameters in total! Someone must please save this ugly work.
    # 
    # if TimeStep == 0:    
    #     existPredictor = preprocess.JudgePredictor(TallyFile)
    #     TallyFile.seek(0)
    #     
    #     TotalTimeStep = preprocess.getTotalTimeStep(TallyFile)
    #     TallyFile.seek(0)
    
    if existPredictor and (TimeStep != TotalTimeStep):
        Head = 'Current burnup step\(Predictor\)'
    else:
        Head = 'Current burnup step:'
    
    singleTallyFile = open('inp.tally%s'%(TimeStep),'w')
    
    StartFlag = False
    PrintFlag = False
    
    for line in TallyFile:
    
        findHead = re.findall(Head,line) !=[]
        endHead = re.findall('in total =+',line) != []
        
        findIDstart = re.findall('ID = %s'%(MeshIDchoice),line) !=[]
        findEnd = (re.findall('Cstally printing is switched off',line) !=[])\
                or (re.findall('-+\s+ID = %s'%( MeshIDchoice+1 ), line) != [])
        
        if findHead:
            StartFlag = True
            PrintFlag = True
        if StartFlag and endHead:
            PrintFlag = False
        if StartFlag and findIDstart:
            PrintFlag = True
        if StartFlag and findEnd:
            PrintFlag = False
            StartFlag = False
            singleTallyFile.close()
            print 'One single tally file of timestep %s has been splited successfully'%TimeStep
            break
        if PrintFlag:
            singleTallyFile.write(line)