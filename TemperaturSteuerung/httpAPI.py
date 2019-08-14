# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 09:17:31 2019

@author: Tiamo
"""

import requests

class httpAPI():
    def __init__(self, baseadress):
        self.baseadress = baseadress
    
    def GET_SP(self):
        pass
    
    def GET_PID(self):
        pass
    
    def GET_T(self):
        pass
    
    def POST_SP(self, SP):
        pass
        
    def POST_PID(self, PIDdict):
        print(self.baseadress + PIDdict)
    
    def POST_RESET(self):