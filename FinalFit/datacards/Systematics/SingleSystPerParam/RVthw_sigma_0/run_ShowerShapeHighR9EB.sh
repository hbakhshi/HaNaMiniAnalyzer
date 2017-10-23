cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/Systematics/SingleSystPerParam//RVthw_sigma_0
text2workspace.py BinShowerShapeHighR9EB.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n ShowerShapeHighR9EB  -M  Asymptotic BinShowerShapeHighR9EB.root --run=blind -m 125 --ct=-1 --cv=1
