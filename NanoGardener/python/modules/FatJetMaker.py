import ROOT
import os
import re
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from LatinoAnalysis.NanoGardener.data.FatJetMaker_cfg import FatJet_br, FatJet_var
from LatinoAnalysis.NanoGardener.data.common_cfg import Type_dict

#--jhchoi 2019.April.23rd
##.Based on LeptonMaker##
##.Take FatJet(AK8) Object in raw NanoAOD
##. W FatJet selection criteria  https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetWtagging
##.NanoAODv4 document https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html#FatJet
##.FatJet selection for 2016 analysis : 
#(1)pt >200 GeV, |eta| < 2.4
#(2)PUPPI softdrop mass m_J > 40 GeV
#(3) tau21 < 0.4
#Variables to store :
# FatJet momentum : FatJet_mass, FatJet_pt, FatJet_eta, FatJet_phi, FatJet_msoftdrop
# Jet Id : FatJet_jetId
# raw factor : FatJet_rawFactor
# Nsubjettiness : FatJet_tau1, FatJet_tau2
# jet area : FatJet_area
# nFatJet : nFatJet


class FatJetMaker(Module): 
    '''
    put this file in LatinoAnalysis/NanoGardener/python/modules/
    Add extra variables to NANO tree
    '''
    def __init__(self, min_fatjet_pt = [180]): ##For test, pt cut = 180. Actaul pt cut ==200 GeV
        self.min_fatjet_pt = min_fatjet_pt
        self.min_fatjet_pt_idx = range(len(min_fajet_pt))
        print_str = ''
        for idx in self.min_fatjet_pt_idx:
            print_str += 'FatJet_pt[' + str(idx) + '] > ' + str(min_fatjet_pt[idx])
            if not idx == self.min_fatjet_pt_idx[-1]: print_str += ', '
        print('FatJetMaker: ' + print_str)

    def beginJob(self): 
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.initReaders(inputTree) # initReaders must be called in beginFile
        self.out = wrappedOutputTree

        # New branches
        for typ in FatJet_br:
           for var in FatJet_br[typ]:
              if 'FatJet_' in var: self.out.branch(var, typ, lenVar='nFatJet')


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class
        
        self.fatjet_var = {}
        for br in tree.GetListOfBranches():
           bname = br.GetName()
           
           if re.match('\AFatJet_', bname):       self.fatjet_var[bname] = tree.arrayReader(bname) ##read NanoAOD variables

        
        self.nFatJet = tree.valueReader('nFatJet')
        self._ttreereaderversion = tree._ttreereaderversion # self._ttreereaderversion must be set AFTER all calls to tree.valueReader or tree.arrayReader

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if event._tree._ttreereaderversion > self._ttreereaderversion: # do this check at every event, as other modules might have read further branches
            self.initReaders(event._tree)
        # do NOT access other branches in python between the check/call to initReaders and the call to C++ worker code
        
        #--- Set vars
        
        nFatJet = int(self.nFatJet)
        

        if nFatJet < len(self.min_fatjet_pt): return False ##If nFatJet < # of pt cuts e.g.) 1jet event with primary/second jets' ptcut ->False

        fatjet_dict = {} ##What to save to Latino Tree
        for fjv in FatJet_var: ##from FatJet cfg  file ==> What to save
           fatjet_dict[fjv] = [0]*nFatJet ##Make list with nFatJet elements whose value = 0 ##initialize[0,0,0,...0]
        fatjet_dict['fatjetIdx'] = [0]*nFatJet #Index
        
        #--- Fatjet Loops
        for iFatJet1 in range(nFatJet):
           pt_idx = 0
           pt1 = self.fatjet_var['FatJet_pt'][iFatJet1]
           # Start comparing FatJets
           for iFatJet2 in range(nFatJet):
              if iFatJet2 == iFatJet1: continue
              pt2 = self.fatjet_var['FatJet_pt'][iFatJet2]
              if pt1 < pt2 or (pt1==pt2 and iFatJet1>iFatJet2):
                 pt_idx += 1 ##for FatJet1, count # of other FatJets whose pt > FatJet1_pt #if pt are the same, follow original index order
                

           # Now index is set, fill the vars  
           
           for var in fatjet_dict:
               if not 'Idx' in var :
                   fatjet_dict[var][pt_idx] = self.fatjet_var['FatJet_'+var][iFatJet1]
               
               else:
                   fatjet_dict[var][pt_idx] = iFatJet1


        #--- Fill branches
        for var in fatjet_dict:
           self.out.fillBranch( 'FatJet_' + var, fatjet_dict[var])

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

fatjetMkr = lambda : FatJetMaker()
