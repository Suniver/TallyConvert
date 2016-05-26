# coding = gbk
# module name: postprocess
import re
import os

class Tecplot:
    """
    this class will help handle the tecplot data file
    data title, variablenames, variables ,solutionstime, xnode, ynode, znode are required
    """
    def __init__(self, Title = 'tecplot.dat', VariableNameList = ['X','Y','Z'],\
                 VariableList = [], SolutionTime = 0.0,\
                 XNodes = 1, YNodes = 1, ZNodes = 1):
        self.Title = Title
        self.VariableNameList = VariableNameList
        self.VariableList = VariableList
        # VariableList is a two-dimentional list containing all the variables
        self.SolutionTime = SolutionTime
        self.XNodes = XNodes
        self.YNodes = YNodes
        self.ZNodes = ZNodes
        
    def outputTecplotFile(self, TecplotFile):
        TecplotFile.write('Title = \"%s\"\n'%self.Title)
        
        TecplotFile.write('Variables = ')
        for VariableName in self.VariableNameList[:-1]:
            TecplotFile.write('\"%s\",'%VariableName)
        TecplotFile.write('\"%s\"\n'%self.VariableNameList[-1])
        
        TecplotFile.write('ZONE SOLUTIONTIME = %f I = %d J = %d K = %d F=POINT\n'%(self.SolutionTime,self.XNodes,self.YNodes,self.ZNodes))
        
        for Variables in self.VariableList:
            # Variables is a list containing the coordinates and 
            # corresponding temperature, power, ect. of every single point
            for Variable in Variables:
                TecplotFile.write('%s    '%(str(Variable)))
            TecplotFile.write('\n')
            
def getTimePoint(singleTallyFile):
    TimePoint = 0.0
    for line in singleTallyFile:
        
        findTimePoint = re.findall('Total step time\(Day\): ([.\d]*)',line)
        
        if  findTimePoint != []:
            TimePoint = float(findTimePoint[0])
            singleTallyFile.seek(0)
            return TimePoint
    
def getAveAndRe(singleTallyFile):
    
    TallyFileContent = singleTallyFile.read()
    
    TallyAve = re.findall('\s+\d+\s+([+-]*[.\d]+[Ee][+-]*[\d]+)',TallyFileContent)
    TallyRe = re.findall('\s+\d+\s+[+-]*[.\d]+[Ee][+-]*[\d]+\s+([+-]*[.\d]+[Ee][+-]*[\d]+)',TallyFileContent)
    
    return [TallyAve, TallyRe]

def normalize(TallyAve):
    
    TallyFluxSum = 0
    for j in range(0,len(TallyAve)):
        TallyFluxSum += float(TallyAve[j])
        
    TallyFlux = []
    for j in range(0,len(TallyAve)):
        TallyFlux.append(float(TallyAve[j])/TallyFluxSum)
    
    for j in range(0,len(TallyAve)):
        TallyAve[j] = '%.4E'%(TallyFlux[j])
        
def createTecplotFile(TallyAve, TecplotFileName, singleTallyFileName, Legend, TimePoint, Xnodes, Ynodes, Znodes):

    MeshBurnup = []
    for z in range(Znodes):
        for y in range(Ynodes):
            for x in range(Xnodes):
                MeshBurnup.append([x+1, y+1, z+1, str(TallyAve[x+Xnodes*y+Xnodes*Ynodes*z])])
                
    TecplotObject = Tecplot(TecplotFileName+singleTallyFileName[9:],['X','Y','Z',Legend],\
                        MeshBurnup, TimePoint, Xnodes,Ynodes,Znodes)
    TecplotFile = open('%s%s.dat'%(TecplotFileName,singleTallyFileName[9:]),'w')
    TecplotObject.outputTecplotFile(TecplotFile)
    TecplotFile.close()
    
def createTable(i, TallyX, TypeName):
    if i == 0:
        TabularXFile = open(TypeName,'w')
        
        for RowCount in range(0,len(TallyX)):
            if RowCount == 0:
                TabularXFile.write('%s'%(TallyX[RowCount]))
            else:
                TabularXFile.write('\n%s'%(TallyX[RowCount]))
        TabularXFile.close()
    
    if i > 0:
        TabularXFile = open(TypeName,'r')
        newTabularXFile = open('new%s'%(TypeName),'w')
        
        TotalRow = 0
        for line in TabularXFile:
            TotalRow += 1
        TabularXFile.seek(0)
        
        RowCount = 0
        for line in TabularXFile:
            if RowCount != TotalRow - 1:
                newTabularXFile.write('%s     %s\n'%(line[:-1], TallyX[RowCount]))
            if RowCount == TotalRow - 1:
                newTabularXFile.write('%s     %s'%(line, TallyX[RowCount]))
            RowCount += 1
        
        TabularXFile.close()
        newTabularXFile.close()
    
        os.remove(TypeName)
        os.rename('new%s'%(TypeName),TypeName)