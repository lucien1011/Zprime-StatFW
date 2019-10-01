import os,copy,math,argparse,ROOT

from CombineStatFW.DataCard import DataCard,CardConfig
from CombineStatFW.Systematic import *
from CombineStatFW.Process import *
from CombineStatFW.Reader import *
from CombineStatFW.Channel import Bin
from CombineStatFW.FileReader import FileReader
from CombineStatFW.RateParameter import RateParameter

from Utils.Hist import getCountAndError,getIntegral,getCountAndErrorByRange
from Utils.DataCard import SignalModel
from Utils.mkdir_p import mkdir_p

# ____________________________________________________________________________________________________________________________________________ ||
parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--verbose",action="store_true")
parser.add_argument("--elWidth",action="store",type=float,default=0.05)
parser.add_argument("--muWidth",action="store",type=float,default=0.02)
parser.add_argument("--massPoints",action="store")

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
        #10,
        15,
        20,
        30,
        40,
        50,
        60,
        70,
        ] 
if option.massPoints: mass_points = [ int(m) for m in option.massPoints.split(",") ]
signal_models = [ 
        SignalModel("ZpToMuMu_M"+str(m),["zpToMuMu_M"+str(m),],m) for m in mass_points 
        ]

data_names = [
        #"Data",
        "qqZZ",
        ]

bkg_names = [
        "qqZZ",
        "ggZZ",
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# bin list
binList = [
        Bin("FourMu_MVA1",signalNames=["zpToMuMu",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="",width=option.muWidth,inputBinNameFunc=lambda x: "NNProb_M%s_4mu"%str(x.central_value),countFunc=lambda hist: getCountAndErrorByRange(hist,0.0,0.2) ),
        Bin("FourMu_MVA2",signalNames=["zpToMuMu",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="",width=option.muWidth,inputBinNameFunc=lambda x: "NNProb_M%s_4mu"%str(x.central_value),countFunc=lambda hist: getCountAndErrorByRange(hist,0.2,0.4)),
        Bin("FourMu_MVA3",signalNames=["zpToMuMu",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="",width=option.muWidth,inputBinNameFunc=lambda x: "NNProb_M%s_4mu"%str(x.central_value),countFunc=lambda hist: getCountAndErrorByRange(hist,0.4,0.6)),
        Bin("FourMu_MVA4",signalNames=["zpToMuMu",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="",width=option.muWidth,inputBinNameFunc=lambda x: "NNProb_M%s_4mu"%str(x.central_value),countFunc=lambda hist: getCountAndErrorByRange(hist,0.6,0.8)),
        Bin("FourMu_MVA5",signalNames=["zpToMuMu",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="",width=option.muWidth,inputBinNameFunc=lambda x: "NNProb_M%s_4mu"%str(x.central_value),countFunc=lambda hist: getCountAndErrorByRange(hist,0.8,0.9)),
        Bin("FourMu_MVA6",signalNames=["zpToMuMu",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="",width=option.muWidth,inputBinNameFunc=lambda x: "NNProb_M%s_4mu"%str(x.central_value),countFunc=lambda hist: getCountAndErrorByRange(hist,0.9,1.0)),
        
        #Bin("FourMu_MVA1",signalNames=["zpToMuMu",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="",width=option.muWidth,inputBinNameFunc=lambda x: "NNProb_M%s_4mu"%str(x.central_value),countFunc=lambda hist: getCountAndErrorByRange(hist,0.2,0.4)),
        #Bin("FourMu_MVA2",signalNames=["zpToMuMu",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="",width=option.muWidth,inputBinNameFunc=lambda x: "NNProb_M%s_4mu"%str(x.central_value),countFunc=lambda hist: getCountAndErrorByRange(hist,0.4,0.6)),
        #Bin("FourMu_MVA3",signalNames=["zpToMuMu",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="",width=option.muWidth,inputBinNameFunc=lambda x: "NNProb_M%s_4mu"%str(x.central_value),countFunc=lambda hist: getCountAndErrorByRange(hist,0.6,0.8)),
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
    central_value = signal_model.central_value
    binListCopy = [b for b in copy.deepcopy(binList) ]
    for ibin,bin in enumerate(binListCopy):
        if option.verbose: print "-"*20
        if option.verbose: print bin.name
        histName = bin.inputBinName if not bin.inputBinNameFunc else bin.inputBinNameFunc(signal_model)

        # bkg
        for bkgName in bkg_names:
            reader.openFile(inputDir,bkgName,TFileName)
            hist = reader.getObj(bkgName,histName)
            #count,error = getCountAndError(hist,central_value,bin.width,isSR=isSRFunc(bin))
            count,error = bin.countFunc(hist)
            process = Process(bkgName,count if count >= 0. else 1e-12,error)
            bin.processList.append(process)

        # data
        dataCount = 0.
        for sample in data_names:
            reader.openFile(inputDir,sample,TFileName)
            hist = reader.getObj(sample,histName)
            #count,error = getCountAndError(hist,central_value,bin.width,isSR=isSRFunc(bin))
            count,error = bin.countFunc(hist)
            dataCount += count
        error = math.sqrt(dataCount)
        bin.data = Process("data_obs",int(dataCount),error)
        
        bin.systList = []
        
        # signal
        for each_signal_model_name in signal_model.signal_list:
            reader.openFile(inputDir,each_signal_model_name,TFileName)
            hist = reader.getObj(each_signal_model_name,histName)
            #count,error = copy.deepcopy(getCountAndError(hist,central_value,bin.width,isSR=isSRFunc(bin)))
            count,error = bin.countFunc(hist)
            bin.processList.append(Process(each_signal_model_name,count if count >= 0. else 1e-12,error)) 
            # systematics
            if count:
                mcSyst = lnNSystematic("SigStat_"+bin.name,[ each_signal_model_name, ],lambda syst,procName,anaBin: float(1.+error/count))
                #bin.systList.append(mcSyst)
        
        for syst in commonLnSystematics:
            bin.systList.append(copy.deepcopy(syst))
        bin.systList += lnSystReader.makeLnSyst(bin.sysFile)

    config = CardConfig(signal_model_name)
    dataCard = DataCard(config) 
    cardDir = outputDir+"/"+dataCard.makeOutFileName("/","")
    mkdir_p(cardDir)
    dataCard.makeCard(cardDir,binListCopy)
    reader.end()
