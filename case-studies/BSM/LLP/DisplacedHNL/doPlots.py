#!/usr/bin/env python
import sys, os
import os.path
import ntpath
import importlib
import ROOT
import copy
import re

#__________________________________________________________
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def sortedDictValues(dic):
    keys = sorted(dic)
    return [dic[key] for key in keys]

#__________________________________________________________
def mapHistos(var, label, sel, param):
    print ('run plots for var:{}     label:{}     selection:{}'.format(var,label,sel))
    signal=param.plots[label]['signal']
    backgrounds=param.plots[label]['backgrounds']

    hsignal = {}
    for s in signal:
        hsignal[s]=[]
        for f in signal[s]:
            fin=param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                print ('file {} does not exist, skip'.format(fin))
            else:
                tf=ROOT.TFile(fin)
                h=tf.Get(var)
                hh = copy.deepcopy(h)
                #scaleSig=1.
                if hh.GetSumOfWeights()!=0.:
                    scaleSig=1./hh.GetSumOfWeights()
                else:
                    scaleSig=1.
                try:
                    scaleSig=param.scaleSig
                except AttributeError:
                    print ('no scale signal, using 1')
                if scaleSig != 0.:
                    hh.Scale(scaleSig) 
                #hh.Scale(param.intLumi*scaleSig)
                #hh.Scale(scaleSig)
                if len(hsignal[s])==0:
                    hsignal[s].append(hh)
                else:
                    hh.Add(hsignal[s][0])
                    hsignal[s][0]=hh


    hbackgrounds = {}
    for b in backgrounds:
        hbackgrounds[b]=[]
        for f in backgrounds[b]:
            fin=param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                print ('file {} does not exist, skip'.format(fin))
            else:
                tf=ROOT.TFile(fin)
                h=tf.Get(var)
                hh = copy.deepcopy(h)
                if hh.GetSumOfWeights()!=0.:
                    scale=1./hh.GetSumOfWeights()
                else:
                    scale=1.
                try:
                    scale=param.scaleBack
                except AttributeError:
                    print ('no scale background, using 1')
                if scale != 0.:
                    hh.Scale(scale)
                #print('entries ', hh.GetEntries())
                #hh.Scale(param.intLumi)
                if len(hbackgrounds[b])==0:
                    hbackgrounds[b].append(hh)
                else:
                    hh.Add(hbackgrounds[b][0])
                    hbackgrounds[b][0]=hh

    for s in hsignal:
        if len(hsignal[s])==0:
            hsignal=removekey(hsignal,s)

    for b in hbackgrounds:
        if len(hbackgrounds[b])==0:
            hbackgrounds=removekey(hbackgrounds,b)

    return hsignal,hbackgrounds


#__________________________________________________________
def mapEffHistos(denVar, numVar, label, sel, param):
    print ('run efficiency plots for denVar:{}  numVar:{}   label:{}     selection:{}'.format(denVar,numVar,label,sel))
    signal=param.plots[label]['signal']
    backgrounds=param.plots[label]['backgrounds']

    hsignal = {}
    for s in signal:
        hsignal[s]=[]
        for f in signal[s]:
            fin=param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                print ('file {} does not exist, skip'.format(fin))
            else:
                tf=ROOT.TFile(fin)
                denh=tf.Get(denVar)
                denhh = copy.deepcopy(denh)

                numh=tf.Get(numVar)
                numhh = copy.deepcopy(numh)

                #don't scale histograms

                numhh.Divide(denhh)
                if len(hsignal[s])==0:
                    hsignal[s].append(numhh)
                else:
                    hh.Add(hsignal[s][0])
                    hsignal[s][0]=numhh


    hbackgrounds = {}
    for b in backgrounds:
        hbackgrounds[b]=[]
        for f in backgrounds[b]:
            fin=param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                print ('file {} does not exist, skip'.format(fin))
            else:
                tf=ROOT.TFile(fin)
                denh=tf.Get(denVar)
                denhh = copy.deepcopy(denh)

                numh=tf.Get(numVar)
                numhh = copy.deepcopy(numh)

                #don't scale histograms

                numhh.Divide(denhh)
                if len(hbackgrounds[b])==0:
                    hbackgrounds[b].append(numhh)
                else:
                    hh.Add(hbackgrounds[b][0])
                    hbackgrounds[b][0]=numhh

    for s in hsignal:
        if len(hsignal[s])==0:
            hsignal=removekey(hsignal,s)

    for b in hbackgrounds:
        if len(hbackgrounds[b])==0:
            hbackgrounds=removekey(hbackgrounds,b)

    return hsignal,hbackgrounds

#__________________________________________________________
def runPlots(var,param,hsignal,hbackgrounds,extralab,splitLeg):

    ###Below are settings for separate signal and background legends
    if(splitLeg):
    ###Make sure to also change to leg2.AddEntry(...)
        legsize = 0.04*(len(hsignal))
        legsize2 = 0.04*(len(hbackgrounds))
        leg = ROOT.TLegend(0.12,0.66 - legsize,0.46,0.68)
        leg2 = ROOT.TLegend(0.58,0.66 - legsize2,0.86,0.68)
        leg2.SetFillColor(0)
        leg2.SetFillStyle(0)
        leg2.SetLineColor(0)
        leg2.SetShadowColor(10)
        leg2.SetTextSize(0.035)
        leg2.SetTextFont(42)
    else:
        legsize = 0.04*(len(hsignal)+len(hbackgrounds))
        # leg = ROOT.TLegend(0.58,0.86 - legsize,0.86,0.88)
        leg = ROOT.TLegend(0.18,0.66 - legsize,0.46,0.68)
        leg2=None


    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetShadowColor(10)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)

    for b in hbackgrounds:
        if(splitLeg):
            leg2.AddEntry(hbackgrounds[b][0],param.legend[b],"f")
        else:
            leg.AddEntry(hbackgrounds[b][0],param.legend[b],"f")
    for s in hsignal:
        leg.AddEntry(hsignal[s][0],param.legend[s],"l")
 

    histos=[]
    colors=[]

    nsig=len(hsignal)
    nbkg=len(hbackgrounds)

    for s in hsignal:
        histos.append(hsignal[s][0])
        colors.append(param.colors[s])

    for b in hbackgrounds:
        histos.append(hbackgrounds[b][0])
        colors.append(param.colors[b])

    intLumiab = param.intLumi/1e+06 

    
    lt = "FCC-hh Simulation (Delphes)"    
    rt = "#sqrt{{s}} = {:.1f} TeV,   L = {:.0f} ab^{{-1}}".format(param.energy,intLumiab)

    if 'ee' in param.collider:
        lt = "FCC-ee Simulation (Delphes)"

        #rt = "#sqrt{{s}} = {:.1f} GeV".format(param.energy) #if scaleSig==1.
        rt = "#sqrt{{s}} = {:.1f} GeV,   L = {:.0f} ab^{{-1}}".format(param.energy,intLumiab)

    if 'stack' in param.stacksig:
        if 'lin' in param.yaxis:
            drawStack(var+"_stack_lin", 'Events', leg, lt, rt, param.formats, param.outdir, False , True , histos, colors, param.ana_tex, extralab, nsig, nbkg, leg2)
        if 'log' in param.yaxis:
            drawStack(var+"_stack_log", 'Events', leg, lt, rt, param.formats, param.outdir, True , True , histos, colors, param.ana_tex, extralab, nsig, nbkg, leg2)
        if 'lin' not in param.yaxis and 'log' not in param.yaxis:
            print ('unrecognised option in formats, should be [\'lin\',\'log\']'.format(param.formats))

    if 'nostack' in param.stacksig:
        if 'lin' in param.yaxis:
            drawStack(var+"_nostack_lin", 'Events', leg, lt, rt, param.formats, param.outdir, False , False , histos, colors, param.ana_tex, extralab, nsig, nbkg, leg2)
        if 'log' in param.yaxis:
            drawStack(var+"_nostack_log", 'Events', leg, lt, rt, param.formats, param.outdir, True , False , histos, colors, param.ana_tex, extralab, nsig, nbkg, leg2)
        if 'lin' not in param.yaxis and 'log' not in param.yaxis:
            print ('unrecognised option in formats, should be [\'lin\',\'log\']'.format(param.formats))
    if 'stack' not in param.stacksig and 'nostack' not in param.stacksig:
        print ('unrecognised option in stacksig, should be [\'stack\',\'nostack\']'.format(param.formats))



#__________________________________________________________
def runEffPlots(denVar,numVar,param,hsignal,hbackgrounds,extralab):
    legsize = 0.04*(len(hbackgrounds)+len(hsignal))
    #leg = ROOT.TLegend(0.58,0.86 - legsize,0.86,0.88)
    leg = ROOT.TLegend(0.18,0.66 - legsize,0.46,0.68)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetShadowColor(10)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)

    for s in hsignal:
    #    leg.AddEntry("")
        leg.AddEntry(hsignal[s][0],param.legend[s],"l")
    for b in hbackgrounds:
    #    leg.AddEntry("")
        leg.AddEntry(hbackgrounds[b][0],param.legend[b],"f")

    histos=[]
    colors=[]

    for s in hsignal:
        histos.append(hsignal[s][0])
        colors.append(param.colors[s])

    for b in hbackgrounds:
        histos.append(hbackgrounds[b][0])
        colors.append(param.colors[b])

    intLumiab = param.intLumi/1e+06

    lt = "FCC-hh Simulation (Delphes)"
    rt = "#sqrt{{s}} = {:.1f} TeV,   L = {:.0f} ab^{{-1}}".format(param.energy,intLumiab)

    if 'ee' in param.collider:
        lt = "FCC-ee Simulation (Delphes)"
        rt = "#sqrt{{s}} = {:.1f} GeV,   L = {:.0f} ab^{{-1}}".format(param.energy,intLumiab)

    if 'lin' in param.yaxis:
        drawEffPlots("eff_"+denVar+"_"+numVar+"_lin", 'Reco/Gen Efficiency', leg, lt, rt, param.formats, param.outdir, False , True , histos, colors, param.ana_tex, extralab)
    if 'log' in param.yaxis:
        drawEffPlots("eff_"+denVar+"_"+numVar+"_log", 'Reco/Gen Efficiency', leg, lt, rt, param.formats, param.outdir, True , True , histos, colors, param.ana_tex, extralab)
    if 'lin' not in param.yaxis and 'log' not in param.yaxis:
        print ('unrecognised option in formats, should be [\'lin\',\'log\']'.format(param.formats))


#_____________________________________________________________________________________________________________
def drawStack(name, ylabel, legend, leftText, rightText, formats, directory, logY, stacksig, histos, colors, ana_tex, extralab, nsig, nbkg, legend2=None):

    canvas = ROOT.TCanvas(name, name, 600, 600) 
    canvas.SetLogy(logY)
    canvas.SetTicks(1,1)
    canvas.SetLeftMargin(0.1)
    canvas.SetRightMargin(0.1)
 

    # first retrieve maximum 
    sumhistos = histos[0].Clone()
    iterh = iter(histos)
    next(iterh)


    try:
        histos[1]
    except IndexError:
        histos1_exists = False
    else:
        histos1_exists = True

    xlabel = histos[0].GetXaxis().GetTitle()
    unitBeginIndex = xlabel.find(" [")
    unitEndIndex = xlabel.endswith("]")
    width = str(histos[0].GetXaxis().GetBinWidth(1))

    if unitBeginIndex is not -1 and unitEndIndex is not -1: #x axis has a unit
        ylabel += " / " + width + " " + xlabel[unitBeginIndex+2:-1]
    else:
        ylabel += " per bin (" + width + " width)"

        
    for h in iterh:
      sumhistos.Add(h)

    maxh = sumhistos.GetMaximum()
    minh = sumhistos.GetMinimum()

    if logY: 
       canvas.SetLogy(1)

    # define stacked histo
    hStack    = ROOT.THStack("hstack","")
    hStackBkg = ROOT.THStack("hstackbkg","")
    BgMCHistYieldsDic = {}

    # first plot backgrounds
    if(nbkg>0):
        histos[nsig].SetLineWidth(0)
        histos[nsig].SetLineColor(ROOT.kBlack)
        histos[nsig].SetFillColor(colors[nsig])

        #put histograms in a dictionary according to their yields
        if histos[nsig].Integral()>0:
            BgMCHistYieldsDic[histos[nsig].Integral()] = histos[nsig]
        # for empty histograms, put them as having negative yields (so multiple ones don't overwrite each other in the dictionary)
        else:
            BgMCHistYieldsDic[-1*nbkg] = histos[nsig]
    
        # now loop over other background (skipping first)
        iterh = iter(histos)
        for i in range(nsig):
            next(iterh)
        next(iterh)
    
        k = nsig+1
        for h in iterh:
            h.SetLineWidth(0)
            h.SetLineColor(ROOT.kBlack)
            h.SetFillColor(colors[k])
            if h.Integral()>0:
                BgMCHistYieldsDic[h.Integral()] = h
            else:
                BgMCHistYieldsDic[-1*nbkg] = h
            k += 1

        # sort stack by yields (smallest to largest)
        BgMCHistYieldsDic = sortedDictValues(BgMCHistYieldsDic)
        for h in BgMCHistYieldsDic:
            hStack.Add(h)
            hStackBkg.Add(h)

        if not stacksig:
            hStack.Draw("hist")

    # define stacked signal histo
    hStackSig = ROOT.THStack("hstacksig","")

    # finally add signal on top
    for l in range(nsig):
        histos[l].SetLineWidth(3)
        histos[l].SetLineColor(colors[l])
        if stacksig:
            hStack.Add(histos[l])
        else:
            hStackSig.Add(histos[l])

    if stacksig:
        hStack.Draw("hist")

    if (not stacksig) and nbkg==0:
        hStackSig.Draw("hist nostack")
        hStackSig.GetXaxis().SetTitle(xlabel)
        hStackSig.GetYaxis().SetTitle(ylabel)

        hStackSig.GetYaxis().SetTitleOffset(1.45)
        hStackSig.GetXaxis().SetTitleOffset(1.3)
    else:
        hStack.GetXaxis().SetTitle(xlabel)
        hStack.GetYaxis().SetTitle(ylabel)

        hStack.GetYaxis().SetTitleOffset(1.45)
        hStack.GetXaxis().SetTitleOffset(1.3)

    lowY=0.
    if logY:
        highY=200.*maxh/ROOT.gPad.GetUymax()
        threshold=0.5
        if (not stacksig) and nbkg==0:
            bin_width=hStackSig.GetXaxis().GetBinWidth(1)
        else:
            bin_width=hStack.GetXaxis().GetBinWidth(1)
        lowY=threshold*bin_width
        if (not stacksig) and nbkg==0:
            #hStackSig.SetMaximum(highY)
            #hStackSig.SetMinimum(lowY)
            # hStackSig.SetMaximum(100)      # plots normalized to 1
            # hStackSig.SetMinimum(0.00001)
            #hStackSig.SetMaximum(3000)      # plots normalized to 1
            #hStackSig.SetMinimum(0.001)
            hStackSig.SetMaximum(1e30)     # background plots normalized with cross-section and integrated luminosity
            #hStackSig.SetMinimum(1e5)
            # hStackSig.SetMaximum(1e8)      # signal plots normalized with cross-section and integrated luminosity
            hStackSig.SetMinimum(1e-4)
            #hStackSig.SetMaximum(1e9)      # background plots with unweighted events (100 000 total events)
            #hStackSig.SetMinimum(0)
            #hStackSig.SetMaximum(1e7)      # signal plots with unweighted events (50 000 total events)
            #hStackSig.SetMinimum(1)
            #hStackSig.SetMaximum(1e25)
        else:
            #hStack.SetMaximum(highY)
            #hStack.SetMinimum(lowY)
            #hStack.SetMaximum(100)      # plots normalized to 1
            #hStack.SetMinimum(0.00001)
            hStack.SetMaximum(1e30)     # background plots normalized with cross-section and integrated luminosity
            #hStack.SetMinimum(1e5)
            # hStack.SetMaximum(1e8)      # signal plots normalized with cross-section and integrated luminosity
            hStack.SetMinimum(1e-4)
            #hStack.SetMaximum(1e9)      # background plots with unweighted events (100 000 total events)
            #hStack.SetMinimum(0)
            #hStack.SetMaximum(1e7)      # signal plots with unweighted events (50 000 total events)
            #hStack.SetMinimum(1)
            #hStack.SetMaximum(1e25)

    else:
        if (not stacksig) and nbkg==0:
            hStackSig.SetMaximum(1.5*maxh)
            # hStackSig.SetMaximum(0.5)
            hStackSig.SetMinimum(0.)
        else:
            hStack.SetMaximum(1.5*maxh)
            # hStack.SetMaximum(0.5)
            hStack.SetMinimum(0.)

    if(nbkg>0):
        escape_scale_Xaxis=True
        hStacklast = hStack.GetStack().Last()
        lowX_is0=True
        lowX=hStacklast.GetBinCenter(1)-(hStacklast.GetBinWidth(1)/2.)
        highX_ismax=False
        highX=hStacklast.GetBinCenter(hStacklast.GetNbinsX())+(hStacklast.GetBinWidth(1)/2.)

        if escape_scale_Xaxis==False:
            for i_bin in range( 1, hStacklast.GetNbinsX()+1 ):
                bkg_val=hStacklast.GetBinContent(i_bin)
                sig_val=histos[0].GetBinContent(i_bin)
                if bkg_val/maxh>0.1 and i_bin<15 and lowX_is0==True:
                    lowX_is0=False
                    lowX=hStacklast.GetBinCenter(i_bin)-(hStacklast.GetBinWidth(i_bin)/2.)

            val_to_compare=bkg_val
            if sig_val>bkg_val : val_to_compare=sig_val
            if val_to_compare<lowY and i_bin>15 and highX_ismax==False:
                highX_ismax=True
                highX=hStacklast.GetBinCenter(i_bin)+(hStacklast.GetBinWidth(i_bin)/2.)
                highX*=1.1
            # protections
            if lowX<hStacklast.GetBinCenter(1)-(hStacklast.GetBinWidth(1)/2.) :
                lowX=hStacklast.GetBinCenter(1)-(hStacklast.GetBinWidth(1)/2.)
            if highX>hStacklast.GetBinCenter(hStacklast.GetNbinsX())+(hStacklast.GetBinWidth(1)/2.) :
                highX=hStacklast.GetBinCenter(hStacklast.GetNbinsX())+(hStacklast.GetBinWidth(1)/2.)
            if lowX>=highX :
                lowX=hStacklast.GetBinCenter(1)-(hStacklast.GetBinWidth(1)/2.)
                highX=hStacklast.GetBinCenter(hStacklast.GetNbinsX())+(hStacklast.GetBinWidth(1)/2.)
            hStack.GetXaxis().SetLimits(int(lowX),int(highX))

    if not stacksig:
        if nbkg>0:
            hStackSig.Draw("same hist nostack")
        else:
            hStackSig.Draw("hist nostack")

    legend.Draw()
    if legend2 != None:
        legend2.Draw()
    
    pave = ROOT.TPaveText(0.63,0.38,0.88,0.68,"ndc") #7 entries
    #pave = ROOT.TPaveText(0.63,0.42,0.88,0.68,"ndc") #6 entries
    #pave = ROOT.TPaveText(0.63,0.46,0.88,0.68,"ndc") #5 entries
    #pave = ROOT.TPaveText(0.63,0.5,0.88,0.68,"ndc") #4 entries
    #pave = ROOT.TPaveText(0.63,0.54,0.88,0.68,"ndc") #3 entries
    #pave = ROOT.TPaveText(0.63,0.46,0.88,0.68,"ndc") #5 entries
    #pave = ROOT.TPaveText(0.63,0.5,0.88,0.68,"ndc") #4 entries
    #pave = ROOT.TPaveText(0.63,0.54,0.88,0.68,"ndc") #3 entries
    pave.SetFillColor(0)
    pave.SetBorderSize(0)

    mean = []
    stdDev = []
    for m,s in zip(mean, stdDev):
        #print(", mean = "+str(m)+", s.d. = "+str(s))
        pave.AddText(", mean = {:.1e}, s.d. = {:.1e}".format(m,s))
    #pave.Draw()
    
    Text = ROOT.TLatex()
    
    Text.SetNDC()
    Text.SetTextAlign(31)
    Text.SetTextSize(0.04)

    text = '#it{' + leftText +'}'
    
    Text.DrawLatex(0.90, 0.92, text)

    rightText = re.split(",", rightText)
    text = '#bf{#it{' + rightText[0] +'}}'
    #text = '#bf{#it{' + rightText +'}}' #use if scaleSig==1
    
    Text.SetTextAlign(12)
    Text.SetNDC(ROOT.kTRUE)
    Text.SetTextSize(0.04)
    Text.DrawLatex(0.18, 0.83, text)

    rightText[1]=rightText[1].replace("   ","")
    text = '#bf{#it{' + rightText[1] +'}}'
    Text.SetTextSize(0.035)
    Text.DrawLatex(0.18, 0.78, text)

    text = '#bf{#it{' + ana_tex +'}}'
    Text.SetTextSize(0.04)
    Text.DrawLatex(0.18, 0.73, text)

    text = '#bf{#it{' + extralab +'}}'
    Text.SetTextSize(0.025)
    Text.DrawLatex(0.18, 0.68, text)
    
    canvas.RedrawAxis()
    #canvas.Update()
    canvas.GetFrame().SetBorderSize( 12 )
    canvas.Modified()
    canvas.Update()

    printCanvas(canvas, name, formats, directory)




#_____________________________________________________________________________________________________________
def drawEffPlots(name, ylabel, legend, leftText, rightText, formats, directory, logY, stacksig, histos, colors, ana_tex, extralab):

    canvas = ROOT.TCanvas(name, name, 600, 600)
    canvas.SetLogy(logY)
    canvas.SetTicks(1,1)
    canvas.SetLeftMargin(0.1)
    canvas.SetRightMargin(0.1)

    # first retrieve maximum
    sumhistos = histos[0].Clone()
    iterh = iter(histos)
    next(iterh)

    try:
        histos[1]
    except IndexError:
        histos1_exists = False
    else:
        histos1_exists = True

    for h in iterh:
      sumhistos.Add(h)

    maxh = 2.3

    if logY:
       canvas.SetLogy(1)

    k = 0
    for h in histos:
       h.SetLineWidth(3)
       h.SetLineColor(colors[k])
       k += 1


    # fix names if needed
    if(histos1_exists):
        #xlabel = histos[1].GetXaxis().GetTitle()
        xlabel = "Electron p [GeV]"

        #histos[0].GetXaxis().SetTitleFont(font)
        #histos[0].GetXaxis().SetLabelFont(font)
        histos[0].GetXaxis().SetTitle(xlabel)
        histos[0].GetYaxis().SetTitle(ylabel)
        #histos[0].GetYaxis().SetTitleFont(font)
        #histos[0].GetYaxis().SetLabelFont(font)
        '''histos[0].GetXaxis().SetTitleOffset(1.3)
        histos[0].GetYaxis().SetTitleOffset(1.3)
        histos[0].GetXaxis().SetLabelOffset(0.02)
        histos[0].GetYaxis().SetLabelOffset(0.02)
        histos[0].GetXaxis().SetTitleSize(0.06)
        histos[0].GetYaxis().SetTitleSize(0.06)
        histos[0].GetXaxis().SetLabelSize(0.06)
        histos[0].GetYaxis().SetLabelSize(0.06)
        histos[0].GetXaxis().SetNdivisions(505);
        histos[0].GetYaxis().SetNdivisions(505);
        histos[0].SetTitle("") '''

        histos[0].GetYaxis().SetTitleOffset(1.45)
        histos[0].GetXaxis().SetTitleOffset(1.3)


        #hStack.SetMaximum(1.5*maxh)

        #if logY:
        #    histos[0].SetMaximum(3)
        #    histos[0].SetMinimum(0.00001)
        #else:
    histos[0].SetMaximum(maxh)
    histos[0].SetMinimum(0.)

    escape_scale_Xaxis=True

    #if not stacksig:
        #if logY:
        #    maxh=200.*maxh/ROOT.gPad.GetUymax()
        #    histos[0].SetMaximum(5000)
        #else:
        #    histos[0].SetMaximum(2.3*maxh)         
    histos[0].Draw("e")
    for h in histos:
        if h!=histos[0]:
            h.Draw("esame")

    #legend.SetTextFont(font)
    legend.Draw()

    Text = ROOT.TLatex()

    Text.SetNDC()
    Text.SetTextAlign(31)
    Text.SetTextSize(0.04)

    text = '#it{' + leftText +'}'

    Text.DrawLatex(0.90, 0.92, text)

    rightText = re.split(",", rightText)
    text = '#bf{#it{' + rightText[0] +'}}'

    Text.SetTextAlign(12)
    Text.SetNDC(ROOT.kTRUE)
    Text.SetTextSize(0.04)
    Text.DrawLatex(0.18, 0.83, text)

    rightText[1]=rightText[1].replace("   ","")
    text = '#bf{#it{' + rightText[1] +'}}'
    Text.SetTextSize(0.035)
    Text.DrawLatex(0.18, 0.78, text)

    text = '#bf{#it{' + ana_tex +'}}'
    Text.SetTextSize(0.04)
    Text.DrawLatex(0.18, 0.73, text)

    text = '#bf{#it{' + extralab +'}}'
    Text.SetTextSize(0.025)
    Text.DrawLatex(0.18, 0.68, text)

    canvas.RedrawAxis()
    canvas.GetFrame().SetBorderSize( 12 )
    canvas.Modified()
    canvas.Update()

    printCanvas(canvas, name, formats, directory)

    


#____________________________________________________
def printCanvas(canvas, name, formats, directory):

    if format != "":
        if not os.path.exists(directory) :
                os.system("mkdir -p "+directory)
        for f in formats:
            outFile = os.path.join(directory, name) + "." + f
            canvas.SaveAs(outFile)



#__________________________________________________________
if __name__=="__main__":
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    ROOT.gStyle.SetOptStat(0)
    # param file
    paramFile = sys.argv[1]

    module_path = os.path.abspath(paramFile)
    module_dir = os.path.dirname(module_path)
    base_name = os.path.splitext(ntpath.basename(paramFile))[0]

    sys.path.insert(0, module_dir)
    param = importlib.import_module(base_name)
        

    for var in param.variables:
        for label, sels in param.selections.items():
            for sel in sels:
                hsignal,hbackgrounds=mapHistos(var,label,sel, param)
                runPlots(var+"_"+label+"_"+sel,param,hsignal,hbackgrounds,param.extralabel[sel],param.splitLeg)
                if var in param.effPlots.keys():
                    print("variable in effPlots.keys() is: "+var+", value is then: "+param.effPlots.get(var))
                    effsignal,effbackgrounds=mapEffHistos(param.effPlots.get(var),var,label,sel, param)
                    runEffPlots(param.effPlots.get(var),var+"_"+label+"_"+sel,param,effsignal,effbackgrounds,param.extralabel[sel])

