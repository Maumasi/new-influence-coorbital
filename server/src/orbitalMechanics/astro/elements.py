import numpy as np
import math
from src.orbitalMechanics.astro.angles import E_to_nu, F_to_nu
from src.orbitalMechanics.astro.utils import modulo, rotation_matrix


# See: https://github.com/poliastro/poliastro/blob/main/src/poliastro/core/elements.py

def coe2rv(mu, p, ecc, inc, raan, argp, nu):
    # Position and velocity in PQW frame
    r_pqw = p / (1 + ecc * np.cos(nu)) * np.array([np.cos(nu), np.sin(nu), 0])
    v_pqw = np.sqrt(mu / p) * np.array([-np.sin(nu), ecc + np.cos(nu), 0])

    # Rotation matrices
    rm_raan = rotation_matrix(-raan, 2)
    rm_inc = rotation_matrix(-inc, 0)
    rm_argp = rotation_matrix(-argp, 2)

    # Combined rotation matrix using numpy.dot for matrix multiplication
    R = np.dot(np.dot(rm_argp, rm_inc), rm_raan)

    # Transform to the geocentric equatorial frame using numpy.dot
    r_geo = np.dot(R, r_pqw)
    v_geo = np.dot(R, v_pqw)

    return r_geo, v_geo



def rv2coe(mu, r, v, tol=1e-8):
    raan, argp, nu = None, None, None

    h = math.cross(r, v)
    n = math.cross([0, 0, 1], h)
    e = [
        (math.dot(v, v) - mu / math.norm(r)) * r[i] - math.dot(r, v) * v[i]
        for i in range(3)
    ]
    e = [e[i] / mu for i in range(3)]

    ecc = math.norm(e)
    p = math.dot(h, h) / mu
    inc = math.acos(h[2] / math.norm(h))

    circular = ecc < tol
    equatorial = abs(inc) < tol

    if equatorial and not circular:
        # Equatorial elliptical orbit
        raan = 0
        argp = math.atan2(e[1], e[0]) % (2 * math.pi)
        nu = math.atan2(math.dot(h, math.cross(e, r)) / math.norm(h), math.dot(r, e))
    elif not equatorial and circular:
        # Non-equatorial circular orbit
        raan = modulo(math.atan2(n[1], n[0]), (2 * math.pi))
        argp = 0
        nu = math.atan2(math.dot(r, math.cross(h, n)) / math.norm(h), math.dot(r, n))
    elif equatorial and circular:
        # Equatorial circular orbit
        raan = 0
        argp = 0
        nu = modulo(math.atan2(r[1], r[0]), (2 * math.pi))
    else:
        a = p / (1 - (ecc ** 2))
        mu_a = mu * a

        if a > 0:
            # Elliptical orbit
            e_se = math.dot(r, v) / math.sqrt(mu_a)
            e_ce = math.norm(r) * math.dot(v, v) / mu - 1
            E = math.atan2(e_se, e_ce)
            nu = E_to_nu(E, ecc)
        else:
            # Hyperbolic orbit
            e_sh = math.dot(r, v) / math.sqrt(-mu_a)
            e_ch = math.norm(r) * (math.norm(v) ** 2) / mu - 1
            F = math.log((e_ch + e_sh) / (e_ch - e_sh)) / 2
            nu = F_to_nu(F, ecc)

        raan = modulo(math.atan2(n[1], n[0]), (2 * math.pi))
        px = math.dot(r, n)
        py = math.dot(r, math.cross(h, n)) / math.norm(h)
        argp = modulo((math.atan2(py, px) - nu), (2 * math.pi))

    # Shift true anomaly into range of -pi to pi
    nu = ((nu % (2 * math.pi) + 3 * math.pi) % (2 * math.pi)) - math.pi

    return {"p": p, "ecc": ecc, "inc": inc, "raan": raan, "argp": argp, "nu": nu}
