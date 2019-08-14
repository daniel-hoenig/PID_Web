# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 16:34:49 2019

@author: Tiamo
"""

import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QHBoxLayout,
                             QLabel, QLCDNumber, QDoubleSpinBox)
from PyQt5.QtCore import QTimer
from GUIElements import PIDGroup, SPGroup, Plotter
import random

class ClientView(QWidget):
    
    def __init__(self):
        super().__init__()
        self.propdict = {"SP":20, "P": 1, "I": 0.2, "D": 0.5, "Ulim": 20, "Llim":0}
        self.initUI()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_update_trace)
        self.timer.setInterval(200)
        self.timer.start()
    
    def initUI(self):
        self.setWindowTitle("Temperature Controller")
        self.setGeometry(200,200,600,300)
        self.show()
        
        self.PIDgroup = PIDGroup(self.propdict)
        self.PIDgroup.p_changed.connect(self.on_p_changed)
        self.PIDgroup.i_changed.connect(self.on_i_changed)
        self.PIDgroup.d_changed.connect(self.on_d_changed)
        self.PIDgroup.ul_changed.connect(self.on_ul_changed)
        self.PIDgroup.ll_changed.connect(self.on_ll_changed)
        
        self.SPgroup = SPGroup(self.propdict)
        self.SPgroup.sp_changed.connect(self.on_sp_changed)
        
        self.TempLabel = QLabel("Current Temperature:")
        self.TempDigit = QLCDNumber()
        self.TempDigit.setSegmentStyle(QLCDNumber.Flat)
        self.TempDigit.setDigitCount(4)
        
        self.PlotView = Plotter()
        
        TempBox = QHBoxLayout()
        TempBox.addStretch(1)
        TempBox.addWidget(self.TempLabel)
        TempBox.addWidget(self.TempDigit)
        
        lVbox = QVBoxLayout()
        lVbox.addWidget(self.SPgroup)
        lVbox.addWidget(self.PIDgroup)
        
        rVbox = QVBoxLayout()
        rVbox.addLayout(TempBox)
        rVbox.addWidget(self.PlotView)

        
        hbox = QHBoxLayout()
        hbox.addLayout(lVbox)
        hbox.addLayout(rVbox)
        
        self.setLayout(hbox)
        

    def on_p_changed(self,val):
        self.propdict["P"] = val
        print (self.propdict)
    
    def on_i_changed(self,val):
        self.propdict["I"] = val
        print (self.propdict)
    
    def on_d_changed(self,val):
        self.propdict["D"] = val
        print (self.propdict)
        
    def on_sp_changed(self,val):
        self.propdict["SP"] = val
        print (self.propdict)
    
    def on_ul_changed(self,val):
        self.propdict["Ulim"] = val
        print (self.propdict)
    
    def on_ll_changed(self,val):
        self.propdict["Llim"] = val
        print (self.propdict)
    
    def on_update_trace(self):
        a = self.PlotView.data[-1]+0.2*(0.5-random.random())
        self.PlotView.data.append(a)
        self.PlotView.trace.setData(self.PlotView.data)
        self.TempDigit.display(a)


app = QApplication(sys.argv)
foo = ClientView()
sys.exit(app.exec_())
    
    