import numpy as np
from scipy.integrate import solve_ivp

G = 9.81


def equations(t, state, m1, m2, L1, L2):
    theta1, omega1, theta2, omega2 = state
    delta = theta2 - theta1

    den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta) ** 2
    den2 = (L2 / L1) * den1

    domega1 = (
        m2 * L1 * omega1**2 * np.sin(delta) * np.cos(delta)
        + m2 * G * np.sin(theta2) * np.cos(delta)
        + m2 * L2 * omega2**2 * np.sin(delta)
        - (m1 + m2) * G * np.sin(theta1)
    ) / den1

    domega2 = (
        -m2 * L2 * omega2**2 * np.sin(delta) * np.cos(delta)
        + (m1 + m2) * G * np.sin(theta1) * np.cos(delta)
        - (m1 + m2) * L1 * omega1**2 * np.sin(delta)
        - (m1 + m2) * G * np.sin(theta2)
    ) / den2

    return [omega1, domega1, omega2, domega2]


def simulate(m1, m2, L1, L2, t1, t2, tmax, steps=4000):
    y0 = [t1, 0.0, t2, 0.0]
    t_eval = np.linspace(0, tmax, steps)

    sol = solve_ivp(
        equations,
        [0, tmax],
        y0,
        args=(m1, m2, L1, L2),
        t_eval=t_eval,
        rtol=1e-9,
        atol=1e-9,
    )

    th1, w1, th2, w2 = sol.y

    x1 = L1 * np.sin(th1)
    y1 = -L1 * np.cos(th1)
    x2 = x1 + L2 * np.sin(th2)
    y2 = y1 - L2 * np.cos(th2)

    T = 0.5 * m1 * (L1 * w1) ** 2 + \
        0.5 * m2 * (
            (L1 * w1) ** 2 +
            (L2 * w2) ** 2 +
            2 * L1 * L2 * w1 * w2 * np.cos(th1 - th2)
        )

    V = -(m1 + m2) * G * L1 * np.cos(th1) - m2 * G * L2 * np.cos(th2)

    E = T + V

    return {
        "t": sol.t,
        "theta1": th1,
        "omega1": w1,
        "theta2": th2,
        "omega2": w2,
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "energy": E,
        "initial_state": y0
    }
