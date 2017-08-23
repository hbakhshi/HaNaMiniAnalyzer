#! /bin/bash

mkdir $1
cd $1
text2workspace.py ../$1.txt -m 125 -o ./$1.root
combineTool.py -t -1 --expectSignal=1 -M Impacts -d $1.root -m 125 --doInitialFit --robustFit 1 --rMin=0 --rMax=10 > InitialFitOut.txt
combineTool.py -M Impacts -d $1.root -m 125 --robustFit 1 --doFits --parallel $2
combineTool.py -M Impacts -d $1.root -m 125 -o impacts.json
plotImpacts.py -i impacts.json -o impacts

