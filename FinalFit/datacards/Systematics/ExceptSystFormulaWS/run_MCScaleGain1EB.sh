cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/Systematics/ExceptSystFormulaWS/
text2workspace.py BinMCScaleGain1EB.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n MCScaleGain1EB  -M  Asymptotic BinMCScaleGain1EB.root --run=blind -m 125 --ct=-1 --cv=1
