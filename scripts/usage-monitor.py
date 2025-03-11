#!/usr/bin/python

import time
import json
import psutil
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--save', type=bool, nargs='?', const=True)
parser.add_argument('-o', '--open', type=str, default='')
args = parser.parse_args()

cpuUsage = []
ramUsage = []
timestamps = []

if args.open:
    with open(args.open, 'r') as f:
        data = json.load(f)
else:
    duration = 60
    interval = 1
    startTime = time.time()

    for i in range(duration):
        cpu = psutil.cpu_percent(interval=interval)
        ram = psutil.virtual_memory().percent
        elapsedTime = time.time() - startTime

        cpuUsage.append(cpu)
        ramUsage.append(ram)
        timestamps.append(elapsedTime)

        print(f"{elapsedTime:.1f} sec - CPU: {cpu}%, RAM: {ram}%")

    data = {
        'cpuUsage': cpuUsage,
        'ramUsage': ramUsage,
        'timestamps': timestamps,
    }

if args.save:
    with open('cpu_ram_usage.json', 'w') as f:
        json.dump(data, f)

    exit(0)

plt.figure(figsize=(10, 5))
plt.plot(data['timestamps'], data['cpuUsage'], label='Загрузка CPU (%)', color='r')
plt.plot(data['timestamps'], data['ramUsage'], label='Загрузка RAM (%)', color='b')
plt.xlabel('Время (секунды)')
plt.ylabel('Загрузка (%)')
plt.title('Загрузка CPU и RAM')
plt.legend()
plt.grid()
plt.show()
