import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
num_frames = 100
theta_range = np.linspace(0, 2 * np.pi, num_frames)

# Create figure
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.set_title('Unitary Evolution of a Single Qubit (XZ Plane)')

point, = ax.plot([], [], 'ro', label='|ψ⟩', markersize=10)
path, = ax.plot([], [], 'b--', alpha=0.5)
xdata, ydata = [], []

def qubit_to_coords(theta):
    x = np.sin(theta)
    z = np.cos(theta)
    return x, z

def init():
    point.set_data([], [])
    path.set_data([], [])
    return point, path

def update(frame):
    theta = theta_range[frame]
    x, z = qubit_to_coords(theta)
    xdata.append(x)
    ydata.append(z)
    point.set_data([x], [z])
    path.set_data(xdata, ydata)
    return point, path

ani = animation.FuncAnimation(fig, update, frames=num_frames, init_func=init,
                              blit=True, interval=50)

ani.save("unitary_qubit_evolution.gif", writer="pillow", fps=20)
