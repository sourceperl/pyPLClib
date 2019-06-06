#!/usr/bin/env python3

# Simple script to display PID response (Y)/time in second (0 to 3600s here)
# use matplotlib to display result

import time
from pyPLClib import PID
import matplotlib.pyplot as plt

# some vars
pid1_out = []
pid1_measure = []
pid1_set_point = []

# compute PID for 3600s (1 pid compute by 1s)
a_secs = range(3600)

# PID 1 param
pid1 = PID(kp=180, ti=1.66, pv_max=100.0, pv_min=0.0)

# populate lists for build chart
for sec in a_secs:
    # pid1
    pid1_out.append(pid1.out)
    pid1_measure.append(pid1.pv)
    pid1_set_point.append(pid1.sp)
    # animate process value if PID is on
    if pid1.run:
        pid1.pv += pid1.out * 0.005
        pid1.pv -= 0.05
    # set-point adjust at 500s
    if sec == 500:
        pid1.sp = 50
        pid1.start()
    # update PID (simulate a PID update every seconds)
    pid1._last_update = time.time() - 1.0
    pid1.update(force=True)

# display plot
plt.ylabel('PID value (in %)')
plt.xlabel('time (in s)')
plt.title('PID plot')
plt.plot(a_secs, pid1_out)
plt.plot(a_secs, pid1_measure)
plt.plot(a_secs, pid1_set_point)
plt.legend(('PID 1 out', 'PID 1 val', 'PID 1 set'))
# graph : X is 0 to 3600s, Y is 0 to 100
# plt.axis([0, 3600, 0, 100])
plt.show()
