#!/usr/bin/python3
import sys
import csv
from bokeh.plotting import figure, output_file, save
import numpy as np

for filename in sys.argv[1:]:
    print("Processing %s" % filename)
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    output_file(filename+'.html')
    p = figure(title=input("Title: "), x_axis_label='time', y_axis_label='latency')
    x = [float(result['time']) for result in data]
    x = np.array(x, dtype='i8').view('datetime64[ms]').tolist() # https://stackoverflow.com/a/41883851
    y = [float(result['ping']) for result in data]
    p.square(x, y, size=5, color="red", alpha=0.5)
    save(p)
