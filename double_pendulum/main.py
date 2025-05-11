import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

# Pendulum rod lengths (m), bob masses (kg)
L1, L2 = 1, 1
m1, m2 = 1, 1
g = 9.81

def deriv(y, t, L1, L2, m1, m2):
    theta1, z1, theta2, z2 = y
    c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)

    theta1dot = z1
    z1dot = (m2*g*np.sin(theta2)*c - m2*s*(L1*z1**2*c + L2*z2**2) -
             (m1+m2)*g*np.sin(theta1)) / L1 / (m1 + m2*s**2)
    theta2dot = z2
    z2dot = ((m1+m2)*(L1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) + 
             m2*L2*z2**2*s*c) / L2 / (m1 + m2*s**2)
    return theta1dot, z1dot, theta2dot, z2dot

def calc_E(y):
    th1, th1d, th2, th2d = y.T
    V = -(m1+m2)*L1*g*np.cos(th1) - m2*L2*g*np.cos(th2)
    T = 0.5*m1*(L1*th1d)**2 + 0.5*m2*((L1*th1d)**2 + (L2*th2d)**2 +
            2*L1*L2*th1d*th2d*np.cos(th1-th2))
    return T + V

# Time setup
tmax, dt = 30, 0.01
t = np.arange(0, tmax+dt, dt)
y0 = np.array([3*np.pi/7, 0, 3*np.pi/4, 0])
y = odeint(deriv, y0, t, args=(L1, L2, m1, m2))

# Check energy conservation
EDRIFT = 0.05
E = calc_E(y0)
if np.max(np.sum(np.abs(calc_E(y) - E))) > EDRIFT:
    raise RuntimeError('Maximum energy drift of {} exceeded.'.format(EDRIFT))

# Convert to Cartesian
theta1, theta2 = y[:,0], y[:,2]
x1 = L1 * np.sin(theta1)
y1 = -L1 * np.cos(theta1)
x2 = x1 + L2 * np.sin(theta2)
y2 = y1 - L2 * np.cos(theta2)

# Trail settings
r = 0.05
trail_secs = 1
max_trail = int(trail_secs / dt)
ns = 20  # trail segments

# Plot setup
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-L1-L2-r, L1+L2+r)
ax.set_ylim(-L1-L2-r, L1+L2+r)
ax.set_aspect('equal')
plt.axis('off')

line, = ax.plot([], [], 'k-', lw=2)
bob1 = Circle((0, 0), r, fc='b', zorder=10)
bob2 = Circle((0, 0), r, fc='r', zorder=10)
anchor = Circle((0, 0), r/2, fc='k', zorder=10)
ax.add_patch(bob1)
ax.add_patch(bob2)
ax.add_patch(anchor)

trail_segments = [ax.plot([], [], 'r-', alpha=(j/ns)**2, lw=2)[0] for j in range(ns)]

def init():
    line.set_data([], [])
    bob1.set_center((0, 0))
    bob2.set_center((0, 0))
    for seg in trail_segments:
        seg.set_data([], [])
    return [line, bob1, bob2] + trail_segments

def update(i):
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]
    line.set_data(thisx, thisy)
    bob1.set_center((x1[i], y1[i]))
    bob2.set_center((x2[i], y2[i]))

    for j in range(ns):
        imin = i - (ns - j)*max_trail // ns
        if imin < 0:
            trail_segments[j].set_data([], [])
            continue
        imax = imin + max_trail // ns
        trail_segments[j].set_data(x2[imin:imax], y2[imin:imax])
    return [line, bob1, bob2] + trail_segments

ani = FuncAnimation(fig, update, frames=range(0, len(t), int(1 / 30 / dt)),
                    init_func=init, blit=True, interval=1000/30)
plt.show()
