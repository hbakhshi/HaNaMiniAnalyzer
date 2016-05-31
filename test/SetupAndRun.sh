export X509_USER_PROXY=$1
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=$2
scramv1 project CMSSW $3
cd $3/src/
eval `scramv1 runtime -sh`
mkdir tHqAnalyzer/
cd tHqAnalyzer
git clone https://github.com/nadjieh/HaNaMiniAnalyzer/
cd HaNaMiniAnalyzer/
git checkout $4
scram b
cd test

if [ ! -z "$LSB_JOBINDEX" ];
then
    echo $LSB_JOBINDEX
    export FILEID=`expr $LSB_JOBINDEX - 1`
    echo $FILEID
else
    if [ ! -z "$CONDORJOBID" ];
    then
	export FILEID=$CONDORJOBID
	echo $FILEID
    fi
fi


echo cmsRun ConfFile_cfg.py sample=$5 job=$FILEID output=$6 maxEvents=-1 nFilesPerJob=$8
cmsRun ConfFile_cfg.py sample=$5 job=$FILEID output=$6 maxEvents=-1 nFilesPerJob=$8

if [[ $7 == eos* ]] ;
then
    echo is mounting eos
    mkdir eos
  
    /afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select -b fuse mount eos
    mountpoint eos
    while [ $? -ne 0 ]; do
	/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select -b fuse mount eos
	mountpoint eos
    done
fi

mkdir -p $7

outfilename=`ls $6*$5*.root`

ls -l $outfilename

if [ -f  $7/$outfilename ]; then
    echo "the file exists, is being renamed"
    mv $7/$outfilename $7/${outfilename}_
fi

COUNTER2=0
while [ ! -f  $7/$outfilename ]
do
    if [ $COUNTER2 -gt 20 ]; then
	break
    fi
    cp $outfilename $7/
    let COUNTER2=COUNTER2+1
    echo ${COUNTER2}th Try
    sleep 10
done
    
rm $outfilename

if [ ! -f  $7/$outfilename ]; then
    echo "The file was not copied to destination after 20 tries"
    exit 1
fi

if [[ $7 == eos* ]] ;
then
    /afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select -b fuse umount eos
    rm -rf eos
fi
