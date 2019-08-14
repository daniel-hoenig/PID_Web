import saveconfig

class PID:
    "Class for performing the PID calculations"
    ### strongly inspired by the PID library for arduino from brett beauregard (bretbeauregard.com)
    
    def __init__(self,configfile='config.ini',use_bounds=True,sampletime=1000):
        ##
        PID_list,SP,Bias,BoundList=saveconfig.load_PID(configfile)
        self.P = PID_list[0] #Proportional Gain
        self.I = PID_list[1] #Integral Gain
        self.D = PID_list[2] # Differential Gain
        self.SP = SP # Setpoint
        self.use_bounds = use_bounds  #enabling/disabling limits for control variable should be enabled
        self.upb = BoundList[1] # upper boundary for control variable
        self.lob = BoundList[0] #lower boundary for control variable
        self.sample_time = sampletime #sample time in milliseconds
        self.bias = Bias #constant bias for the control variable
                
        self.ierr = 0. #initialisation of integral error
        self.lastPV = 0. #initialisation for differential part
        
    
    def set_PID(self,PIDlist): 
        " routine for setting the PID parameters "
        self.P = PIDlist[0]
        self.I = PIDlist[1]
        self.D = PIDlist[2]
    
    def set_SP(self,SP):
        " routine for setting the desired Setpoint"
        self.SP= SP
        
    def set_bias(self,bias):
        " routine for setting the PID offset"
        self.bias= bias
    
    
    
    def set_bounds(self,boundlist):
        "routine for setting the bounds for the control variable"
        self.upb = boundlist[1]
        self.lob = boundlist[0]
    
    def set_from_config(self,configfile):
        "routine to set up the PID-Parameters from a config file"
        PID_list,SP,Bias,BoundList=saveconfig.load_PID(configfile)
        
        
    
    def compute(self,PV):
        "routine to calculate the control variable"
        
        err = self.SP-PV  #calculating proportional error
        self.ierr += (self.I*err) #calculating Integral part
        
        if self.use_bounds == True:
            self.ierr = max(self.lob,min(self.upb,self.ierr)) #clamping the integral part to avoid windup 
        
        derr = self.D*(PV-self.lastPV) #calculating Differential part
        
        cont = self.bias+self.P*err+self.ierr-derr #calculating the control  variable
        
        if self.use_bounds == True:
            cont = max(self.lob,min(self.upb,cont)) #limiting output
        
        return cont,err
        
        
        
    

