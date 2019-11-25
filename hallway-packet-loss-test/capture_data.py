#!/usr/bin/python3
import subprocess
import time

def get_ssid():
    iwconfig_output=subprocess.run(['iwconfig','wlan0'], stdout=subprocess.PIPE)
    iwconfig_output=iwconfig_output.stdout.decode()
    iwconfig_lines=iwconfig_output.split("\n")
    ssid=iwconfig_lines[1].strip().split()[-1]
    return ssid


def ping():
    try:
        ping_output=subprocess.run(['ping','-c','1','ahti.d.umn.edu'],timeout=0.15,stdout=subprocess.PIPE)
        ping_ms=ping_output.stdout.decode().split("\n")[1].split()[-2].split("=")[1]
    except:
        return "401"
    return ping_ms

last_time = time.time()
results = []
try:
    while True:
        time_res = time.time()
        ssid_res = get_ssid()
        ping_res = ping()
        print("%s,%s,%s" % (time_res, ssid_res, ping_res))
        results.append({'time': time_res, 'ssid': ssid_res, 'ping': ping_res})
        time_to_next_ping = last_time + 0.2 - time.time()
        if time_to_next_ping < 0:
            time_to_next_ping = 0
        last_time += .2
        time.sleep(time_to_next_ping)
except KeyboardInterrupt:
    pass

print("Exporting %s results..." % len(results))

import csv
filename=input('CSV File to write to:')
with open(filename+'.csv', 'w', newline='') as csvfile:
    fieldnames = ['time', 'ssid', 'ping']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        writer.writerow(result)
