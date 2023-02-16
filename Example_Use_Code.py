import numpy as np
import matplotlib.pyplot as plt
import time
from Mettler_Toledo_Codes import Mettler_Toledo

mt=Mettler_Toledo('COM5',False)
#power on the scale
mt.set_parameter('power_change', 1)
#open the top draft shield to 75%
# res=mt.set_parameter('draft_opening_width', 50)
# resp=mt.set_parameter('open_draft', 3)
#zero the scale
# tare_val=mt.read_single_line('tare')
# time.sleep(2)
[weight,times]=mt.read_continuous('weight_immediate_repeat',
                                      number_samples=50,wait=0.045)
# x=input('Waiting for any key to continue')
#collect 1000 samples for with no air flow
# time.sleep(1)
# [no_flow,no_times]=mt.read_continuous('weight_immediate_repeat',
#                                       number_samples=50,wait=0.042)
# # split the no flow and plot it
# no_flow_=[]
# no_times_=[]
# for i in range(len(no_flow)):
#     try:
#         no_flow_.append(float(no_flow[i].split(sep=' ')[-3]))
#         no_times_.append(no_times[i])
#     except:
#         print(i)

# plt.plot(no_times_,no_flow_)
# print('switch to flow')
# time.sleep(1)
#wait  until the gas flow is turned on to begin sampling again
# wait=input('Enter any key to continue')
# [with_flow,with_times]=mt.read_continuous('weight_immediate_repeat', 
#                                           number_samples=50,
#                                           wait=0.042)
# with_flow_=[]
# with_times_=[]
# for i in range(len(with_flow)):
#     try:
#         with_flow_.append(float(with_flow[i].split(sep=' ')[-3]))
#         with_times_.append(with_times[i])
#     except:
#         print(i)
# plt.plot(with_times_,with_flow_)
# plt.show()
mt.set_parameter('power_change', 0)
mt.close_serial()