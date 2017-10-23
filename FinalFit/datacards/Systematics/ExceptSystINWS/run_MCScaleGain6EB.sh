cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/Systematics/ExceptSystINWS/
text2workspace.py BinMCScaleGain6EB.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n MCScaleGain6EB  -M  Asymptotic BinMCScaleGain6EB.root --run=blind -m 125 --ct=-1 --cv=1
