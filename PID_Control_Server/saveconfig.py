import configparser
# Basic functions to read and write to the configfile.


def load_PID(configfile):
    config = configparser.ConfigParser()
    config.read(configfile)
    PID = config['PID']
    PID_list = [PID.getfloat('P'),PID.getfloat('I'),PID.getfloat('D')]
    SP = PID.getfloat('SP')
    Bias = PID.getfloat('Bias')
    BoundList = [PID.getfloat('lob'),PID.getfloat('upb')]
    return PID_list,SP,Bias,BoundList
    


def save_PID(PID_list,SP,bias,Boundlist,configfile):
    config = configparser.ConfigParser()
    config.read(configfile)
    PID=config['PID']
    PID['P']=str(PID_list[0])
    PID['I']=str(PID_list[1])
    PID['D']=str(PID_list[2])
    PID['SP']=str(SP)
    PID['Bias']=str(bias)
    PID['upb']=str(Boundlist[1])
    PID['lob']=str(Boundlist[0])
    with open(configfile, 'w') as writefile:
        config.write(writefile)




    