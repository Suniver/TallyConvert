# TallyConvert

**Desciption of the function**  
This small script can help convert the burnup.tally file to tecplot .dat file &amp; tabular file

**How to use it**  
1. Put your burnup.tally file and the **TallyConvertor.py**, **preprocess.py**, **splitTallyFile.py** and **postprocess.py** in one directory  
2. Run the **TallyConvertor.py** script  
3. Follow the options on your command window  
4. Enjoy

**What does the code do**  
1. Split the big burnup.tally file into several single-time-step tally files  
2. If you choose to create tecplot .dat files, the code will convert those small tally files to corresponding data files  
3. Else if you choose to create tabular files, the code will extract **Ave** and **Re** data and write them to Ave file and Re file respectively  
