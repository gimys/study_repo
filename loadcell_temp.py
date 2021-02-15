import serial
import sys
from collections import defaultdict

import statistics

import time

ser = serial.Serial ("/dev/serial0")    #Open named port 
ser.baudrate = 57600                     #Set baud rate to 57600
ser.timeout = None




data = str(ser.read(12))

channel_name = 'A'
slice_index = data.index(channel_name)+1


def find_sensor_list(check_time = 3):
    sensor_list_dict = {}
    end_time = time.time() + check_time
    
    while True:
        data = ser.read(12)
        data = str(data)
        sensor_name = data[slice_index-3:slice_index]
        sensor_list_dict[sensor_name] = 'check'
        
        if time.time() > end_time:
            break
    
    return sensor_list_dict


def weight_measurement(time_delay=5):
    sensor_old_data_dict = defaultdict(lambda : list())
    end_time = time.time() + time_delay

    while True:
        data = ser.read(12)
        data = str(data)
        sensor_name = data[slice_index-3:slice_index]
        sensor_value = data[slice_index:slice_index+6]
        sensor_old_data_dict[sensor_name].append(int(sensor_value))
        
        if time.time() > end_time:
            break
    
    weight_measurement_dict = {}
    for sensor in sensor_old_data_dict.keys():
        weight_measurement_dict[sensor] = statistics.mean(sensor_old_data_dict[sensor])
        
    return weight_measurement_dict

def calculation_coefficient(tare_dict, gram=0):
    weight_dict = weight_measurement()
    calc_dict = {}
    
    for sensor in tare_dict.keys():
        calc_dict[sensor] = gram/(weight_dict[sensor] - tare_dict[sensor])
    return calc_dict
        

def mean_coefficient(coefficient_list):
    
    for co in coefficient_list:
        if co == coefficient_list[0]:
            mean_coefficient_dict = co
        else:
            mean_coefficient_dict = {key : mean_coefficient_dict[key] + co[key] for key in mean_coefficient_dict.keys()}
    
    mean_coefficient_dict = {key : mean_coefficient_dict[key]/len(coefficient_list) for key in mean_coefficient_dict.keys()}
    
    return mean_coefficient_dict


## tare setting
tare_dict = weight_measurement()
print(tare_dict)




co100 = calculation_coefficient(tare_dict, gram=100)
print(co100)
co50 = calculation_coefficient(tare_dict, gram=50)
print(co50)
co20 = calculation_coefficient(tare_dict, gram=20)
print(co20)
co10 = calculation_coefficient(tare_dict, gram=10)
print(co10)
co5 = calculation_coefficient(tare_dict, gram=5)
print(co5)




coefficient_list = [co100, co50, co20, co10, co5]

mean_coefficient_dict = mean_coefficient(coefficient_list)



coefficient_list = [co100, co50, co20, co10]

mean_coefficient_dict = mean_coefficient(coefficient_list)

## tare_dict
## mean_coefficient_dict



mean_coefficient_dict = mean_coefficient_dict
tare_dict = weight_measurement()
tare_dict


sensor_data_dict = defaultdict(lambda : 0.0)

while True:
    
    try :
        data = ser.read(12)
        data = str(data)
        sensor_name = data[slice_index-3:slice_index]
        sensor_value = data[slice_index:slice_index+6]
        
        ## for passing irregular sensor data
        #### if channel_name in data:
        if channel_name in data:
            sensor_data_dict[sensor_name] = (int(sensor_value) - tare_dict[sensor_name])*mean_coefficient_dict[sensor_name]

            print('01A :', '%.1f |' % abs(sensor_data_dict['01A']),
                  '02A :', '%.1f |' % abs(sensor_data_dict['02A']),
                  '03A :', '%.1f |' % abs(sensor_data_dict['03A']),
                  '------------------'
                  '01A :', '%d g |' % abs(round(sensor_data_dict['01A'], 0)),
                  '02A :', '%d g |' % abs(round(sensor_data_dict['02A'], 0)),
                  '03A :', '%d g |' % abs(round(sensor_data_dict['03A'], 0)),)
        else:
            pass
        
        
    except KeyboardInterrupt:
        print('cancel')
        break







'''
def weight_sensor_d(time_delay=10, gram = None):
    if type(gram) != int:
        print('Set the stuff weight(int)')
    
    elif type(gram) == int:
        sensor_old_data_dict = defaultdict(lambda : list())
        end_time = time.time() + time_delay
        
        while True:
            data = ser.read(12)
            data = str(data)
            sensor_name = data[slice_index-3:slice_index]
            sensor_value = data[slice_index:slice_index+6]
            sensor_old_data_dict[sensor_name].append(int(sensor_value))
        
        if time.time() > end_time:
            break
        
        weight_sensor_data = {}
        for sensor in sensor_tare_dict.keys():
            weight_sensor_data[sensor] = statistics.mean(sensor_old_data_dict[sensor])
'''        
    
    
    
    
'''
print_value_dict = defaultdict(lambda : 'Check the sensor.')
while True:
    
    try :
        data = ser.read(12)
        data = str(data)
        sensor_name = data[slice_index-3:slice_index]
        sensor_value = data[slice_index:slice_index+6]
        
        ## for passing irregular sensor data
        #### if channel_name in data:
        if channel_name in data:
            print_value_dict[sensor_name] = (float(sensor_value)-tare_dict[sensor_name])*mean_coefficient_dict[sensor_name]
            
            
            print('01A :', print_value_dict['01A'],
                  '02A :', print_value_dict['02A'],
                  '03A :', print_value_dict['03A'])
            
            old_data_dict[sensor_name].pop(0)
            old_data_dict[sensor_name].append(sensor_value)
            print(old_data_dict['03A'][:3])
            
        else:
            pass
        
        
    except KeyboardInterrupt:
        print('cancel')
        break
'''



