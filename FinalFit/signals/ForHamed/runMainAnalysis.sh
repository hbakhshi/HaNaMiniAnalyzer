cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/FinalFit
eval `scramv1 runtime -sh`
cd /eos/user/h/hbakhshi/Personal/Projects/tHq/Analyzer/FinalFit/signals/ForHamed/
text2workspace.py MainAnalysisCard.txt
combine -n MainAnalysis  -M  Asymptotic MainAnalysisCard.root --run=blind -m 125 --ct=-1 --cv=1
