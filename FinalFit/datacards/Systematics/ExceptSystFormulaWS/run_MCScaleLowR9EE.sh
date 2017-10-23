cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/Systematics/ExceptSystFormulaWS/
text2workspace.py BinMCScaleLowR9EE.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n MCScaleLowR9EE  -M  Asymptotic BinMCScaleLowR9EE.root --run=blind -m 125 --ct=-1 --cv=1
