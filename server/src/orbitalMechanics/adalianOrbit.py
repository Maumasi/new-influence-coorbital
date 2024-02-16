from math import atan2, sqrt, tan, sin, cos, atan, atanh, pi

from numpy import isnan
from src.orbitalMechanics.constants import GM_ADALIA
from src.orbitalMechanics.astro.orbit import Orbit
import src.orbitalMechanics.astro.angles as angles
import src.orbitalMechanics.astro.constants as constants


MU = GM_ADALIA / (1000 ** 3)  # Convert to km^3 / s^2

class AdalianOrbit:
    def __init__(self, el={}, options={'units': 'AU'}):
        a = el['a']  # Semi-major axis
        e = el['e']  # Eccentricity
        i = el['i']  # Inclination
        o = el['o']  # Longitude of ascending node
        w = el['w']  # Argument of periapsis
        m = el['m']  # Mean anomoly at epoch
        p = el['p']  # Semi-latus rectum
        nu = el['nu']  # True anomaly

        units = constants.AU / 1000 if options['units'] == 'AU' else 1
        p = a * (1 - e ** 2) * units  # Convert to semi-latus rectum in km
        nu = angles.M_to_nu(m, e)  # Convert to true anomaly

        self.orbit = Orbit.fromClassicElements(MU, p, e, i, o, w, nu)

    @staticmethod
    def fromStateVectors(r, v):
        adalianOrbit = AdalianOrbit()
        adalianOrbit.orbit = Orbit.fromStateVectors(
            MU,
            [x / 1000 for x in r],  # convert to km for astro
            [x / 1000 for x in v]  # convert to km / s for astro
        )
        return adalianOrbit

    def getRadius(self, nu):
        return self.orbit.radius * 1000  # Convert km -> m

    def getPosByAngle(self, nu):
        r = self.orbit.sampleAtAngle(nu)['r']
        return {'x': r[0] * 1000, 'y': r[1] * 1000, 'z': r[2] * 1000}  # Convert km -> m

    def getSmoothOrbit(self, numPoints):
        points = self.orbit.ephem(numPoints)
        return [{'x': rv['r'][0] * 1000, 'y': rv['r'][1] * 1000, 'z': rv['r'][2] * 1000} for rv in points]

    def getPeriod(self):
        return self.orbit.period / 86400  # Convert seconds -> days

    def getPositionAtTime(self, elapsed):
        tof = elapsed * 86400  # Convert days to seconds
        r = self.orbit.sampleAtEpoch(tof)['r']
        return {'x': r[0] * 1000, 'y': r[1] * 1000, 'z': r[2] * 1000}  # Convert km -> m

    def getTrueAnomalyAtPos(self, pos):
        e, i, o, w = self.orbit['ecc'], self.orbit['inc'], self.orbit['raan'], self.orbit['argp']

        u = atan2(pos['z'] / sin(i), (pos['x'] * cos(o) + pos['y'] * sin(o)))

        if e < 1:
            E = 2 * atan(sqrt((1 - e) / (1 + e)) * tan((u - w) / 2))
            if u < w:
                E += 2 * pi
            return angles.E_to_nu(E, e)
        else:
            F = 2 * atanh(sqrt((e - 1) / (e + 1)) * tan((u - w) / 2))
            return angles.F_to_nu(F, e)
