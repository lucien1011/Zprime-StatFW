import os,copy,math,argparse,ROOT

from CombineStatFW.DataCard import DataCard,CardConfig
from CombineStatFW.Systematic import *
from CombineStatFW.Process import *
from CombineStatFW.Reader import *
from CombineStatFW.Channel import Bin
from CombineStatFW.FileReader import FileReader
from CombineStatFW.RateParameter import RateParameter

from Utils.Hist import getCountAndError,getIntegral
from Utils.DataCard import SignalModel
from Utils.mkdir_p import mkdir_p

# ____________________________________________________________________________________________________________________________________________ ||
parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--verbose",action="store_true")
parser.add_argument("--elWidth",action="store",type=float,default=0.05)
parser.add_argument("--muWidth",action="store",type=float,default=0.02)

option = parser.parse_args()

# ____________________________________________________________________________________________________________________________________________ ||
# Configurable
inputDir = option.inputDir
commonLnSystFilePath = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/CommonSyst_2mu2e.txt"
lnSystFilePathDict = {
        "TwoMu": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_2mu.txt", 
        "TwoEl": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_2e.txt", 
        }
outputDir = option.outputDir
TFileName = "StatInput.root"
isSRFunc = lambda x: x.name.endswith("SR")

# ____________________________________________________________________________________________________________________________________________ ||
# mass window
mass_points = [
        5,
        15,
        ] + range(20,80,10)
signal_models = [ 
        SignalModel("ZpToMuMu_MZp"+str(m),["zpToMuMu_M"+str(m),],m) for m in mass_points 
        ]

data_names = [
        "Data",
        ]

bkg_names = [
        "qqZZ",
        "ggZZ",
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# bin list
binList = [
        Bin("FourMu_SR",signalNames=["zpToMuMu",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu_HiggsSR",width=option.muWidth),
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# syst
lnSystReader = LogNormalSystReader()
commonLnSystematics = lnSystReader.makeLnSyst(commonLnSystFilePath)

# ____________________________________________________________________________________________________________________________________________ ||
reader = FileReader()

mkdir_p(os.path.abspath(outputDir))

for signal_model in signal_models:
    signal_model_name = signal_model.name
    if option.verbose: print "*"*100
    if option.verbose: print "Making data card for ",signal_model_name
    #central_value = float(signal_model_name.replace("HZZd_M",""))
    central_value = signal_model.central_value
    binListCopy = [b for b in copy.deepcopy(binList) if option.sideband or (not option.sideband and "SR" in b.name)]
    for ibin,bin in enumerate(binListCopy):
        if option.verbose: print "-"*20
        if option.verbose: print bin.name
        histName = bin.inputBinName

        # bkg
        for bkgName in bkg_names:
            reader.openFile(inputDir,bkgName,TFileName)
            hist = reader.getObj(bkgName,histName)
            count,error = getCountAndError(hist,central_value,bin.width,isSR=isSRFunc(bin))
            process = Process(bkgName,count if count >= 0. else 1e-12,error)
            bin.processList.append(process)

        # data
        dataCount = 0.
        for sample in data_names:
            reader.openFile(inputDir,sample,TFileName)
            hist = reader.getObj(sample,histName)
            count,error = getCountAndError(hist,central_value,bin.width,isSR=isSRFunc(bin))
            dataCount += count
        error = math.sqrt(dataCount)
        bin.data = Process("data_obs",int(dataCount),error)
        
        bin.systList = []
        
        # signal
        for each_signal_model_name in signal_model.signal_list:
            if bin.name.endswith("_SR"): 
                for key in bin.interFuncDict:
                    if key in each_signal_model_name: break
                count = bin.interFuncDict[key].Eval(central_value)
            else:
                count = 0.
            bin.processList.append(Process(each_signal_model_name,count if count > 0. else 1e-12,0.))
        
        for syst in commonLnSystematics:
            bin.systList.append(copy.deepcopy(syst))
        bin.systList += lnSystReader.makeLnSyst(bin.sysFile)

    config = CardConfig(signal_model_name)
    dataCard = DataCard(config) 
    cardDir = outputDir+"/"+dataCard.makeOutFileName("/","")
    mkdir_p(cardDir)
    dataCard.makeCard(cardDir,binListCopy)
    reader.end()