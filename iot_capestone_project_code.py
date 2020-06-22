# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 22:04:02 2019

@author: ARCHIT
"""

"""Code for Capestone project"""

import email_config, json, time, ad_conf, math, statistics
from boltiot import Email, Bolt

min_limit = 0
max_limit = 41

def compute_bounds(history_data, frame_size, factor):
    if len(history_data)<frame_size:
        return None
    
    if len(history_data)>frame_size:
        del history_data[0:len(history_data)-frame_size]
        
    Mn=statistics.mean(history_data)
    Variance=0
    
    for data in history_data:
        Variance+= math.pow((data-Mn),2)
        
    Zn= factor* math.sqrt(Variance/frame_size)
    High_bound=history_data[frame_size-1]+Zn
    Low_bound= history_data[frame_size-1]-Zn
    return [High_bound, Low_bound]


mybolt= Bolt(ad_conf.API_KEY, ad_conf.DEVICE_ID)
mybolt= Bolt(email_config.API_KEY, email_config.DEVICE_ID)
mailer= Email(email_config.MAILGUN_API_KEY, email_config.SANDBOX_URL,email_config.SENDER_EMAIL, email_config.RECIPIENT_EMAIL)
history_data=[]


while True: 
    response = mybolt.analogRead('A0') 
    data = json.loads(response) 
    print (data['value'])
    
    try: 
        sensor_value = int(data['value']) 
        print ("temperature: ",((sensor_value*100)/1024))
        
        if sensor_value > max_limit or sensor_value < min_limit:
            response = mailer.send_email("Temperature Alert", "The Current temperature is " +str(sensor_value*100/1024))
            print("mail sent\n")
            
    except Exception as e: 
        print ("Error 1",e)
        continue
    
    bound = compute_bounds(history_data,ad_config.FRAME_SIZE,ad_config.MUL_FACTOR)
    
    if not bound:
        
        required_data_count=conf.FRAME_SIZE-len(history_data)
        print("Need ",required_data_count," more data points to calculate Z-score")
        history_data.append(int(data['value']))
        time.sleep(10)
        continue
    
    try:
        
        if sensor_value > bound[0] :
            print ("SOMEONE HAS OPENED THE FRIDGE DOOR")
            
        elif sensor_value < bound[1]:
            print ("SOMEONE HAS OPENED THE FRIDGE DOOR")
            
        history_data.append(sensor_value)
            
    except Exception as e:
        print ("Error 2",e)
        
    time.sleep(10)

    
    
    
    
    
    
    
    