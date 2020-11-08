#!/usr/bin/python3
import os
import time
from datetime import datetime

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import memory_profiler


log_path = os.path.join(os.sep, "home", "pi", "weather_log.csv")

print("Running:{}".format(os.path.abspath(__file__)))

mem1 = memory_profiler.memory_usage()
t1 = time.time()

history=-10000

# function that filters vowels
def filterblank(input_list):
    if input_list == '':
        return False
    else:
        return True

print("Plotting data from:{}".format(log_path))
with open(log_path) as temp_log:
    temp_data = [x.strip().split(',') for x in temp_log.readlines()[history:]]

myplot_x = []
myplot_x_lbl = []
myplot_y1 = []
myplot_y2 = []
myplot_y3 = []

temp_sens_1_correction = 0.0

sample_len = 10
sample = []
sample_time = temp_data[sample_len][0]  # the first timestamp
ravg_sample_len = 50

running_average_temp = 0
running_average_rh = 0
running_average_pres = 0
trend_length = 30
myplot_y1_trend = []
myplot_y2_trend = []
myplot_y3_trend = []

print("Found {} samples, smoothing {}/plot".format(len(temp_data), sample_len))

for x in range(0, len(temp_data), sample_len - 1):
    sample  = temp_data[x * sample_len: x * sample_len + sample_len]
    if len(sample) == 0:
        continue
    sample_time = [float(s[0]) for s in sample]
    sample_temp = [s[2] for s in sample]
    sample_humi = [s[3] for s in sample]
    sample_pres = [s[4] for s in sample]
    ts = sum(sample_time) / len(sample_time)
    temp = [float(d) for d in filter(filterblank, sample_temp)]
    rh = [float(d) for d in filter(filterblank, sample_humi)]
    pres = [float(d) for d in filter(filterblank, sample_pres)]

    dt = datetime.fromtimestamp(ts)

    try:
        avg_temp = round(sum(temp) / len(temp) + temp_sens_1_correction, 1)
        avg_rh = round(sum(rh) / len(rh), 1)
        avg_pres = round(sum(pres) / len(pres), 1)
        
        myplot_y1.append(avg_temp)
        myplot_y2.append(avg_rh)
        myplot_y3.append(avg_pres)
        myplot_x.append(dt)
        running_average_temp = round(sum(myplot_y1[-trend_length:]) / len(myplot_y1[-trend_length:]), 1)
        myplot_y1_trend.append(running_average_temp)
        running_average_rh = round(sum(myplot_y2[-trend_length:]) / len(myplot_y2[-trend_length:]), 1)
        myplot_y2_trend.append(running_average_rh)
        running_average_pres = round(sum(myplot_y3[-trend_length:]) / len(myplot_y3[-trend_length:]), 1)
        myplot_y3_trend.append(running_average_pres)


    except Exception as ex:
        print("Error:{}-{}".format(ex, sample[-1]))
        pass

print("points to plot:{}".format(len(myplot_x)))

print("last:{}".format(myplot_x[-1]))

last_temp = myplot_y1[-1]

#fig, ax1 = plt.plot(myplot_x, myplot_y1)
fig, ax1 = plt.subplots()
ax1.patch.set_facecolor((0.3, 0.3, 0.3))
fig.patch.set_facecolor((0.3, 0.3, 0.3))
plt.xticks(rotation=90, )
ax1.set_ylabel('')
ax1.plot(myplot_x, myplot_y1, color=(0.2,0.7,0.5,0.2))
ax1.plot(myplot_x, myplot_y1_trend, linewidth=3, linestyle='dashed', color=(0.2,0.7,0.5,0.9))
#ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(12, 30)

ax2 = ax1.twinx()
ax2.set_ylabel('')
#ax2.tick_params(axis="y",direction="in")
ax2.plot(myplot_x, myplot_y2, color=(0.1,0.1,0.8,0.2))
ax2.plot(myplot_x, myplot_y2_trend, linewidth=3, linestyle='dashed', color=(0.1,0.1,0.8,0.9))
#ax2.tick_params(axis='y', labelcolor=color, length=6)
ax2.set_ylim(0, 110)

ax3 = ax1.twinx()
ax3.set_ylabel('')
#ax3.labelpad = 20
ax3.tick_params(axis="y",direction="out", pad=25)
ax3.plot(myplot_x, myplot_y3, color=(0.6,0.4,0.4,0.2))
ax3.plot(myplot_x, myplot_y3_trend, linewidth=3, linestyle='dashed', color=(0.6,0.4,0.4,1.0))
ax3.set_ylim(950, 990)


ax1.text(0.01, 0.98, "Indoor: {}".format(myplot_x[-1].strftime('%Y-%m-%d %H:%M')),
        horizontalalignment='left', verticalalignment='top', transform=ax1.transAxes, fontsize=16
        )
ax1.text(0.01, 0.02, "{}ºC".format(myplot_y1[-1]),
        horizontalalignment='left', verticalalignment='bottom', transform=ax1.transAxes, fontsize=16,
        bbox={"facecolor":"green", "alpha":0.2}
        )
ax1.text(0.4, 0.02, "{} %".format(myplot_y2[-1]),
        horizontalalignment='left', verticalalignment='bottom', transform=ax1.transAxes, fontsize=16,
        bbox={"facecolor":"blue", "alpha":0.2}
        )
ax1.text(0.99, 0.02, "{} hpa".format(myplot_y3[-1]),
        horizontalalignment='right', verticalalignment='bottom', transform=ax1.transAxes, fontsize=16,
        bbox={"facecolor":"red", "alpha":0.2}
        )

fig.autofmt_xdate()
ax1.fmt_xdata = mdates.DateFormatter('%m-%d')
fig.tight_layout()  # otherwise the right y-label is slightly clipped

#plt.axis([myplot_x[0], myplot_x[-1], 12, 27])
#plt.xticks(rotation=90)
plt.savefig('/var/www/html/indoor_temp.png')

mem_used = memory_profiler.memory_usage()[0] - mem1[0]
time_taken = time.time() - t1

print("Memory:{}\nTime:{}".format(mem_used, time_taken))
