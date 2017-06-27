cd /home/hbakhshi/Desktop/tHq/HiggsAnalysis/CombinedLimit
source env_standalone.sh
cd -

## declare an array variable
#declare -a arr=( 3.  2.  1.5  1.25   1.0 .75  .5  .25  0.0  -0.25  -0.5  -0.75 -1  -1.25  -1.5  -2.  -3. )

declare -a arr=( -1  1 )

# CMS_hgg_nuisance_ShowerShapeHighR9EB_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MCSmearHighR9EBPhi_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MCScaleHighR9EB_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MCSmearLowR9EBPhi_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MaterialForward_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MvaShift_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MCSmearHighR9EBRho_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MCScaleGain6EB_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MCScaleLowR9EB_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MaterialOuterBarrel_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MCSmearLowR9EEPhi_13TeV param 0.0 1.0
# CMS_hgg_nuisance_metJerUncertainty_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MCSmearHighR9EEPhi_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MaterialCentralBarrel_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MCSmearLowR9EBRho_13TeV param 0.0 1.0
# CMS_hgg_nuisance_FNUFEB_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MCScaleHighR9EE_13TeV param 0.0 1.0
# CMS_hgg_nuisance_MCSmearHighR9EERho_13TeV param 0.0 1.0

## now loop through the above array
for i in "${arr[@]}"
do
    echo "$i"
    echo ${1}
    combine  -M  Asymptotic hgg_card_13TeV_thq_moriond17_NoTHMVACut_onlythq.txt --run=blind -m 125.5 --ct="$i" --cv=${1}
   # or do whatever with individual element of the array
done

# You can access them using echo "${arr[0]}", "${arr[1]}" also

