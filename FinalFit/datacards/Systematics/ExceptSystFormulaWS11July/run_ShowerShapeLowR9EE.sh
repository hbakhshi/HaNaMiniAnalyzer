cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/Systematics/ExceptSystFormulaWS11July/
text2workspace.py BinShowerShapeLowR9EE.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n ShowerShapeLowR9EE  -M  Asymptotic BinShowerShapeLowR9EE.root --run=blind -m 125 --ct=-1 --cv=1
