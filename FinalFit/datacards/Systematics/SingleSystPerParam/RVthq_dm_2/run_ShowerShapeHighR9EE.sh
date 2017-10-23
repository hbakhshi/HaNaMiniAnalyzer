cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/Systematics/SingleSystPerParam//RVthq_dm_2
text2workspace.py BinShowerShapeHighR9EE.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n ShowerShapeHighR9EE  -M  Asymptotic BinShowerShapeHighR9EE.root --run=blind -m 125 --ct=-1 --cv=1
