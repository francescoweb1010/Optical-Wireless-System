import pandas as pd
import numpy as np
import os
import sys
from time import sleep
from Levenshtein import distance as levenshtein_distance



print("---------- Optical Wireless System Demo ----------")
print("---------- Francesco Russo, Michele Cernigliaro, spring semester 2020")
print("---------- Demo for Smart Environments Course @LaSapienza (Msc Data Science)")
print("---------- Starting in 2 seconds")

sleep(2)

if len(sys.argv) > 2:
    print('You have specified too many arguments')
    sys.exit()

file_path = sys.argv[1]

print('loading log file from: {}' .format(file_path))

skiprows=30
df = pd.read_csv(file_path, sep=';', header=None, skiprows=skiprows)
df.columns = ['t', 'y']


print('loaded')

print("starting the real-time algorithm")

millis = 200
print("parameters: timedelta = {}" .format(millis))

import numpy as np

rest_state = True
configuration_state = False
loiter_state = False
receiving_state = False
conclusion_state = False

zero_setting_time = df["t"][0] + 1000
zero_list = df[df["t"] <= zero_setting_time]
nominal_zero = np.mean(zero_list)["y"]
zero_thr = 1.2*nominal_zero

df_real_time = df[df["t"] > zero_setting_time]
df_real_time.reset_index(inplace = True)
ratio = 0.5
cumulative_mean = nominal_zero
loiter_t = 2000
signal_delta = millis

message = ""
final_message = ""

debug = True

for i in range(0, len(df_real_time)):
    
    sleep(20/1000)

    y = df_real_time["y"][i]
    t = df_real_time["t"][i]
    
    if rest_state:
        if debug: print("rest state: y={}, t={}" .format(y, t))
        if y > zero_thr:
            thr = zero_thr
            configuration_state = True
            rest_state = False

    if configuration_state:
        if debug: print("configuration state: y={:.2f}, t={}, thr={:.2f}, cumulative_mean={:.2f}".format(y, t, round(thr,3), round(cumulative_mean,3)))
        if y < thr:
            loiter_state = True
            configuration_state = False
            loiter_start = t
        if configuration_state:
            cumulative_mean = (y + cumulative_mean)/2
            thr = cumulative_mean*ratio
        
    if loiter_state:
        if debug: print("loiter state: y={}, t={}" .format(y, t))
        if t >= loiter_start + loiter_t:
            loiter_state = False
            receiving_state = True
            t_0 = t
            cnt = 1
            n_peaks = 0
            n_gaps = 0
    
    if receiving_state:
        if debug: print("receiving state: y={}, t={}, t_0={}" .format(y, t, t_0))
        if y >= thr:
            n_peaks += 1
        else:
            n_gaps += 1
        if t >= t_0 + cnt*signal_delta:
            print("\tn_peaks: {}, n_gaps: {}, actual_time_slot (bin): {}" .format(n_peaks, n_gaps, cnt))
            cnt += 1
            if n_peaks >= n_gaps:
                message = message + "1"
            else:
                if message[-10:] == "1111111111" or message[-10:] == "0000000000":
                    message = message[:-10]
                    receiving_state = False
                    conclusion_state = True
                    break
                message = message + "0"
            n_peaks = 0
            n_gaps = 0
    
if conclusion_state:
    print("conclusion state")
    for idx in range(len(message)//4):
        n1 = 0; n0 = 0
        for bit in message[idx*4:(idx+1)*4]:
            if bit == "1":
                n1 += 1
            else:
                n0 += 1
        if n1 >= n0:
            final_message = final_message + "1"
        else:
            final_message = final_message + "0"
            
    rest_state = True


print("------------------ END TRANSMISSION ------------------")
print("received encoded message: {}".format(message))
print("original encoded message: 11110000111100001111000011110000111100001111")


print("final message:    {}" .format(final_message))
print("original message: 10101010101")
print("Levenshtein distance: {}" .format(levenshtein_distance("10101010101", final_message)))
