#!/bin/bash

#inputDir=/raid/raid7/lucien/Higgs/Zprime/ParaInput/EXO-18-001-Nominal/2019-06-05/
#outputDir=DataCard/EXO-18-001-Nominal/2019-06-05/

#inputDir=/raid/raid7/lucien/Higgs/Zprime/ParaInput/EXO-18-001-Nominal/2019-06-06_MVAInput_mZp10/
#inputDir=/raid/raid7/lucien/Higgs/Zprime/ParaInput/EXO-18-001-Nominal/2019-06-06_MVAInput_mZp30/
#inputDir=/raid/raid7/lucien/Higgs/Zprime/ParaInput/EXO-18-001-Nominal/2019-06-06_MVAInput_mZp40/
#outputDir=DataCard/EXO-18-001-Nominal/2019-06-06/

#inputDir=/raid/raid7/lucien/Higgs/Zprime/ParaInput/EXO-18-001-Nominal/2019-06-10/
#inputDir=/raid/raid7/lucien/Higgs/Zprime/ParaInput/EXO-18-001-Nominal/2019-06-10_MVAInput_mZp40/
#outputDir=DataCard/EXO-18-001-Nominal/2019-06-10_MVAInput/

inputDir=/raid/raid7/lucien/Higgs/Zprime/ParaInput/EXO-18-008-MVAShape/2019-06-10_MVAInput/
outputDir=DataCard/EXO-18-008-MVAShape/2019-06-10_MVAInput/

#python makeDataCard.py --inputDir=${inputDir} --outputDir ${outputDir} --verbose
#python makeDataCard.py --inputDir=${inputDir} --outputDir ${outputDir} --verbose --massPoints 40
#python makeMVADataCard.py --inputDir=${inputDir} --outputDir ${outputDir} --verbose

for d in $(ls ${outputDir}); 
do
    echo ${outputDir}/${d}/
    #python makeWorkspace.py --inputDir ${outputDir}/${d}/ --pattern "ZpToMuMu_M*.txt"
    #python makeWorkspace.py --inputDir ${outputDir}/${d}/ --pattern "ZpToMuMu_M4*.txt"
done

#python runCombineTask.py --inputDir ${outputDir} --selectStr "ZpToMuMu_M" --option "-t -1 --run=blind"
python runCombineTask.py --inputDir ${outputDir} --selectStr "ZpToMuMu_M" --option "-t -1 --expectSignal=1" --method=Significance

#python runCombineTask.py --inputDir ${outputDir} --selectStr "ZpToMuMu_M4" --option "-t -1 --run=blind"
