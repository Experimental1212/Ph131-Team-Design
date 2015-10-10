from pylab import *

''' Numerical prediction for the kinematics of a baseball in freefall
    Starting height = 550ft = 167.64 meters
'''

DELTA_T = 0.001  # seconds
T_MAX = 50.00  # seconds
M = 0.145      # kg
K = 7.9026e-4  # drag coefficient (drag force = Kv^2)
g = 9.81       # m/s^2
X_INITIAL = 167.64  # m

DECIMAL_PRECISION = int(log10(1 / DELTA_T))


def decimal_format(x, precision=DECIMAL_PRECISION):  # precision=2 means 0.##
    if x >= 0:
        return str(int(x) + round(pow(10, precision) * x) % pow(10, precision) / (0.0+(pow(10, precision))))
    else:
        n = -x
        return str(int(n) - round(pow(10, precision) * n) % pow(10, precision) / (0.0+(pow(10, precision))))


t = arange(0, T_MAX, DELTA_T)
v_drag = zeros(len(t))
v_vacuum = zeros(len(t))
x_drag = zeros(len(t));  x_drag[0] = X_INITIAL
x_vacuum = zeros(len(t)); x_vacuum[0] = X_INITIAL

# quadratic formula inputs
A = -K / (2.0*M)
B = -1.0/DELTA_T

t_final_vacuum_index = 0
for i in range(1, len(t)):
    c = g + A*(v_drag[i-1]**2) + v_drag[i-1] / DELTA_T
    v_drag[i] = (-B - sqrt(B**2 - 4*A*c)) / (2*A)  # quadratic formula
    v_vacuum[i] = v_vacuum[i-1] + g*DELTA_T
    x_drag[i] = x_drag[i-1] - v_drag[i]*DELTA_T
    x_vacuum[i] = x_vacuum[i-1] - v_vacuum[i]*DELTA_T

    # "final time" is the first negative position
    if x_vacuum[i-1] > 0:
        t_final_vacuum_index = i-1
    if x_drag[i-1] < 0:
        t = t[:i-1]
        v_drag = v_drag[:i]
        v_vacuum = v_vacuum[:i]
        x_drag = x_drag[:i]
        x_vacuum = x_vacuum[:i]
        break

# Output results
print "Results for a free falling baseball dropped from x = " + str(X_INITIAL) + " m :"
print "Acknowledging air resistance, at x = " + decimal_format(x_drag[len(x_drag)-1]) + " m,"
print "t = " + str(t[len(t)-1]) + " s, v = " + decimal_format(v_drag[len(v_drag)-1]) + " m/s (with drag)."
print "Ignoring air resistance, at x = " + decimal_format(x_vacuum[t_final_vacuum_index]) + " m,"
print "t = "+str(t[t_final_vacuum_index])+"s, v = " + decimal_format(v_vacuum[t_final_vacuum_index]) + " m/s (no drag)."

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
