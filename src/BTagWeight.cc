#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/BTagWeight.h"


float BTagWeight::weight(flashggJetCollection jets/*, int ntag*/){
	//if (!filter(ntag)){
      		//   std::cout << "nThis event should not pass the selection, what is it doing here?" << std::endl;
        //	return 0;
	//}
	int njetTags = jets.size();
	int comb = 1 << njetTags;
	float pMC = 0;
	float pData = 0;
	for (int i = 0; i < comb; i++){
		float mc = 1.;
      		float data = 1.;
      		int ntagged = 0;
      		for (int j = 0; j < njetTags; j++){
	  		bool tagged = ((i >> j) & 0x1) == 1;
			float eff = this->MCTagEfficiency(jets[j],WPT);
			float sf = this->TagScaleFactor(jets[j]);
	  		if (tagged){
	      			ntagged++;
				mc *= eff;
				data *= (eff*sf);
				//mc *= jetTags[j].eff;
				//data *= jetTags[j].eff * jetTags[j].sf;
			} else {
			        mc*=(1-eff);
                		data*=(1-sf*eff);
				//mc *= (1. - jetTags[j].eff);
				//data *= (1. - jetTags[j].eff * jetTags[j].sf);
            		}
        	}

      		if (filter(ntagged)){
			//std::cout << mc << " " << data << endl;
			pMC += mc;
			pData += data;
	        }
	}
	if (pMC == 0) return 0;
	return pData / pMC;
}



float BTagWeight::weightExclusive(flashggJetCollection jets){
//This function takes into account cases where you have n b-tags and m vetoes, but they have different thresholds.
    if(WPL == -1){
	std::cout<<"FATAL ERROR: Provide the second btag WP!!!!"<<std::endl;
	return 0;
    } //https://twiki.cern.ch/twiki/pub/CMS/BTagSFMethods/latex3766350f938279e8ab2cee576fcba0d7.png
    std::vector<float> effL, effT, sfL, sfT;
    for (auto j : jets){
	effL.push_back(this->MCTagEfficiency(j,WPL));
	sfL.push_back(this->TagScaleFactor(j,(WPL != -1)));
	effT.push_back(this->MCTagEfficiency(j,WPT));
	sfT.push_back(this->TagScaleFactor(j));
    }
    int njetTags = jets.size();
    int comb = 1 << njetTags;
    float pMC = 0;
    float pData = 0;

    for (int i = 0; i < comb; i++){
      	int ntagged = 0;
        float wNonTaggedData = 1;
        float wNonTaggedMC = 1;
	std::vector<unsigned int> taggedIndecies;
      	for (int j = 0; j < njetTags; j++){
		bool tagged = ((i >> j) & 0x1) == 1;
	  	if (tagged){
	      		ntagged++;
			taggedIndecies.push_back(j);
		} else {
			wNonTaggedMC*=(1.-effL[j]);
                	wNonTaggedData*=(1.-sfL[j]*effL[j]);
            	}
       	}
	
	int combTagged = 1 << ntagged;
	for (int iTagged = 0; iTagged < combTagged; iTagged++){
		int nLoose = 0;
		float wTaggedData = 1;
                float wTaggedMC = 1;
	      	for (int jTagged = 0; jTagged < ntagged; jTagged++){
			bool tight = ((iTagged >> jTagged) & 0x1) == 1;	
			unsigned int realIndex = taggedIndecies[jTagged];

			if (tight){
				wTaggedMC*=(effT[realIndex]);
                		wTaggedData*=(sfT[realIndex]*effT[realIndex]);
			} else {
				nLoose++;
				wTaggedMC*=(effT[realIndex] - effL[realIndex]);
                		wTaggedData*=(sfT[realIndex]*effT[realIndex] - sfL[realIndex]*effL[realIndex]);
			}
		}
		if( filter( ntagged-nLoose , nLoose ) ){
			pMC += ( wNonTaggedMC*wTaggedMC );
			pData += (wNonTaggedData*wTaggedData) ;
		}
	}
    }
    if (pMC == 0) return 0;
    return pData / pMC;

}
//*************************************************************************

float BTagWeight::MCTagEfficiency(flashgg::Jet jet, int WP){
  int flavor = fabs(jet.hadronFlavour());
  if(flavor == 5){
    if(WP==0) return 0.38; //L
    if(WP==1) return 0.58; //M
    if(WP==2) return 0.755;//T
  }
  if(flavor == 4){
    if(WP==0) return 0.015; //L
    if(WP==1) return 0.08; //M
    if(WP==2) return 0.28;//T
  }
  if(flavor != 4){
    if(WP==0) return 0.0008; //L
    if(WP==1) return 0.007; //M
    if(WP==2) return 0.079;//T
 }
  return 1.0;
}

float BTagWeight::TagScaleFactor(flashgg::Jet jet, bool LooseWP ){

	float MinJetPt = 20.;
	float MaxBJetPt = 670., MaxLJetPt = 1000.;
        float JetPt = jet.pt(); bool DoubleUncertainty = false;
	int flavour = fabs(jet.hadronFlavour());
	if(flavour == 5) flavour = BTagEntry::FLAV_B;
	else if(flavour == 4) flavour = BTagEntry::FLAV_C;
	else flavour = BTagEntry::FLAV_UDSG;
	
	if(flavour != BTagEntry::FLAV_UDSG){
	   if (JetPt>MaxBJetPt)  { // use MaxLJetPt for  light jets
        	JetPt = MaxBJetPt; 
        	DoubleUncertainty = true;
      	   }
	} else {
	   if (JetPt>MaxLJetPt)  { // use MaxLJetPt for  light jets
                JetPt = MaxBJetPt;
                DoubleUncertainty = true;
           }
	}
	if(JetPt<MinJetPt){
	   JetPt = MinJetPt;
	   DoubleUncertainty = true;
	}

	float jet_scalefactor = 1;
	if((BTagEntry::JetFlavor)flavour != BTagEntry::FLAV_UDSG){
		jet_scalefactor = reader->eval((BTagEntry::JetFlavor)flavour, jet.eta(), JetPt); 
		if(LooseWP)
			jet_scalefactor = readerExc->eval((BTagEntry::JetFlavor)flavour, jet.eta(), JetPt);
	} else {
		jet_scalefactor = readerLight->eval((BTagEntry::JetFlavor)flavour, jet.eta(), JetPt);
		if(LooseWP)
			jet_scalefactor = readerExcLight->eval((BTagEntry::JetFlavor)flavour, jet.eta(), JetPt);
	}


	if(DoubleUncertainty && syst != 0){
	        float jet_scalefactorCent = 1;
		if((BTagEntry::JetFlavor)flavour != BTagEntry::FLAV_UDSG){
			jet_scalefactorCent = readerCent->eval((BTagEntry::JetFlavor)flavour, jet.eta(), JetPt); 
			if(LooseWP)
				jet_scalefactorCent = readerCentExc->eval((BTagEntry::JetFlavor)flavour, jet.eta(), JetPt);
		} else {
			jet_scalefactorCent = readerCentLight->eval((BTagEntry::JetFlavor)flavour, jet.eta(), JetPt); 
			if(LooseWP)
				jet_scalefactorCent = readerCentExcLight->eval((BTagEntry::JetFlavor)flavour, jet.eta(), JetPt);
		}
                jet_scalefactor = 2*(jet_scalefactor - jet_scalefactorCent) + jet_scalefactorCent; 
	}
	return jet_scalefactor;
}

