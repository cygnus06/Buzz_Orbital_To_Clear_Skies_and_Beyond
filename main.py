import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skyfield.api import load

# Load TLE data
satellites = load.tle_file("cosmos_1408.tle")

# Load timescale
ts = load.timescale()

# Generate time range (next 6 hours, every 5 minutes)
t_range = ts.utc(2025, 2, 14, np.arange(0, 6 * 60, 5) / 60)  # 6 hours

# Create 3D plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")

# Plot each debris piece
for sat in satellites:
    positions = [sat.at(t).position.km for t in t_range]
    positions = np.array(positions)

    ax.plot(
        positions[:, 0], positions[:, 1], positions[:, 2], alpha=0.7
    )  # Slight transparency for better visibility

# Labels and formatting
ax.set_xlabel("X (km)")
ax.set_ylabel("Y (km)")
ax.set_zlabel("Z (km)")
ax.set_title("Orbital Paths of All Cosmos 1408 Debris")
plt.show()
