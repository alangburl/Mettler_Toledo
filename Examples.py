'''Notes:
    1.) if using a windows PC, you must identify the com port 
        that the mettler scale is communicating on. This may 
        eventually be automated, but for the first code iteration
        it is done manually

    2.) a full set of supported commands can be found in commands.cm, 
        a text readable file
        
    3.) this code is very much in beta testing and should be treated as such
        p.s trust, but verify the readings make sense
'''

import time
from Mettler_Toledo_Codes import Mettler_Toledo

#commection to the scale using COM5, identify on your system
#if trying to debug change the second argument to True
#this will connect to the scale and display the system information
#about the scale currently connected
mt=Mettler_Toledo('COM5',False)
#power on the scale
confirm=mt.set_parameter('power_change', 1)
#zero the scale for initial use
confirm_zero=mt.read_single_line('zero')
#read a single stable value
single_value=mt.read_single_line('stable_read')
#give the balance a couple seconds to make sure it read a stable value
time.sleep(2)
#read a single value regardless of stability
single_value_immediate=mt.read_single_line('weight_immediate')
time.sleep(0.5)
#get a continous stream of data from the system and the time of reading
#there may be slight time reading errors due to the speed of the serial
#port and how the time is determined. the error will be in <0.01 s. 
#The wait command of 0.045 s should be really not need to be changed as the 
#system is capable of ~23 Hz data collection
[weight,times]=mt.read_continuous('weight_immediate_repeat',
                                      number_samples=50,wait=0.045)

#power down the scale after the data is retrieved
mt.set_parameter('power_change', 0)
#disconnect from the scale and release the com port, this MUST be called at
#the end of any program to ensure the resource is released. If you get a
#connection error, this is likely the reason. You should try restart you
#python IDE or physically disconnecting from the balance
mt.close_serial()