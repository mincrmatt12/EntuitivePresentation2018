import matplotlib
import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0, 2, 0.01)
s = 1 + np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(title="sample")
ax.set(xlabel="x label yay")

ax.grid()

plt.show()

