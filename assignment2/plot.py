# !/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt


# parameters to modify 
filename="interval001.txt"
label='0.01 interval'
xlabel = 'RTT'
ylabel = 'CDF'
title='CDF 0.01 interval plot'
fig_name='0.01 interval ping.png'
bins=1000000 #adjust the number of bins to your plot

## load data from input file
t = np.loadtxt(filename, delimiter=" ", dtype="float")

## if your data is "X Y" (2 cols), use the following line
#plt.plot(t[:,0], t[:,1], label=label)  # Plot some data on the (implicit) axes.

## if your data is "X" (1 col), use the following line
#plt.plot(t, label=label)  # Plot some data on the (implicit) axes.

## comment the lines above and uncomment the line below to plot a simple CDF
#plt.hist(t[:], bins, density=True, histtype='step', cumulative=True, label=label)

## comment the lines above and uncomment the 4 lines below for a nicer CDF
n = np.arange(1,len(t)+1) / float(len(t))
ts = np.sort(t)
fig, ax = plt.subplots()
ax.step(ts,n)
minimum = np.min(ts)
median = np.percentile(ts, 50)
a90th_percentile = np.percentile(ts, 90)
a99th_percentile = np.percentile(ts, 99)
maximum = np.percentile(ts, 100)
average = np.mean(ts)
print("minimum = ", minimum, "median = ", median, "90th = ", a90th_percentile, "99th = ", a99th_percentile, "maximum =", maximum, "average = ", average)


plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.legend()
plt.savefig(fig_name)
plt.show()
