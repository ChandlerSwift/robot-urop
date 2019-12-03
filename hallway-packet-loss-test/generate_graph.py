#!/usr/bin/python3
import sys
import csv
from bokeh.plotting import figure, output_file, save
from bokeh.models import BoxAnnotation
import numpy as np

for filename in sys.argv[1:]:
    print("Processing %s" % filename)
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    output_file(filename+'.html')
    p = figure(title=input("Title: "), x_axis_type='datetime', y_axis_label='latency')
    x = [float(result['time']) * 1000 for result in data]
    # TODO: unnecessary? :
    #x = np.array(x, dtype='i8').view('datetime64[s]').tolist() # https://stackoverflow.com/a/41883851
    y = [float(result['ping']) for result in data]
    p.square(x, y, size=5, color="red", alpha=0.5)

    start_time = None
    connected = False
    prev_datum = {'ssid': 'dBm'} # Hackety hack hack
    for datum in data:
        if datum['ssid'] != prev_datum['ssid']: # Connection status changed
            if datum['ssid'][2] == ':': # There's a colon at position 2, meaning it's a MAC address
                print('connected')
                connected = True
                start_time = float(datum['time']) * 1000
            else:
                connected = False
                end_time = float(datum['time']) * 1000
                print("Connection lost to %s, connected for %s seconds." % (prev_datum['ssid'], (end_time - start_time) / 1000))
                connection_box = BoxAnnotation(left=start_time, right=end_time, fill_color='green', fill_alpha=0.1)
                p.add_layout(connection_box)
        prev_datum = datum

    if connected: # If the graph ended with a connection in place?
        print(start_time)
        end_time = float(prev_datum['time']) * 1000
        print("end time: %s, start time: %s" % (end_time, start_time))
        print("Run ended, disconnected from %s, connected for %s seconds." % (prev_datum['ssid'], (end_time - start_time) / 1000))
        connection_box = BoxAnnotation(left=start_time, right=end_time, fill_color='green', fill_alpha=0.1)
        p.add_layout(connection_box)

    save(p)
