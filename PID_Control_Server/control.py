import time
from PID import PID
from MAX31865 import max31865
from usbtmc import usbtmc


### Initialisation of Driver
instr =  usbtmc.Instrument(1155, 30016)


###Initialisation of Sensor
csPin = 8
misoPin = 9
mosiPin = 10
clkPin = 11
max = max31865.max31865(csPin,misoPin,mosiPin,clkPin)


### Initialisation of PID
P = 10
I = 0
D = 0
SP=20
last_cont = 0

myPID = PID()
myPID.set_PID([P,I,D])
myPID.set_SP(SP)

starttime=time.time()  
while True:
    temp = max.readTemp()
    cont,err = myPID.compute(temp)
    cont = round(cont, 2)
    if last_cont !=  cont:
        last_cont = cont
        instr.write("CH1:CURR "+str(cont))
        time.sleep(0.01)
        instr.write("CH2:CURR "+str(cont))
    time.sleep(1.- ((time.time() - starttime) % 1.))



