#
#
#
#   \ \        / \ \        /       \  |  |      |
#    \ \  \   /   \ \  \   /         \ |  |      |
#     \ \  \ /     \ \  \ /        |\  |  |      |
#      \_/\_/       \_/\_/        _| \_| _____| _____|
#
#
#
#


from LatinoAnalysis.Gardener.gardening import TreeCloner
import numpy
import ROOT
import sys
import optparse
import re
import warnings
import os.path
from array import array;

class wwNLLcorrectionWeightFiller(TreeCloner):
    def __init__(self):
       pass

    def help(self):
        return '''Add weight for WW NLL reweighting'''

    def addOptions(self,parser):
        description = self.help()
        group = optparse.OptionGroup(parser,self.label, description)
        group.add_option('-m', '--mcsample' , dest='mcsample', help='Name of the mc sample to be considered. Possible options [powheg, mcatnlo, madgraph]',default='random')
        group.add_option('-c', '--cmssw'    , dest='cmssw', help='cmssw version (naming convention may change)', default='764', type='string')
        parser.add_option_group(group)

        return group


    def checkOptions(self,opts):
        if (
             not hasattr(opts,'mcsample')      ) :
            raise RuntimeError('Missing parameter')

        self.mcsample = opts.mcsample

        self.cmssw = opts.cmssw
        print " cmssw =", self.cmssw


    def process(self,**kwargs):

        # change this part into correct path structure... 
        cmssw_base = os.getenv('CMSSW_BASE')
        try:
            ROOT.gROOT.LoadMacro(cmssw_base+'/src/LatinoAnalysis/Gardener/python/variables/wwNLLcorrectionWeight.C+')
        except RuntimeError:
            ROOT.gROOT.LoadMacro(cmssw_base+'/src/LatinoAnalysis/Gardener/python/variables/wwNLLcorrectionWeight.C++')
        #----------------------------------------------------------------------------------------------------

        #wwNLL = ROOT.wwNLL(self.mcsample, 
                           #cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/central.dat',
                           #cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/resum_up.dat',  #
                           #cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/resum_down.dat',  #
                           #cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/scale_up.dat',    #
                           #cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/scale_down.dat',  #
                           #cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/nnlo_central.dat',   
                           #cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/powheg_2l2nu_nlo.dat',
                           #cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/powheg_2l2nu_qup_nlo.dat',
                           #cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/powheg_2l2nu_qdown_nlo.dat',
                           #cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/powheg_2l2nu_sup_nlo.dat',
                           #cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/powheg_2l2nu_sdown_nlo.dat',
                           #cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/powheg_2l2nu_nnlo.dat'
                           #)

        wwNLL = ROOT.wwNLL(
                           cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/central.dat',
                           cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/resum_up.dat',  
                           cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/resum_down.dat',
                           cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/scale_up.dat', 
                           cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/wwresum/scale_down.dat'
                           )

        print " starting ..."

        tree  = kwargs['tree']
        input = kwargs['input']
        output = kwargs['output']

        # does that work so easily and give new variable itree and otree?
        self.connect(tree,input)
        newbranches = ['nllnnloW', 'nllW', 'nllW_Rup', 'nllW_Qup', 'nllW_Rdown', 'nllW_Qdown', 'gen_mww', 'gen_ptww']
        self.clone(output,newbranches)


        nllnnloW    = numpy.ones(1, dtype=numpy.float32)
        nllW        = numpy.ones(1, dtype=numpy.float32)
        nllW_Rup    = numpy.ones(1, dtype=numpy.float32)
        nllW_Qup    = numpy.ones(1, dtype=numpy.float32)
        nllW_Rdown  = numpy.ones(1, dtype=numpy.float32)
        nllW_Qdown  = numpy.ones(1, dtype=numpy.float32)
        gen_mww     = numpy.ones(1, dtype=numpy.float32)
        gen_ptww    = numpy.ones(1, dtype=numpy.float32)

        self.otree.Branch('nllnnloW'  , nllnnloW  , 'nllnnloW/F')
        self.otree.Branch('nllW'  , nllW  , 'nllW/F')
        self.otree.Branch('nllW_Rup'  , nllW_Rup  , 'nllW_Rup/F')
        self.otree.Branch('nllW_Qup'  , nllW_Qup  , 'nllW_Qup/F')
        self.otree.Branch('nllW_Rdown'  , nllW_Rdown  , 'nllW_Rdown/F')
        self.otree.Branch('nllW_Qdown'  , nllW_Qdown  , 'nllW_Qdown/F')
        self.otree.Branch('gen_mww'  , gen_mww   , 'gen_mww/F')
        self.otree.Branch('gen_ptww' , gen_ptww  , 'gen_ptww/F')

        nentries = self.itree.GetEntries()
        print 'Total number of entries: ',nentries 

        #what is self.itree? what is self.otree?
        itree     = self.itree
        otree     = self.otree

        print '- Starting eventloop'
        step = 5000

        for i in xrange(nentries):
        #for i in xrange(100):

            itree.GetEntry(i)

            if i > 0 and i%step == 0.:
                print i,'events processed.'

            number1 = -1
            number2 = -1
            
            #print "--------"
            #print " size = ", itree.std_vector_VBoson_pt.size()
            #print " self.cmssw  = ", self.cmssw 
            
            if self.cmssw == '74x' :


             # 74X release, 21st Oct tag

              for numlepton in range(0, itree.std_vector_VBoson_pt.size()):
                #print " - ", numlepton, " :: ", itree.std_vector_VBoson_fromHardProcessBeforeFSR.at(numlepton), " :: ", abs(itree.std_vector_VBoson_pid.at(numlepton))
                if itree.std_vector_VBoson_fromHardProcessBeforeFSR.at(numlepton) == 1 and abs(itree.std_vector_VBoson_pid.at(numlepton)) == 24 :
                  if number1 == -1 :
                    number1 = numlepton
                  else :
                    number2 = numlepton

              #print "     number1 = ",  number1           
              #print "     number2 = ",  number2

              if number1 != -1 and number2 != -1 :
                ptV1 = itree.std_vector_VBoson_pt.at(number1)
                ptV2 = itree.std_vector_VBoson_pt.at(number2)
                phiV1 = itree.std_vector_VBoson_phi.at(number1)
                phiV2 = itree.std_vector_VBoson_phi.at(number2)
                etaV1 = itree.std_vector_VBoson_eta.at(number1)
                etaV2 = itree.std_vector_VBoson_eta.at(number2)

                wwNLL.SetPTWW(ptV1, phiV1, etaV1, ptV2, phiV2, etaV2)

                gen_ptww[0]  = wwNLL.GetPTWW()
                gen_mww[0]   = wwNLL.GetMWW()

              else :
                gen_mww[0]  = -9999.
                gen_ptww[0] = -9999.
 
            else:

              if itree.std_vector_VBoson_pt.size() >= 2 :
                number1 = 0
                number2 = 1
              
              #print "     number1 = ",  number1           
              #print "     number2 = ",  number2
      
              if number1 != -1 and number2 != -1 : 
                ptV1 = itree.std_vector_VBoson_pt.at(number1)
                ptV2 = itree.std_vector_VBoson_pt.at(number2)
                phiV1 = itree.std_vector_VBoson_phi.at(number1)
                phiV2 = itree.std_vector_VBoson_phi.at(number2)
                etaV1 = itree.std_vector_VBoson_eta.at(number1)
                etaV2 = itree.std_vector_VBoson_eta.at(number2)
      
                wwNLL.SetPTWW(ptV1, phiV1, etaV1, ptV2, phiV2, etaV2)
                
                gen_ptww[0]  = wwNLL.GetPTWW()
                gen_mww[0]   = wwNLL.GetMWW()
                
              else :
                gen_mww[0]  = -9999.
                gen_ptww[0] = -9999.
                                
                






             

            nllnnloW[0] = wwNLL.nllnnloWeight(0)
            nllW[0]   = wwNLL.nllWeight(0)
            nllW_Rup[0]   = wwNLL.nllWeight(1,1)
            nllW_Qup[0]   = wwNLL.nllWeight(1,0)
            nllW_Rdown[0] = wwNLL.nllWeight(-1,1)
            nllW_Qdown[0] = wwNLL.nllWeight(-1,0)

            otree.Fill()

        self.disconnect()
        print '- Eventloop completed'



