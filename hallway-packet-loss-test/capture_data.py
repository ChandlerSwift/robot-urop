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
        ping_output=subprocess.run(['ping','-c','1','-W','0.1','ahti.d.umn.edu'],timeout=0.4,stdout=subprocess.PIPE)
        ping_ms=ping_output.stdout.decode().split("\n")[1].split()[-2].split("=")[1]
    except:
        return "timeout"
    return ping_ms


while True:
    print("%s,%s,%s" % (time.time(), get_ssid(), ping()))
    time.sleep(0.1)
