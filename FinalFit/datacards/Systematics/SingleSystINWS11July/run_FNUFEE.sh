cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd FinalFit/datacards/Systematics/SingleSystINWS11July/
text2workspace.py BinFNUFEE.txt
combine --X-rtd ADDNLL_RECURSIVE=0 -n FNUFEE  -M  Asymptotic BinFNUFEE.root --run=blind -m 125 --ct=-1 --cv=1
