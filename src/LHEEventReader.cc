#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/LHEEventReader.h"
#include <iostream>

LHEEventReader::LHEEventReader( edm::ParameterSet const& iPS, edm::ConsumesCollector && iC) :
  BaseEventReader< LHEEventProduct >( iPS , &iC )
{
  
}

double LHEEventReader::Read( const edm::Event& iEvent ){
  BaseEventReader< LHEEventProduct >::Read( iEvent );
  WeightSign = (handle->hepeup().XWGTUP > 0) ? 1.0 : -1.0 ; 
  return WeightSign;
}

std::valarray<double> LHEEventReader::ExtractWeightsInRange( int from , int to ){
  std::vector<double> ret;
  double orig_w = handle->originalXWGTUP();
  
  ret.push_back( orig_w/fabs( orig_w ) );
  for(int i=from ; i <= to ; i++){
    //std::cout << i << endl;
    ret.push_back( handle->weights()[i].wgt / fabs(orig_w) ) ;
  }

  std::valarray<double> ret_( ret.data() , ret.size() );
  return ret_;
}
