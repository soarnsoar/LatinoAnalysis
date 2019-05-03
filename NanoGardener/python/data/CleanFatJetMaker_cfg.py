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

CleanFatJet_br = {
               'F': [
                     'CleanFatJet_pt',
                     'CleanFatJet_eta',
                     'CleanFatJet_phi',
                     'CleanFatJet_mass',
                     'CleanFatJet_msoftdrop',
                     'CleanFatJet_jetId',
                     'CleanFatJet_rawFactor',
                     'CleanFatJet_tau1',
                     'CleanFatJet_tau2',
                     'CleanFatJet_area',
                     ],

               'I': [
                     'CleanFatJet_fatjetIdx',
                    ],
              }

CleanFatJet_var = ['pt', 'eta', 'phi', 'mass', 'msoftdrop', 'jetId', 'rawFactor', 'tau1', 'tau2', 'area']
