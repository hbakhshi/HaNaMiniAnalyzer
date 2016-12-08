######################################################################
# Project: TMVA - Toolkit for Multivariate Data Analysis             #
# Code   : Example usage for TMVA analyses                           #
###################################################################### 
CXX = g++
CCFLAGS = -O0 -ggdb -std=c++11 


LD = g++
LDFLAGS = 

LIBS = $(shell root-config --libdir) 
INCS = $(shell root-config --incdir)  


default : bin/TMVAClassification bin/MakeFriendTrees.so

bin/TMVAClassification : src/TMVAClassification.C
	@echo -n "Building $@ ... "
	$(CXX) $(CCFLAGS) $<  $(addprefix -I, $(INCS))  $(shell root-config --libs) -lMLP -lMinuit -lTreePlayer -lTMVA -lTMVAGui -lXMLIO  -lMLP -lm  -g -o $@
	@echo "Done"

bin/MakeFriendTrees.o : src/MakeFriendTrees.C
	@echo -n "Building $@ ... "
	$(CXX) -c $(CCFLAGS) $<  $(addprefix -I, $(INCS))  -g -fPIC -o $@
	@echo "Done"

bin/MakeFriendTrees.so : bin/MakeFriendTrees.o
	@echo -n "Building $@ ... "
	$(CXX) -shared $(CCFLAGS) $<  $(addprefix -I, $(INCS))  $(shell root-config --libs) -lMLP -lMinuit -lTreePlayer -lTMVA -lTMVAGui -lXMLIO  -lMLP -lm  -g -o $@
	@echo "Done"

clean: 
	rm -f bin/*.o bin/TMVAClassification bin/MakeFriendTrees.so

