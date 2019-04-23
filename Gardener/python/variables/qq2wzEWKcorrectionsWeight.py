from LatinoAnalysis.Gardener.gardening import TreeCloner
import numpy
import ROOT
import sys
import optparse
import re
import warnings
import os.path
from array import array;

class qq2wzEWKcorrectionsWeightFiller(TreeCloner):
    def __init__(self):
       pass

    def help(self):
        return '''Add weight to cope with electroweak corrections'''

    def addOptions(self,parser):
        pass

    def checkOptions(self,opts):
        pass

    def process(self,**kwargs):
        tree  = kwargs['tree']
        input = kwargs['input']
        output = kwargs['output']

        self.connect(tree,input)
        newbranches = ['ewkWZ', 'ewkWZuncertainty']
        self.clone(output,newbranches)

        ewkWZ    = numpy.ones(1, dtype=numpy.float32)
        ewkWZuncertainty    = numpy.ones(1, dtype=numpy.float32)
        self.otree.Branch('ewkWZ'  ,            ewkWZ  ,            'ewkWZ/F')
        self.otree.Branch('ewkWZuncertainty'  , ewkWZuncertainty  , 'ewkWZuncertainty/F')

        nentries = self.itree.GetEntries()
        print 'Total number of entries: ',nentries

        itree     = self.itree
        otree     = self.otree

        cmssw_base = os.getenv('CMSSW_BASE')
        try:
            ROOT.gROOT.LoadMacro(cmssw_base+'/src/LatinoAnalysis/Gardener/python/variables/qq2wvEWKcorrectionsWeight.C')
        except RuntimeError:
            ROOT.gROOT.LoadMacro(cmssw_base+'/src/LatinoAnalysis/Gardener/python/variables/qq2wvEWKcorrectionsWeight.C++g')
        #----------------------------------------------------------------------------------------------------

        qq2wvEWKcorrections = ROOT.qq2wvEWKcorrections(cmssw_base+'/src/LatinoAnalysis/Gardener/python/data/ewk/WZ_EwkCorrections.dat')

        print '- Starting eventloop'
        step = 5000
        for i in xrange(nentries):
            itree.GetEntry(i)

            if i > 0 and i%step == 0.:
                print i,'events processed.'

            temp_ptl1 = itree.std_vector_LHElepton_pt[0]
            temp_etal1 = itree.std_vector_LHElepton_eta[0]
            temp_phil1 = itree.std_vector_LHElepton_phi[0]
            temp_idl1 = itree.std_vector_LHElepton_id[0]
            
            temp_ptl2 = itree.std_vector_LHElepton_pt[1]
            temp_etal2 = itree.std_vector_LHElepton_eta[1]
            temp_phil2 = itree.std_vector_LHElepton_phi[1]
            temp_idl2 = itree.std_vector_LHElepton_id[1]

            temp_ptl3 = itree.std_vector_LHElepton_pt[2]
            temp_etal3 = itree.std_vector_LHElepton_eta[2]
            temp_phil3 = itree.std_vector_LHElepton_phi[2]
            temp_idl3 = itree.std_vector_LHElepton_id[2]


            temp_ptv1 = itree.std_vector_LHEneutrino_pt[0]
            temp_etav1 = itree.std_vector_LHEneutrino_eta[0]
            temp_phiv1 = itree.std_vector_LHEneutrino_phi[0]
            temp_idv1  = itree.std_vector_LHEneutrino_id[0]
            
            temp_ptv2 = itree.std_vector_LHEneutrino_pt[1]
            temp_etav2 = itree.std_vector_LHEneutrino_eta[1]
            temp_phiv2 = itree.std_vector_LHEneutrino_phi[1]
            temp_idv2  = itree.std_vector_LHEneutrino_id[1]
                  
            temp_ptv3 = itree.std_vector_LHEneutrino_pt[2]
            temp_etav3 = itree.std_vector_LHEneutrino_eta[2]
            temp_phiv3 = itree.std_vector_LHEneutrino_phi[2]
            temp_idv3  = itree.std_vector_LHEneutrino_id[2]



            temp_ptq1 = itree.std_vector_LHEparton_pt[0]
            temp_etaq1 = itree.std_vector_LHEparton_eta[0]
            temp_phiq1 = itree.std_vector_LHEparton_phi[0]
            temp_idq1  = itree.std_vector_LHEparton_id[0]
            
            temp_ptq2 = itree.std_vector_LHEparton_pt[1]
            temp_etaq2 = itree.std_vector_LHEparton_eta[1]
            temp_phiq2 = itree.std_vector_LHEparton_phi[1]
            temp_idq2  = itree.std_vector_LHEparton_id[1]
                  
                  
 
            x1 = itree.pdfx1
            x2 = itree.pdfx2

            id1 = itree.pdfid1
            id2 = itree.pdfid2


            ptl1  = 0.
            etal1 = 0.
            phil1 = 0.
            idl1  = 0.
            
            ptl2  = 0.
            etal2 = 0.
            phil2 = 0.
            idl2  = 0.

            ptv1   = 0
            etav1  = 0
            phiv1  = 0
            idv1   = 0.
            
            ptv2   = 0.
            etav2  = 0.
            phiv2  = 0.
            idv2   = 0.


            # 1 should be the W
            # 2 should be the Z
            
            if temp_ptv2 > 0 :
              # W>lv  and   Z>vv
              ptl1  = temp_ptl1
              etal1 = temp_etal1
              phil1 = temp_phil1
              idl1  = temp_idl1
              
              if (abs(temp_idv1) == (abs(idl1)+1)) :
                    
                ptv1  = temp_ptv1
                etav1 = temp_etav1
                phiv1 = temp_phiv1
                idv1  = temp_idv1
               
                ptl2  = temp_ptv2
                etal2 = temp_etav2
                phil2 = temp_phiv2
                idl2  = temp_idv2
               
                ptv2  = temp_ptv3
                etav2 = temp_etav3
                phiv2 = temp_phiv3
                idv2  = temp_idv3    
             
              elif (abs(temp_idv2) == (abs(idl1)+1)) :
                      
                ptv1  = temp_ptv2
                etav1 = temp_etav2
                phiv1 = temp_phiv2
                idv1  = temp_idv2
               
                ptl2  = temp_ptv1
                etal2 = temp_etav1
                phil2 = temp_phiv1
                idl2  = temp_idv1
               
                ptv2  = temp_ptv3
                etav2 = temp_etav3
                phiv2 = temp_phiv3
                idv2  = temp_idv3    
             
              elif (abs(temp_idv3) == (abs(idl1)+1)) :
                      
                ptv1  = temp_ptv3
                etav1 = temp_etav3
                phiv1 = temp_phiv3
                idv1  = temp_idv3
               
                ptl2  = temp_ptv1
                etal2 = temp_etav1
                phil2 = temp_phiv1
                idl2  = temp_idv1
               
                ptv2  = temp_ptv2
                etav2 = temp_etav2
                phiv2 = temp_phiv2
                idv2  = temp_idv2   
             
                      
            elif temp_ptq1 > 0 :

              # W>qq  and   Z>ll

              ptl1  = temp_ptq1
              etal1 = temp_etaq1
              phil1 = temp_phiq1
              idl1  = temp_idq1
              
              ptv1  = temp_ptq2
              etav1 = temp_etaq2
              phiv1 = temp_phiq2
              idv1  = temp_idq2
              
              ptl2  = temp_ptl1
              etal2 = temp_etal1
              phil2 = temp_phil1
              idl2  = temp_idl1
             
              ptv2  = temp_ptl2
              etav2 = temp_etal2
              phiv2 = temp_phil2
              idv2  = temp_idl2   

              
            else :
              # W>lv  and   Z>ll
 
              # assign the 3 leptons and the neutrino to the correct vector boson
              #
              # 1) the neutrino is hte first position
              #
              ptv1  = temp_ptv1
              etav1 = temp_etav1
              phiv1 = temp_phiv1
              idv1  = temp_idv1
              #
              # 2) look for a lepton with the correct charge and the invariant mass close to W
              #
              v1 = ROOT.TLorentzVector()
              v1.SetPtEtaPhiM(ptv1, etav1, phiv1, 0)
                
              if (abs(idv1) == (abs(temp_idl1)+1)) :
                
                l1 = ROOT.TLorentzVector()
                l1.SetPtEtaPhiM(temp_ptl1, temp_etal1, temp_phil1, 0)
                
                mass = (l1+v1).M()                
                #print " mass = ", mass
                
                if abs (mass - 80.385) < 3 :
                  
                  ptl1  = temp_ptl1
                  etal1 = temp_etal1
                  phil1 = temp_phil1
                  idl1  = temp_idl1
                  
                  ptl2  = temp_ptl2
                  etal2 = temp_etal2
                  phil2 = temp_phil2
                  idl2  = temp_idl2
                 
                  ptv2  = temp_ptl3
                  etav2 = temp_etal3
                  phiv2 = temp_phil3
                  idv2  = temp_idl3    
                                 

                
              elif (abs(idv1) == (abs(temp_idl2)+1)) :
                
                l1 = ROOT.TLorentzVector()
                l1.SetPtEtaPhiM(temp_ptl2, temp_etal2, temp_phil2, 0)
                
                mass = (l1+v1).M()                
                #print " mass 2 = ", mass
                
                if abs (mass - 80.385) < 3 :
                  
                  ptl1  = temp_ptl2
                  etal1 = temp_etal2
                  phil1 = temp_phil2
                  idl1  = temp_idl2
                  
                  ptl2  = temp_ptl1
                  etal2 = temp_etal1
                  phil2 = temp_phil1
                  idl2  = temp_idl1
                 
                  ptv2  = temp_ptl3
                  etav2 = temp_etal3
                  phiv2 = temp_phil3
                  idv2  = temp_idl3    


              else :
                      
                ptl1  = temp_ptl3
                etal1 = temp_etal3
                phil1 = temp_phil3
                idl1  = temp_idl3

                ptl2  = temp_ptl1
                etal2 = temp_etal1
                phil2 = temp_phil1
                idl2  = temp_idl1
               
                ptv2  = temp_ptl2
                etav2 = temp_etal2
                phiv2 = temp_phil2
                idv2  = temp_idl2    
             
            #print " ptl1, etal1, phil1, idl1, ptl2, etal2, phil2, idl2, ptv1, etav1, phiv1, idv1, ptv2, etav2, phiv2, idv2, x1, x2, id1, id2 = ", ptl1, etal1, phil1, idl1, ptl2, etal2, phil2, idl2, ptv1, etav1, phiv1, idv1, ptv2, etav2, phiv2, idv2, x1, x2, id1, id2
            
            results_value_and_error = qq2wvEWKcorrections.getqq2WVEWKCorr(ptl1, etal1, phil1, idl1, ptl2, etal2, phil2, idl2, ptv1, etav1, phiv1, idv1, ptv2, etav2, phiv2, idv2, x1, x2, id1, id2,    1)
            ewkWZ[0] = results_value_and_error[0]
            ewkWZuncertainty[0] = results_value_and_error[1]
            
            otree.Fill()

        self.disconnect()
        print '- Eventloop completed'