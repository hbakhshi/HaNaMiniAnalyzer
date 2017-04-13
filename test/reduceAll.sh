#!/bin/bash
shopt -s nullglob
maindir=/home/hbakhshi/Downloads/tHq_Georgios/output/03_15_17/
datafiles=$maindir/data/WS_*.root
signalfiles=$maindir/signals/WS_*.root
bkgfiles=$maindir/bkgs/WS_*.root

for f in $datafiles
do
	echo "reducing ws in - $f"
        root -l -q ReduceDataset.C\(\"$f\"\)
done
for f in $bkgfiles
do
	echo "reducing ws in - $f"
        root -l -q ReduceDataset.C\(\"$f\"\)
done
for f in $signalfiles
do
	echo "reducing ws in - $f"
        root -l -q ReduceDataset.C\(\"$f\"\)
done

