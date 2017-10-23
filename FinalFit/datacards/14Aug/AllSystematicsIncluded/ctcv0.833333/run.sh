cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/FinalFit
eval `scramv1 runtime -sh`
cd /eos/user/h/hbakhshi/Personal/Projects/tHq/Analyzer/FinalFit/datacards/14Aug/ctcv0.833333
text2workspace.py BinTHQLeptonicTag.txt
combine -n Preselection  -M  Asymptotic BinTHQLeptonicTag.root --run=blind -m 125.5 --ct=0.833333 --cv=1
text2workspace.py BinTHQLeptonicTHQTag.txt
combine -n THQLeptonicTHQTag  -M  Asymptotic BinTHQLeptonicTHQTag.root --run=blind -m 125.5 --ct=0.833333 --cv=1
combineCards.py BinTHQLeptonicTHQTag.txt BinTHQLeptonicTTHTag.txt > CombinedTHQLeptonic.txt
text2workspace.py CombinedTHQLeptonic.txt
combine -n THQLeptonic -M Asymptotic CombinedTHQLeptonic.root --run=blind -m 125.5 --ct=0.833333 --cv=1
text2workspace.py BinMVATHQ.txt
combine -n MVATHQ  -M  Asymptotic BinMVATHQ.root --run=blind -m 125.5 --ct=0.833333 --cv=1
combineCards.py BinMVATHQ.txt BinMVATTH.txt > CombinedMVA.txt
text2workspace.py CombinedMVA.txt
combine -n MVA -M Asymptotic CombinedMVA.root --run=blind -m 125.5 --ct=0.833333 --cv=1
text2workspace.py BinEtaNJetTHQTag.txt
combine -n EtaNJetTHQTag  -M  Asymptotic BinEtaNJetTHQTag.root --run=blind -m 125.5 --ct=0.833333 --cv=1
combineCards.py BinEtaNJetTHQTag.txt BinEtaNJetTTHTag.txt > CombinedEtaNJet.txt
text2workspace.py CombinedEtaNJet.txt
combine -n EtaNJet -M Asymptotic CombinedEtaNJet.root --run=blind -m 125.5 --ct=0.833333 --cv=1
text2workspace.py BinEtaNbJetTHQTag.txt
combine -n EtaNbJetTHQTag  -M  Asymptotic BinEtaNbJetTHQTag.root --run=blind -m 125.5 --ct=0.833333 --cv=1
combineCards.py BinEtaNbJetTHQTag.txt BinEtaNbJetTTHTag.txt > CombinedEtaNbJet.txt
text2workspace.py CombinedEtaNbJet.txt
combine -n EtaNbJet -M Asymptotic CombinedEtaNbJet.root --run=blind -m 125.5 --ct=0.833333 --cv=1
text2workspace.py BinNJetNbJetTHQTag.txt
combine -n NJetNbJetTHQTag  -M  Asymptotic BinNJetNbJetTHQTag.root --run=blind -m 125.5 --ct=0.833333 --cv=1
combineCards.py BinNJetNbJetTHQTag.txt BinNJetNbJetTTHTag.txt > CombinedNJetNbJet.txt
text2workspace.py CombinedNJetNbJet.txt
combine -n NJetNbJet -M Asymptotic CombinedNJetNbJet.root --run=blind -m 125.5 --ct=0.833333 --cv=1
