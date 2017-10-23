cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/Systematics/SingleSystPerParam//RVtth_dm_2
text2workspace.py BinMCSmearHighR9EERho.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n MCSmearHighR9EERho  -M  Asymptotic BinMCSmearHighR9EERho.root --run=blind -m 125 --ct=-1 --cv=1
