# formulas to be added, in python language
# call to branches have to be in the form event.branchName
# if you want to use logical operators, the have to be the python ones (i.e "and" not " and ")

formulas = {}

# from https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#Moriond_2018
METFilter_Common = '(event.Flag_goodVertices*\
                     event.Flag_globalSuperTightHalo2016Filter*\
                     event.Flag_HBHENoiseFilter*\
                     event.Flag_HBHENoiseIsoFilter*\
                     event.Flag_EcalDeadCellTriggerPrimitiveFilter*\
                     event.Flag_BadPFMuonFilter*\
                     event.Flag_BadChargedCandidateFilter*\
                     event.Flag_ecalBadCalibFilter\
                   )'

METFilter_DATA   =  METFilter_Common 

formulas['METFilter_MC'] = METFilter_DATA

# Common Weights


formulas['XSWeight'] = 'event.baseW*\
                        event.genWeight \
                        if hasattr(event, \'genWeight\') else event.baseW'


formulas['SFweight2l'] = 'event.puWeight*\
                          event.TriggerEffWeight_2l*\
                          event.Lepton_RecoSF[0]*\
                          event.Lepton_RecoSF[1]*\
                          event.EMTFbug_veto \
                          if event.nLepton > 1 else 0.'

formulas['SFweight3l'] = 'event.puWeight*\
                          event.TriggerEffWeight_3l*\
                          event.Lepton_RecoSF[0]*\
                          event.Lepton_RecoSF[1]*\
                          event.Lepton_RecoSF[2]*\
                          event.EMTFbug_veto \
                          if event.nLepton > 2 else 0.'

formulas['SFweight4l'] = 'event.puWeight*\
                          event.TriggerEffWeight_4l*\
                          event.Lepton_RecoSF[0]*\
                          event.Lepton_RecoSF[1]*\
                          event.Lepton_RecoSF[2]*\
                          event.Lepton_RecoSF[3]*\
                          event.EMTFbug_veto \
                          if event.nLepton > 3 else 0.'


# Lepton WP

formulas['LepCut2l'] = '(event.nLepton>=2 and (event.Lepton_isTightElectron_mvaFall17Iso_WP90[0]>0.5 or event.Lepton_isTightMuon_cut_Tight_HWWW[0]>0.5) and \
                                              (event.Lepton_isTightElectron_mvaFall17Iso_WP90[1]>0.5 or event.Lepton_isTightMuon_cut_Tight_HWWW[1]>0.5) )' 

formulas['LepCut2lSS'] = '(event.nLepton>=2 and (event.Lepton_isTightElectron_mvaFall17Iso_WP90_SS[0]>0.5 or event.Lepton_isTightMuon_cut_Tight_HWWW[0]>0.5) and \
                                              (event.Lepton_isTightElectron_mvaFall17Iso_WP90_SS[1]>0.5 or event.Lepton_isTightMuon_cut_Tight_HWWW[1]>0.5) )' 

formulas['LepCut3l'] = '(event.nLepton>=3 and (event.Lepton_isTightElectron_mvaFall17Iso_WP90[0]>0.5 or event.Lepton_isTightMuon_cut_Tight_HWWW[0]>0.5) and \
                                              (event.Lepton_isTightElectron_mvaFall17Iso_WP90[1]>0.5 or event.Lepton_isTightMuon_cut_Tight_HWWW[1]>0.5) and \
                                              (event.Lepton_isTightElectron_mvaFall17Iso_WP90[2]>0.5 or event.Lepton_isTightMuon_cut_Tight_HWWW[2]>0.5) )'

formulas['LepCut4l'] = '(event.nLepton>=4 and (event.Lepton_isTightElectron_mvaFall17Iso_WP90[0]>0.5 or event.Lepton_isTightMuon_cut_Tight_HWWW[0]>0.5) and \
                                              (event.Lepton_isTightElectron_mvaFall17Iso_WP90[1]>0.5 or event.Lepton_isTightMuon_cut_Tight_HWWW[1]>0.5) and \
                                              (event.Lepton_isTightElectron_mvaFall17Iso_WP90[2]>0.5 or event.Lepton_isTightMuon_cut_Tight_HWWW[2]>0.5) and \
                                              (event.Lepton_isTightElectron_mvaFall17Iso_WP90[3]>0.5 or event.Lepton_isTightMuon_cut_Tight_HWWW[3]>0.5) )'


muWP='cut_Tight_HWWW'
eleWPlist = ['mvaFall17Iso_WP90', 'mvaFall17Iso_WP90_SS']

for eleWP in eleWPlist: 

  formulas['LepSF2l__ele_'+eleWP+'__mu_'+muWP] = 'event.Lepton_tightElectron_'+eleWP+'_IdIsoSF'+'[0]*\
                                                  event.Lepton_tightElectron_'+eleWP+'_IdIsoSF'+'[1]*\
                                                  event.Lepton_tightMuon_'+muWP+'_IdIsoSF'+'[0]*\
                                                  event.Lepton_tightMuon_'+muWP+'_IdIsoSF'+'[1] \
                                                  if event.nLepton > 1 else 0.'

  formulas['LepSF3l__ele_'+eleWP+'__mu_'+muWP] = 'event.Lepton_tightElectron_'+eleWP+'_IdIsoSF'+'[0]*\
                                                  event.Lepton_tightElectron_'+eleWP+'_IdIsoSF'+'[1]*\
                                                  event.Lepton_tightElectron_'+eleWP+'_IdIsoSF'+'[2]*\
                                                  event.Lepton_tightMuon_'+muWP+'_IdIsoSF'+'[0]*\
                                                  event.Lepton_tightMuon_'+muWP+'_IdIsoSF'+'[1]*\
                                                  event.Lepton_tightMuon_'+muWP+'_IdIsoSF'+'[2] \
                                                  if event.nLepton > 2 else 0.'

  formulas['LepSF4l__ele_'+eleWP+'__mu_'+muWP] = 'event.Lepton_tightElectron_'+eleWP+'_IdIsoSF'+'[0]*\
                                                  event.Lepton_tightElectron_'+eleWP+'_IdIsoSF'+'[1]*\
                                                  event.Lepton_tightElectron_'+eleWP+'_IdIsoSF'+'[2]*\
                                                  event.Lepton_tightElectron_'+eleWP+'_IdIsoSF'+'[3]*\
                                                  event.Lepton_tightMuon_'+muWP+'_IdIsoSF'+'[0]*\
                                                  event.Lepton_tightMuon_'+muWP+'_IdIsoSF'+'[1]*\
                                                  event.Lepton_tightMuon_'+muWP+'_IdIsoSF'+'[2]*\
                                                  event.Lepton_tightMuon_'+muWP+'_IdIsoSF'+'[3] \
                                                  if event.nLepton > 3 else 0.'

  formulas['LepCut2l__ele_'+eleWP+'__mu_'+muWP] = '((event.Lepton_isTightElectron_'+eleWP+'[0]>0.5 or event.Lepton_isTightMuon_'+muWP+'[0]>0.5) and \
                                                    (event.Lepton_isTightElectron_'+eleWP+'[1]>0.5 or event.Lepton_isTightMuon_'+muWP+'[1]>0.5)) \
                                                   if event.nLepton > 1 else 0.'

  formulas['LepCut3l__ele_'+eleWP+'__mu_'+muWP] = '((event.Lepton_isTightElectron_'+eleWP+'[0]>0.5 or event.Lepton_isTightMuon_'+muWP+'[0]>0.5) and \
                                                    (event.Lepton_isTightElectron_'+eleWP+'[1]>0.5 or event.Lepton_isTightMuon_'+muWP+'[1]>0.5) and \
                                                    (event.Lepton_isTightElectron_'+eleWP+'[2]>0.5 or event.Lepton_isTightMuon_'+muWP+'[2]>0.5)) \
                                                   if event.nLepton > 2 else 0.'

  formulas['LepCut4l__ele_'+eleWP+'__mu_'+muWP] = '((event.Lepton_isTightElectron_'+eleWP+'[0]>0.5 or event.Lepton_isTightMuon_'+muWP+'[0]>0.5) and \
                                                    (event.Lepton_isTightElectron_'+eleWP+'[1]>0.5 or event.Lepton_isTightMuon_'+muWP+'[1]>0.5) and \
                                                    (event.Lepton_isTightElectron_'+eleWP+'[2]>0.5 or event.Lepton_isTightMuon_'+muWP+'[2]>0.5) and \
                                                    (event.Lepton_isTightElectron_'+eleWP+'[3]>0.5 or event.Lepton_isTightMuon_'+muWP+'[3]>0.5)) \
                                                   if event.nLepton > 3 else 0.'

  formulas['LepSF2l__ele_'+eleWP+'__Up'] = '((abs(event.Lepton_pdgId[0]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Up[0])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[0])+\
                                             (abs(event.Lepton_pdgId[0]) == 13)) * \
                                            ((abs(event.Lepton_pdgId[1]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Up[1])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[1])+\
                                             (abs(event.Lepton_pdgId[1]) == 13)) \
                                            if event.nLepton > 1 else 0.'

  formulas['LepSF2l__ele_'+eleWP+'__Do'] = '((abs(event.Lepton_pdgId[0]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Down[0])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[0])+\
                                             (abs(event.Lepton_pdgId[0]) == 13)) * \
                                            ((abs(event.Lepton_pdgId[1]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Down[1])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[1])+\
                                             (abs(event.Lepton_pdgId[1]) == 13)) \
                                            if event.nLepton > 1 else 0.'

  formulas['LepSF3l__ele_'+eleWP+'__Up'] = '((abs(event.Lepton_pdgId[0]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Up[0])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[0])+\
                                             (abs(event.Lepton_pdgId[0]) == 13)) * \
                                            ((abs(event.Lepton_pdgId[1]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Up[1])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[1])+\
                                             (abs(event.Lepton_pdgId[1]) == 13)) * \
                                            ((abs(event.Lepton_pdgId[2]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Up[2])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[2])+\
                                             (abs(event.Lepton_pdgId[2]) == 13)) \
                                            if event.nLepton > 2 else 0.'

  formulas['LepSF3l__ele_'+eleWP+'__Do'] = '((abs(event.Lepton_pdgId[0]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Down[0])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[0])+\
                                             (abs(event.Lepton_pdgId[0]) == 13)) * \
                                            ((abs(event.Lepton_pdgId[1]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Down[1])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[1])+\
                                             (abs(event.Lepton_pdgId[1]) == 13)) * \
                                            ((abs(event.Lepton_pdgId[2]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Down[2])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[2])+\
                                             (abs(event.Lepton_pdgId[2]) == 13)) \
                                            if event.nLepton > 2 else 0.'

  formulas['LepSF4l__ele_'+eleWP+'__Up'] = '((abs(event.Lepton_pdgId[0]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Up[0])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[0])+\
                                             (abs(event.Lepton_pdgId[0]) == 13)) * \
                                            ((abs(event.Lepton_pdgId[1]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Up[1])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[1])+\
                                             (abs(event.Lepton_pdgId[1]) == 13)) * \
                                            ((abs(event.Lepton_pdgId[2]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Up[2])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[2])+\
                                             (abs(event.Lepton_pdgId[2]) == 13)) * \
                                            ((abs(event.Lepton_pdgId[3]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Up[3])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[3])+\
                                             (abs(event.Lepton_pdgId[3]) == 13)) \
                                            if event.nLepton > 3 else 0.'

  formulas['LepSF4l__ele_'+eleWP+'__Do'] = '((abs(event.Lepton_pdgId[0]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Down[0])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[0])+\
                                             (abs(event.Lepton_pdgId[0]) == 13)) * \
                                            ((abs(event.Lepton_pdgId[1]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Down[1])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[1])+\
                                             (abs(event.Lepton_pdgId[1]) == 13)) * \
                                            ((abs(event.Lepton_pdgId[2]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Down[2])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[2])+\
                                             (abs(event.Lepton_pdgId[2]) == 13)) * \
                                            ((abs(event.Lepton_pdgId[3]) == 11)*(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'_Down[3])/(event.Lepton_tightElectron_'+eleWP+'_TotSF'+'[3])+\
                                             (abs(event.Lepton_pdgId[3]) == 13)) \
                                            if event.nLepton > 3 else 0.'

formulas['LepSF2l__mu_'+muWP+'__Up'] = '((abs(event.Lepton_pdgId[0]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Up[0])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[0])+\
                                         (abs(event.Lepton_pdgId[0]) == 11)) * \
                                        ((abs(event.Lepton_pdgId[1]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Up[1])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[1])+\
                                         (abs(event.Lepton_pdgId[1]) == 11)) \
                                        if event.nLepton > 1 else 0.'

formulas['LepSF2l__mu_'+muWP+'__Do'] = '((abs(event.Lepton_pdgId[0]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Down[0])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[0])+\
                                         (abs(event.Lepton_pdgId[0]) == 11)) * \
                                        ((abs(event.Lepton_pdgId[1]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Down[1])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[1])+\
                                         (abs(event.Lepton_pdgId[1]) == 11)) \
                                        if event.nLepton > 1 else 0.'
                                        
formulas['LepSF3l__mu_'+muWP+'__Up'] = '((abs(event.Lepton_pdgId[0]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Up[0])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[0])+\
                                         (abs(event.Lepton_pdgId[0]) == 11)) * \
                                        ((abs(event.Lepton_pdgId[1]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Up[1])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[1])+\
                                         (abs(event.Lepton_pdgId[1]) == 11)) * \
                                        ((abs(event.Lepton_pdgId[2]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Up[2])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[2])+\
                                         (abs(event.Lepton_pdgId[2]) == 11)) \
                                        if event.nLepton > 2 else 0.'

formulas['LepSF3l__mu_'+muWP+'__Do'] = '((abs(event.Lepton_pdgId[0]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Down[0])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[0])+\
                                         (abs(event.Lepton_pdgId[0]) == 11)) * \
                                        ((abs(event.Lepton_pdgId[1]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Down[1])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[1])+\
                                         (abs(event.Lepton_pdgId[1]) == 11)) * \
                                        ((abs(event.Lepton_pdgId[2]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Down[2])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[2])+\
                                         (abs(event.Lepton_pdgId[2]) == 11)) \
                                        if event.nLepton > 2 else 0.'

formulas['LepSF4l__mu_'+muWP+'__Up'] = '((abs(event.Lepton_pdgId[0]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Up[0])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[0])+\
                                         (abs(event.Lepton_pdgId[0]) == 11)) * \
                                        ((abs(event.Lepton_pdgId[1]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Up[1])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[1])+\
                                         (abs(event.Lepton_pdgId[1]) == 11)) * \
                                        ((abs(event.Lepton_pdgId[2]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Up[2])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[2])+\
                                         (abs(event.Lepton_pdgId[2]) == 11)) * \
                                        ((abs(event.Lepton_pdgId[3]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Up[3])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[3])+\
                                         (abs(event.Lepton_pdgId[3]) == 11)) \
                                        if event.nLepton > 3 else 0.'

formulas['LepSF4l__mu_'+muWP+'__Do'] = '((abs(event.Lepton_pdgId[0]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Down[0])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[0])+\
                                         (abs(event.Lepton_pdgId[0]) == 11)) * \
                                        ((abs(event.Lepton_pdgId[1]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Down[1])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[1])+\
                                         (abs(event.Lepton_pdgId[1]) == 11)) * \
                                        ((abs(event.Lepton_pdgId[2]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Down[2])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[2])+\
                                         (abs(event.Lepton_pdgId[2]) == 11)) * \
                                        ((abs(event.Lepton_pdgId[3]) == 13)*(event.Lepton_tightMuon_'+muWP+'_TotSF'+'_Down[3])/(event.Lepton_tightMuon_'+muWP+'_TotSF'+'[3])+\
                                         (abs(event.Lepton_pdgId[3]) == 11)) \
                                        if event.nLepton > 3 else 0.'

formulas['GenLepMatch2l'] = 'event.Lepton_genmatched[0]*\
                             event.Lepton_genmatched[1] \
                             if event.nLepton > 1 else 0.'

formulas['GenLepMatch3l'] = 'event.Lepton_genmatched[0]*\
                             event.Lepton_genmatched[1]*\
                             event.Lepton_genmatched[2] \
                             if event.nLepton > 2 else 0.'

formulas['GenLepMatch4l'] = 'event.Lepton_genmatched[0]*\
                             event.Lepton_genmatched[1]*\
                             event.Lepton_genmatched[2]*\
                             event.Lepton_genmatched[3] \
                             if event.nLepton > 3 else 0.'
