# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import process_log as pl
import utility as u
import os
import time
import shutil
import errno
import glob

import process_data as pd
import Output as out

#path="data/p3d_arcsphere_results.log"
#path="data/p3d_contemporary-bathroom_results.log"
##path="data/p3d_caustic-view0_results.log"
path="data/p3d_crown_results.log"
#path="data/p3d_indirect_results.log"
out.showResult(path)
out.show_thresholdImage(path,"E:/image",True)
