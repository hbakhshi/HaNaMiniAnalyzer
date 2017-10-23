cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/CRInvLepCut22July/ctcv0.25
text2workspace.py BinCRInvertLepCutTHQLeptonicTag.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n Preselection  -M  Asymptotic BinCRInvertLepCutTHQLeptonicTag.root --run=blind -m 125 --ct=0.25 --cv=1
text2workspace.py BinCRInvertLepCutTHQLeptonicTHQTag.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n CRInvertLepCutTHQLeptonicTHQTag  -M  Asymptotic BinCRInvertLepCutTHQLeptonicTHQTag.root --run=blind -m 125 --ct=0.25 --cv=1
combineCards.py BinCRInvertLepCutTHQLeptonicTHQTag.txt BinCRInvertLepCutTHQLeptonicTTHTag.txt > CombinedTHQLeptonic.txt
text2workspace.py CombinedTHQLeptonic.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n THQLeptonic -M Asymptotic CombinedTHQLeptonic.root --run=blind -m 125 --ct=0.25 --cv=1
text2workspace.py BinCRInvertLepCutEtaNJetTHQTag.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n CRInvertLepCutEtaNJetTHQTag  -M  Asymptotic BinCRInvertLepCutEtaNJetTHQTag.root --run=blind -m 125 --ct=0.25 --cv=1
combineCards.py BinCRInvertLepCutEtaNJetTHQTag.txt BinCRInvertLepCutEtaNJetTTHTag.txt > CombinedEtaNJet.txt
text2workspace.py CombinedEtaNJet.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n EtaNJet -M Asymptotic CombinedEtaNJet.root --run=blind -m 125 --ct=0.25 --cv=1
text2workspace.py BinCRInvertLepCutEtaNbJetTHQTag.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n CRInvertLepCutEtaNbJetTHQTag  -M  Asymptotic BinCRInvertLepCutEtaNbJetTHQTag.root --run=blind -m 125 --ct=0.25 --cv=1
combineCards.py BinCRInvertLepCutEtaNbJetTHQTag.txt BinCRInvertLepCutEtaNbJetTTHTag.txt > CombinedEtaNbJet.txt
text2workspace.py CombinedEtaNbJet.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n EtaNbJet -M Asymptotic CombinedEtaNbJet.root --run=blind -m 125 --ct=0.25 --cv=1
text2workspace.py BinCRInvertLepCutNJetNbJetTHQTag.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n CRInvertLepCutNJetNbJetTHQTag  -M  Asymptotic BinCRInvertLepCutNJetNbJetTHQTag.root --run=blind -m 125 --ct=0.25 --cv=1
combineCards.py BinCRInvertLepCutNJetNbJetTHQTag.txt BinCRInvertLepCutNJetNbJetTTHTag.txt > CombinedNJetNbJet.txt
text2workspace.py CombinedNJetNbJet.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n NJetNbJet -M Asymptotic CombinedNJetNbJet.root --run=blind -m 125 --ct=0.25 --cv=1
