import matplotlib
matplotlib.use('TkAgg')

import random

import pylab as plt

fig = plt.figure(1)
plt.hist([random.randint(1,100) for val in range(1000)])
fig.suptitle('Random 1-100')
fig = plt.figure(2)
plt.hist([random.randint(1,1000) for val in range(1000)])
fig.suptitle('Random 1-1000')
fig = plt.figure(3)
plt.plot(range(100), [random.randint(1,100) for val in range(100)], 'x', label="stuff!")
fig.suptitle('Random 1-100')
plt.xlabel('index')
plt.ylabel('value')

leg = plt.legend()
if leg:
    leg.draggable()


plt.show()
