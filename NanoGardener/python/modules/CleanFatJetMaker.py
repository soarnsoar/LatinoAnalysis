import ROOT
import os
import re
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from LatinoAnalysis.NanoGardener.data.CleanFatJetMaker_cfg import CleanFatJet_br, CleanFatJet_var
from LatinoAnalysis.NanoGardener.data.common_cfg import Type_dict

class CleanFatJetMaker(Module):
    '''                                                                                                                        
    put this file in LatinoAnalysis/NanoGardener/python/modules/                                                               
    Add extra variables to NANO tree                                                                                           
    '''
    def __init__(self):
        
        print('CleanFatJetMaker:')

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.initReaders(inputTree) # initReaders must be called in beginFile                                                  
        self.out = wrappedOutputTree

        # New branches                                                                                                         
        
        for typ in CleanFatJet_br:
           for var in CleanFatJet_br[typ]:
              if 'CleanFatJet_' in var: self.out.branch(var, typ, lenVar='nCleanFatJet')
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class                                                                                                                            
       
       self.fatjet_var = {}
       for br in tree.GetListOfBranches():
           bname = br.GetName()
           if re.match('\AFatJet_', bname):       self.fatjet_var[bname] = tree.arrayReader(bname)

       self.nFatJet = tree.valueReader('nFatJet')
       self._ttreereaderversion = tree._ttreereaderversion # self._ttreereaderversion must be set AFTER all calls to tree.valueReader or tree.arrayReader

    def analyze(self, event):
       """process event, return True (go to next module) or False (fail, go to next event)"""

       if event._tree._ttreereaderversion > self._ttreereaderversion: # do this check at every event, as other modules might have read further branches
           self.initReaders(event._tree)
       # do NOT access other branches in python between the check/call to initReaders and the call to C++ worker code         
               
       #--- Set vars                                                                                                          
       nFJt = int(self.nFatJet)
       fatjet_dict = {}
       for jv in CleanFatJet_var:
           fatjet_dict[jv] = [0]*nFJt # [ 0 0 0 0 0 0 0 ... 0] nFJt zeros
       fatjet_dict['fatjetIdx'] = [0]*nFJt
       
       
       #--- FatJet Loops                                                                                                         
       for iFJ1 in range(nFJt):
           pt_idx = 0 ##new idx by pt
           pt1 = self.fatjet_var['FatJet_pt'][iFJ1]
           # Start comparing jets                                                                                              
           for iFJ2 in range(nFJt):
               if iFJ2 == iFJ1: continue #same fatjet. 
               pt2 = self.fatjet_var['Jet_pt'][iFJ2]
               if pt1 < pt2 or (pt1==pt2 and iFJ1>iFJ2): ##pt ordering. if the same pt -> ordering by original idx
                   pt_idx += 1
           # Now index is set, fill the vars                                                                                   
           for var in fatjet_dict:
               if not 'Idx' in var:
                   fatjet_dict[var][pt_idx] = self.fatjet_var['FatJet_' + var][iFJ1]
               else:
                   fatjet_dict[var][pt_idx] = iFJ1 ## save original index
       #--- Fill branches                                                                                                     
                   
       for var in fatjet_dict:
           self.out.fillBranch( 'CleanFatJet_' + var, fatjet_dict[var])
           
       return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed                    

cleanfatjetMkr = lambda : CleanFatJetMaker()
