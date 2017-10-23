cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/Systematics/SingleSystPerParam//RVthw_dm_2
text2workspace.py BinFNUFEB.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n FNUFEB  -M  Asymptotic BinFNUFEB.root --run=blind -m 125 --ct=-1 --cv=1
