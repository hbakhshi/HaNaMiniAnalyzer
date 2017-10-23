cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/Systematics/SingleSystPerParam//RVthw_frac_0
text2workspace.py BinMCSmearLowR9EEPhi.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n MCSmearLowR9EEPhi  -M  Asymptotic BinMCSmearLowR9EEPhi.root --run=blind -m 125 --ct=-1 --cv=1
