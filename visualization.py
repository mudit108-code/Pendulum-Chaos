import matplotlib.pyplot as plt


def trajectory(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y, lw=1)
    ax.set_title("End Mass Trajectory")
    ax.set_aspect("equal")
    ax.grid(True)
    return fig


def angle_time(t, th1, th2):
    fig, ax = plt.subplots()
    ax.plot(t, th1, label="θ₁")
    ax.plot(t, th2, label="θ₂")
    ax.set_title("Angular Position vs Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Angle (rad)")
    ax.legend()
    ax.grid(True)
    return fig


def phase_space(th, w, label):
    fig, ax = plt.subplots()
    ax.plot(th, w)
    ax.set_title(f"Phase Space ({label})")
    ax.set_xlabel("θ (rad)")
    ax.set_ylabel("ω (rad/s)")
    ax.grid(True)
    return fig


def energy_plot(t, E):
    fig, ax = plt.subplots()
    ax.plot(t, E)
    ax.set_title("Total Energy vs Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Energy (J)")
    ax.grid(True)
    return fig
