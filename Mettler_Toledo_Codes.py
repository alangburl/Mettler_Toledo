import serial
import time
# from serial_interface import SerialInterface,SerialInterfaces,find_serial_interface_ports

class Mettler_Toledo():
    def __init__(self, com_port,debug=False):
        #get the command options
        self.commands=self._load_commands()
        self.debug=debug
        if not debug:
        #set up the comm port to read out data
            self.serial_device=serial.Serial(port=com_port,
                                          baudrate=9600,timeout=0.05)
            #wake the machine up 
            self.set_parameter('power_change', 1)
            serial_num=self.read_single_line('serial_number')
            model=self.read_single_line('model_number')
            data=self.read_single_line('device_data')
            print('Connected to MT:\nS/N: {}Model: {}Data: {}'.format(
                serial_num,model,data))
        else:
            print('Debug connected to serial port')
        #get the model and serial number from the device

    def _configure_commands(self,command,inputs=None):
        if inputs==None:
            cm='{}\r\n'.format(command)
            return bytes(cm,'ASCII')
        else:
            cm='{} {}\r\n'.format(command,inputs)
            return bytes(cm,'ASCII')
        
    def _load_commands(self):
        f=open('commands.cm','r')
        data=f.readlines()
        f.close()
        cmds={}
        for i in range(len(data)):
            if '#' in data[i]:
                curr=data[i].split(sep='#')[1].split(sep='\n')[0]
                cmds[curr]={}
            else:
                this_command=data[i].split(sep=',')
                if len(this_command)>2:
                    cmds[curr][this_command[0]]=[this_command[1]]+\
                    [int(i) for i in this_command[2::]]
                else:
                    cmds[curr][this_command[0]]=this_command[1].split(sep='\n')[0]
        return cmds
    
    def _write(self,command,inputs=None):
        #get the command structure
        cmd=self._configure_commands(command,inputs)
        if not self.debug:
            self.serial_device.write(cmd)
        else:
            print(cmd)
        #sleep a little bit before reading
        time.sleep(0.01)
        
    def _clear_buffer(self):
        if not self.debug:
            self.serial_device.flushInput()
            self.serial_device.flushOutput()
    def _abort(self):
        self._write(self.commands['read_commands']['abort'])
        self._clear_buffer()
        
    def set_parameter(self,command,value):
        write_params=self.commands['write_commands'][command]
        if type(value)!=int or value not in write_params:
            print('Parameter not valid acceptable values:')
            print(write_params)
        else:
            self._write(self.commands['write_commands'][command][0],value)
            response=self.serial_device.readline()
            return response.decode().replace('"','')
    
    def read_single_line(self,command=None,write_on=True):
        if write_on:
            self._clear_buffer()
            if command not in list(self.commands['read_commands'].keys()):
                print('Command not supported')
            else:
                self._write(self.commands['read_commands'][command])
        if not self.debug:
            data_out=self.serial_device.readline()
            self._clear_buffer()
            return data_out.decode().replace('"','')
    
    def read_continuous(self,start_command,**kwargs):
        if 'wait_time' in kwargs.keys():
            wait=kwargs['wait_time']
        else:
            wait=0.05
        self._clear_buffer()
        #tell the system to start the measurement
        self._write(self.commands['read_commands'][start_command])
        data=[]
        times=[]
        if 'run_time' in kwargs.keys():
            #get the initial start time
            start=time.time()
            ct=start
            while ct-start<kwargs['run_time']:
                ct=time.time()
                data.append(self.read_single_line(write_on=False))
                times.append(ct)
                time.sleep(0.05)
        elif 'number_samples' in kwargs.keys():
            start=time.time()
            for i in range(kwargs['number_samples']):
                data.append(self.read_single_line(write_on=False))
                times.append(time.time()-start)
                time.sleep(wait)
        self._abort()
        self._clear_buffer()
        return data, times
    
    def close_serial(self):
        #must be called at the end of a continous stream of 
        #when exiting the program
        if not self.debug:
            self.serial_device.close()
        else:
            print('Serial port closed')
            
if __name__ =='__main__':
    mt=Mettler_Toledo('COM4',False)
    single_read=mt.read_single_line('weight_immediate')
    print(single_read)
    # set_params=mt.set_parameter('open_draft', 1)
    # time.sleep(1)
    # mt.set_parameter('open_draft', 3)
    # time.sleep(1)
    # mt.set_parameter('open_draft',2)
    # time.sleep(2)
    # set_params=mt.set_parameter('open_draft', 0)
    [data,times]=mt.read_continuous('weight_immediate_repeat',number_samples=100)
    mt.set_parameter('power_change',0)
    mt.close_serial()
