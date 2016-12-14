#!/usr/bin/env python

'''
switcher for network evaluation scheme
return an object depending on the flag "quality_method" in config.py
'''

import sys
import config as cf

class Quality:

    def __new__(cls):
        if cf.quality_method == 1: # use map equation for communities' quality estimation
            import mapequation as mp
            new_cls = mp.Map
        elif cf.quality_method == 2: # use modularity for communities' quality estimation
            pass # not implemented yet
        else:
            print("error: in config.py, undefined number of quality_method was selected.")
            sys.exit(1)

        instance = super(Quality, new_cls).__new__(new_cls)
        if new_cls != cls:
            instance.__init__

        return instance