cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/Systematics/SingleSystPerParam//RVvh_sigma_2
text2workspace.py BinMCScaleHighR9EB.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n MCScaleHighR9EB  -M  Asymptotic BinMCScaleHighR9EB.root --run=blind -m 125 --ct=-1 --cv=1