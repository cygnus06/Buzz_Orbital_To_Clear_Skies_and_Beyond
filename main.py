import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skyfield.api import load, EarthSatellite
import requests

# Function to fetch TLE data from a given URL
def fetch_tle(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure request was successful
    lines = response.text.strip().split("\n")
    satellites = []
    

    # Process lines in groups of 3 (Name, Line 1, Line 2)
    for i in range(0, len(lines) - 2, 3):
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()
        satellites.append(EarthSatellite(line1, line2, name))

    return satellites

# URLs for debris and active satellites
debris_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=cosmos-1408-debris&FORMAT=tle'
active_sats_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'

# Fetch and load TLE data
debris = fetch_tle(debris_url)
active_sats = fetch_tle(active_sats_url)
print("Debris:", [sat.name for sat in debris][:5])  # Print first 5 debris names
print("Active Satellites:", [sat.name for sat in active_sats][:5])  # Print first 5 active satellites

# Load timescale
ts = load.timescale()

# Generate time range (next 6 hours, every 5 minutes)
t_range = ts.utc(2025, 2, 14, np.arange(0, 6 * 60, 5) / 60)  # 6 hours
print(f'ts = {ts}')
print(f't_range = {t_range}')
# Create 3D plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")

# Function to plot orbits
def plot_orbits(objects, color, label):
    for obj in objects[:3]:  # Debug first 3 objects
        positions = np.array([obj.at(t).position.km for t in t_range])
        if len(positions) == 0:
            print(f"⚠️ No positions generated for {obj.name}")
        else:
            print(f"✅ {obj.name} first 3 positions:\n{positions[:3]}")
        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], alpha=0.7, color=color, label=label if obj == objects[0] else "")

# Plot debris and active satellites
plot_orbits(debris, 'red', 'Debris')
plot_orbits(active_sats, 'blue', 'Active Satellites')

# Set axis limits for better visibility
ax.set_xlim(-20000, 20000)
ax.set_ylim(-20000, 20000)
ax.set_zlim(-20000, 20000)

# Labels and formatting
ax.set_xlabel("X (km)")
ax.set_ylabel("Y (km)")
ax.set_zlabel("Z (km)")
ax.set_title("Orbital Paths of Cosmos 1408 Debris & Active Satellites")
ax.legend()

# Show the plot
plt.show(block=True)  # Force it to stay open