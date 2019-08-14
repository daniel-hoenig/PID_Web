### Skript to Set_up the Control-Server as well as recording the data.
### The Server and the Data recording routine will both run in thei own seperate process making the regular scheduling of data capturing
### easily independent from user interaction.
import time
import signal
import sys
import math
import RPi.GPIO as GPIO
import saveconfig
from PID import PID
from MAX31865 import max31865
from usbtmc import usbtmc
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, flash, jsonify, request
from forms import PIDForm, TemperatureForm, BiasForm, LimitForm
from multiprocessing import Process, Pipe, Manager
from bokeh import plotting as plt
from bokeh.models.sources import AjaxDataSource
from bokeh.embed import components
from bokeh.models import Label
from bokeh.resources import INLINE

### Setting up Flask
app = Flask(__name__)
app.secret_key='safe-password'
bootstrap=Bootstrap(app)



    
### Data Capturing routine
def record_loop():
    ''' function for reading Data from sensors and PID control'''

    ### Initialisation of Driver
    instconnect=False
    while instconnect == False:
        try:
            instr =  usbtmc.Instrument(1155, 30016) #find the Instrument you use with lsusb and insert its adress here (convert from hexadecimal)
            time.sleep(10)
            break
        except:
            time.sleep(0.5)
            print("failed to open Instrument")
        
    
    instr.write("CH1:CURR 0")
    time.sleep(0.1)
    instr.write("CH2:CURR 0")
    time.sleep(0.1)
    instr.write("OUTP CH1, ON")
    time.sleep(0.1)
    instr.write("OUTP CH2, ON")

    ###CatchShutdown event
    def shutdown(signum,stack):
        instr.write("OUTP CH1, OFF")
        time.sleep(0.1)
        instr.write("OUTP CH2, OFF")
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGHUP,signal.SIG_IGN)
    ###Initialisation of Sensor
    csPin = 8
    misoPin = 9
    mosiPin = 10
    clkPin = 11
    max = max31865.max31865(csPin,misoPin,mosiPin,clkPin)


    ### Initialisation of PID
    myPID = PID()
    

    ### Initialising Control Variable, Time, and Temperature
    last_cont = 0
    starttime=time.time()
    temp = max.readTemp()
    tempcount=0
    
    
    while True:
        # Recording Temperature and manually smoothing out recordingerrors.
        newtemp = max.readTemp()
        
        if abs(newtemp-temp) < 1:
            temp = newtemp
            tempcount = 0
        else:
            if tempcount == 0:
                tempcount = 1

            else:
                temp = newtemp
                tempcount == 0
                
        Tempa.value = temp
        
        
        ### Checking if any of the PID parameters got changed via the website
        if pid_output.poll()== True:
            PIDlist = pid_output.recv()
            myPID.set_PID(PIDlist)
        if bias_out.poll()== True:
            myPID.set_bias(bias_out.recv())
        if sp_out.poll()== True:
            myPID.set_SP(sp_out.recv())
        if bounds_out.poll()== True:
            myPID.set_bounds(bounds_out.recv())
        
        ### Calculating the controller Variable
        cont,err = myPID.compute(temp)
        cont = round(cont, 2)
        
        #print(myPID.P, myPID.SP, myPID.bias, myPID.upb,cont)
        
        ### Checking if the controller Variable has changed and updating the Controller
        if last_cont !=  cont:
            last_cont = cont
            instr.write("CH1:CURR "+str(cont))
            time.sleep(0.01)
            instr.write("CH2:CURR "+str(cont))
            #print(cont)
        time.sleep(1.- ((time.time() - starttime) % 1.))

 
### Setting the control-server up with Flask

### FLASK APP 

@app.route('/')
def index():
    return 'Index Page'

###uploading data
x = 0
z= list(range(-299,1))

@app.route("/data/", methods=['POST'])
def data():
    global z
    ylist.append(Tempa.value)
    ylist.pop(0)
    return jsonify(x=z, y=ylist)

### Page for setting up the PI
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    PIDlist,SP,Bias,BoundList=saveconfig.load_PID('config.ini')
    ### Reading out the Forms
    class PIDSettings(object):
        PID_list,SP,Bias,BoundList=saveconfig.load_PID('config.ini')
        P=PID_list[0]
        I=PID_list[1]
        D=PID_list[2]
        lolim=BoundList[0]
        uplim=BoundList[1]
        
    form1 = PIDForm(obj=PIDSettings)
    form2 = BiasForm(obj=PIDSettings)
    form3 = TemperatureForm(obj=PIDSettings)
    form4 = LimitForm(obj=PIDSettings)
    if form1.submit.data and form1.validate():
        PIDlist = [form1.P.data, form1.I.data,form1.D.data]
        pid_input.send(PIDlist)
        #flash('PID set'+ str(PIDlist))
    if form2.submit.data and form2.validate():
        Bias = form2.Bias.data
        bias_in.send(Bias)
        #flash('Offset set'+ str(Bias))
    if form3.submit.data and form3.validate(): 
        SP = form3.SP.data
        sp_in.send(SP)
        #flash('Temperature Set'+ str(SP))
    if form4.submit.data and form4.validate():
        BoundList = [form4.lolim.data, form4.uplim.data]
        bounds_in.send(BoundList)
        #flash('Limits set'+ str(BoundList))
        
    plot=make_ajax_plot()
    
    saveconfig.save_PID(PIDlist,SP,Bias,BoundList,'config.ini')
    
    return render_template('setup.html', title = 'Setup', form1 = form1,
                            form2 = form2, form3 = form3, form4 = form4, plot=plot)


def make_ajax_plot():
    streaming = True
    source = AjaxDataSource(data_url=request.url_root + 'data/',
                            polling_interval=1000, mode='replace')
    plot = plt.figure(plot_height=300,sizing_mode='scale_width')
    plot.line('x', 'y', source=source, line_width=4)
 
    
    
    script, div = components(plot)
    return script, div




### Actual Program
if __name__ == "__main__":
    #Setup Pipes to communicate between the processes
    pid_output, pid_input = Pipe()
    bias_out, bias_in = Pipe()
    sp_out, sp_in = Pipe()
    bounds_out, bounds_in = Pipe()
    manager=Manager()
    Tempa=manager.Value(float,0)
    
    #Starting controller as Process
    p = Process(target=record_loop) 
    p.start()
    #Running Flask Server
    ylist= [Tempa.value]*300
    app.run(host='0.0.0.0')
    p.join()