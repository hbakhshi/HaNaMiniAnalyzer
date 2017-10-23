cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/Systematics/ExceptSyst/
text2workspace.py BinMCSmearLowR9EBPhi.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n MCSmearLowR9EBPhi  -M  Asymptotic BinMCSmearLowR9EBPhi.root --run=blind -m 125 --ct=-1 --cv=1
