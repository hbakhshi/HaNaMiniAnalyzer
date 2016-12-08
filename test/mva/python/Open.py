#!/usr/bin/env python

from ROOT import TMVA, gApplication
import sys

TMVA.Tools.Instance()
TMVA.gTools().TMVAWelcomeMessage()

TMVA.TMVAGui(sys.argv[1])
    
gApplication.Run() 
