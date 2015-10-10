from pylab import *

''' Numerical prediction for the kinematics of a baseball in freefall
    Starting height = 550ft = 167.64 meters
'''

DELTA_T = 0.01  # seconds
T_MAX = 10.00  # seconds
M = 0.145      # kg
K = 7.9026e-4  # drag coefficient (drag force = Kv^2)
g = 9.81       # m/s^2
X_INITIAL = 167.64  # m

t = arange(0, T_MAX, DELTA_T)
v_drag = zeros(len(t))
v_vacuum = zeros(len(t))
x_drag = zeros(len(t));  x_drag[0] = X_INITIAL
x_vacuum = zeros(len(t)); x_vacuum[0] = X_INITIAL

# quadratic formula inputs
A = -K / (2.0*M)
B = -1.0/DELTA_T
for i in range(1, len(t)):
    if x_drag[i-1] <= 0:
        t = t[:i]
        break
    c = g + A*v_drag[i-1]*v_drag[i-1] + v_drag[i-1] / DELTA_T
    v_drag[i] = (-B - sqrt(B**2 - 4*A*c)) / (2*A)  # quadratic formula
    v_vacuum[i] = v_vacuum[i-1] + g*DELTA_T
    x_drag[i] = x_drag[i-1] - v_drag[i]*DELTA_T
    x_vacuum[i] = x_vacuum[i-1] - v_vacuum[i]*DELTA_T

# Output results
print "At t = " + str(max(t)) + " s,"
print "v = " + str(max(v_drag)) + " m/s"
print "v = " + str(max(v_vacuum)) + " m/s (no drag)"

# plot graph
v_vs_t_color = 'b'
x_vs_t_color = 'r'

# plot velocity vs. time
fig, axis1 = subplots()
line1 = axis1.plot(t, v_drag[:len(t)], '-'+v_vs_t_color, label='Velocity (drag)')
line2 = axis1.plot(t, v_vacuum[:len(t)], ':'+v_vs_t_color, label='Velocity (no drag)')
axis1.set_xlabel('Time (s)')
# Make the y-axis label and tick labels match the velocity line color
axis1.set_ylabel('Velocity (m/s)', color=v_vs_t_color)
for tl in axis1.get_yticklabels():
    tl.set_color(v_vs_t_color)

# plot position vs. time
axis2 = axis1.twinx()
line3 = axis2.plot(t, x_drag[:len(t)], '-'+x_vs_t_color, label='Position (drag)')
line4 = axis2.plot(t, x_vacuum[:len(t)], ':'+x_vs_t_color, label='Position (no drag)')
axis2.set_ylim(0, (X_INITIAL/10)*10 + 10)
axis2.set_ylabel('Position (m)', color=x_vs_t_color)
for tl in axis2.get_yticklabels():
    tl.set_color(x_vs_t_color)

# title and legend
lines = line1+line2+line3+line4
labels = [l.get_label() for l in lines]
axis1.legend(lines, labels, loc=(0.025, 0.5), prop={'size': 12})
title('Velocity and Position vs. Time of a Baseball in Freefall')

show()
