from src.orbitalMechanics.adalianOrbit import AdalianOrbit


# Given orbital data for Adalia Prime
orbital_data = {
    "a": 2.192,  # Semi-major axis in Astronomical Units (AU)
    "e": 0.325,  # Eccentricity
    "i": 0.002443460952792061,  # Inclination in radians
    "o": 3.4108969571725183,  # Longitude of ascending node in radians
    "w": 5.283809777487633,  # Argument of periapsis in radians
    "m": 0.9480628496833199,  # Mean anomaly at epoch in radians

    "p": None,  # Semi-latus rectum in meters
    "nu": None,  # True anomaly in radians
}

adalia_orbit = AdalianOrbit(orbital_data)

# Example operations:

# 1. Get radius at a specific true anomaly
nu = 0.5  # True anomaly in radians
radius = adalia_orbit.getRadius(nu)
print(f"Radius at true anomaly {nu} radians: {radius} meters")

# 2. Generate a smooth orbit trajectory with 100 points
num_points = 4
smooth_orbit = adalia_orbit.getSmoothOrbit(num_points)
print(f"Smooth orbit trajectory with {num_points} points: {smooth_orbit}")

# 3. Get position at a specific elapsed time since epoch
elapsed_time_days = 100  # Elapsed time in days
position = adalia_orbit.getPositionAtTime(elapsed_time_days)
print(f"Position at {elapsed_time_days} days since epoch: {position}")