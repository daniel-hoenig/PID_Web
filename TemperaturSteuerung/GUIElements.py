# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 17:13:14 2019

@author: Tiamo
"""

from PyQt5.QtWidgets import (QLabel, QDoubleSpinBox,
                             QGroupBox, QFormLayout)
from PyQt5.QtCore import pyqtSignal,QTimer
import pyqtgraph as pg
import random



class PIDGroup(QGroupBox):
    '''Subgroup of the GUI containg all the PID parameters'''
    
    ### Defining Signals to communicate with main GUI 
    ###in which PID group will be included
    
    p_changed = pyqtSignal(float)
    i_changed = pyqtSignal(float)
    d_changed = pyqtSignal(float)
    ul_changed = pyqtSignal(float)
    ll_changed = pyqtSignal(float)
    

    def __init__(self, propdict):
        
        super().__init__("PID Control")
        
        
        self.createSpinboxes(propdict)
        GroupLayout = QFormLayout()
        GroupLayout.addRow(QLabel("P:"),self.PSB)
        GroupLayout.addRow(QLabel("I:"),self.ISB)
        GroupLayout.addRow(QLabel("D:"),self.DSB)
        GroupLayout.addRow(QLabel("Upper Limit"),self.UlimSB)
        GroupLayout.addRow(QLabel("Lower Limit"),self.LlimSB)
        
        self.setLayout(GroupLayout)

        
    def createSpinboxes(self, propdict):
        
        self.PSB = QDoubleSpinBox(value = propdict["P"], decimals = 2)
        self.PSB.setObjectName("PSB")
        self.PSB.valueChanged.connect(self.p_changed)
        
        self.ISB = QDoubleSpinBox(value = propdict["I"], decimals = 2)
        self.ISB.setObjectName("ISB")
        self.ISB.valueChanged.connect(self.i_changed)
        
        self.DSB = QDoubleSpinBox(value = propdict["D"], decimals = 2)
        self.DSB.setObjectName("DSB")
        self.DSB.valueChanged.connect(self.d_changed)
        
        self.UlimSB = QDoubleSpinBox(value = propdict["Ulim"],
                                     decimals = 2, suffix = "A")
        self.UlimSB.setObjectName("UlimSB")
        self.UlimSB.valueChanged.connect(self.ul_changed)
        
        self.LlimSB = QDoubleSpinBox(value = propdict["Llim"],
                                     decimals = 2, suffix = "A")
        self.LlimSB.setObjectName("LlimSB")
        self.LlimSB.valueChanged.connect(self.ll_changed)
        
        

class SPGroup(QGroupBox):
    '''Subgroup of the GUI conatining the desired Temperature.
        Only for style!'''
    
    sp_changed = pyqtSignal(float)
    
    def __init__(self, propdict):
        super().__init__("Setpoint:")
        
        self.createSpinboxes(propdict)
        
        GroupLayout = QFormLayout()
        GroupLayout.addRow(QLabel("Setpoint"),self.SPSB)
        self.setLayout(GroupLayout)
        
    def createSpinboxes(self,propdict):
       
        self.SPSB =  QDoubleSpinBox(value = propdict["SP"], decimals=2,
                                   suffix = "°C")
        self.SPSB.valueChanged.connect(self.sp_changed)



class Plotter(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.data = [0]
        self.trace = self.getPlotItem().plot()
        
