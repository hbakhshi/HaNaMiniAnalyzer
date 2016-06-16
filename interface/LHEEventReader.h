#ifndef LHEEventReader_H
#define LHEEventReader_H

#include <valarray>     // std::valarray
#include "BaseEventReader.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

using namespace edm;
//using namespace reco;

class LHEEventReader : public BaseEventReader< LHEEventProduct > {
public:
  LHEEventReader( edm::ParameterSet const& iPS, edm::ConsumesCollector && iC);
  double Read( const edm::Event& iEvent ) override;
  double WeightSign;

  std::valarray<double> ExtractWeightsInRange( int from , int to );
private :

};

#endif
