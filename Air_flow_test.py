import numpy as np
import matplotlib.pyplot as plt
import time
from Mettler_Toledo_Codes import Mettler_Toledo

mt=Mettler_Toledo('COM4',False)
#open the top draft shield to 75%
# res=mt.set_parameter('draft_opening_width', 75)
# resp=mt.set_parameter('open_draft', 3)
#zero the scale
# tare_val=mt.read_single_line('tare')
x=input('Waiting for any key to continue')
#collect 1000 samples for with no air flow
[no_flow,no_times]=mt.read_continuous('weight_immediate_repeat',
                                      number_samples=50,wait=0.042)
# split the no flow and plot it
no_flow_=[]
no_times_=[]
for i in range(len(no_flow)):
    try:
        no_flow_.append(no_flow[i].split(sep=' ')[-2])
        no_times_.append(no_times[i])
    except:
        print(i)

plt.plot(no_times_,no_flow_)

#wait  until the gas flow is turned on to begin sampling again
wait=input('Enter any key to continue')
[with_flow,with_times]=mt.read_continuous('weight_immediate_repeat', 
                                          number_samples=50,
                                          wait=0.042)
with_flow_=[]
with_times_=[]
for i in range(len(with_flow)):
    try:
        with_flow_.append(with_flow[i].split(sep=' ')[-2])
        with_times_.append(with_times[i])
    except:
        print(i)
plt.plot(with_times_,with_flow_)
plt.show()
mt.close_serial()