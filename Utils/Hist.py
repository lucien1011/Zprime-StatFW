import ROOT,math

def getIntegral(hist):
    error = ROOT.Double(0.)
    integral = hist.IntegralAndError(
            0,
            hist.GetNbinsX()+1,
            #1,
            #hist.GetNbinsX(),
            error,
            )
    return integral,error

def getCountAndErrorByRange(hist,lower_value,upper_value,):
    error = ROOT.Double(0.)
    integral = hist.IntegralAndError(
            hist.GetXaxis().FindFixBin(lower_value),
            hist.GetXaxis().FindFixBin(upper_value),
            error,
            )
    return integral,error

def getCountAndError(hist,central,width,isSR=True):
    lower_value = central*(1.-width)
    upper_value = central*(1.+width)

    if isSR:
        error = ROOT.Double(0.)
        integral = hist.IntegralAndError(
                hist.GetXaxis().FindFixBin(lower_value),
                hist.GetXaxis().FindFixBin(upper_value),
                error,
                )
    else:
        error1 = ROOT.Double(0.)
        integral1 = hist.IntegralAndError(
                0,
                hist.GetXaxis().FindFixBin(lower_value)-1,
                error1,
                )
        error2 = ROOT.Double(0.)
        integral2 = hist.IntegralAndError(
                hist.GetXaxis().FindFixBin(upper_value)+1,
                hist.GetNbinsX()+1,
                error2,
                )
        integral = integral1+integral2
        error = math.sqrt(error1**2+error2**2)
    return integral,error
