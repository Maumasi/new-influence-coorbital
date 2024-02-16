import math
from src.orbitalMechanics.astro.propagation import farnocchia_coe
from src.orbitalMechanics.astro.elements import rv2coe, coe2rv


class Orbit:
    def __init__(self, mu, p, ecc, inc, raan, argp, nu, epoch=0):
        self.mu = mu
        self.p = p
        self.ecc = ecc
        self.inc = inc
        self.raan = raan
        self.argp = argp
        self.nu = nu
        self.epoch = epoch

    @staticmethod
    def fromStateVectors(mu, r, v, epoch=0):
        p, ecc, inc, raan, argp, nu = rv2coe(mu, r, v)
        return Orbit(mu, p, ecc, inc, raan, argp, nu, epoch)

    @staticmethod
    def fromClassicElements(mu, p, ecc, inc, raan, argp, nu, epoch=0):
        return Orbit(mu, p, ecc, inc, raan, argp, nu, epoch)

    @property
    def a(self):
        return self.p / (1 - self.ecc ** 2)

    @property
    def coe(self):
        return {'p': self.p, 'ecc': self.ecc, 'inc': self.inc, 'raan': self.raan, 'argp': self.argp, 'nu': self.nu}

    @property
    def period(self):
        return 2 * math.pi * math.sqrt(abs(self.a) ** 3 / self.mu)

    @property
    def radius(self):
        return self.p / (1 + self.ecc * math.cos(self.nu))

    @property
    def rv(self):
        (r, v), _ = coe2rv(self.mu, self.p, self.ecc, self.inc, self.raan, self.argp, self.nu)
        return {'r': r, 'v': v}

    def propagateFor(self, tof):
        self.nu = farnocchia_coe(self.mu, self.p, self.ecc, self.inc, self.raan, self.argp, self.nu, tof)
        self.epoch += tof

    def propagateTo(self, epoch):
        tof = epoch - self.epoch
        self.propagateFor(tof)

    def sampleAtEpoch(self, epoch):
        tof = epoch - self.epoch
        nu = farnocchia_coe(self.mu, self.p, self.ecc, self.inc, self.raan, self.argp, self.nu, tof)
        return self.sampleAtAngle(nu)

    def sampleAtAngle(self, nu):
        r, v = coe2rv(self.mu, self.p, self.ecc, self.inc, self.raan, self.argp, nu)
        return {'r': r, 'v': v}

    def ephem(self, samples=100, tof=None, start=None):
        if not tof and self.ecc >= 1:
            raise ValueError('tof must be specified for non elliptical orbits')
        if not tof:
            tof = self.period
        if not start:
            start = self.epoch

        dt = tof / samples
        times = [start + i * dt for i in range(samples)]
        return [self.sampleAtEpoch(t) for t in times]
