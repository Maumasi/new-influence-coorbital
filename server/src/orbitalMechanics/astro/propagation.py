from math import sqrt, acos, acosh, cos, pi
from src.orbitalMechanics.astro.utils import modulo
from src.orbitalMechanics.astro.elements import rv2coe, coe2rv
from src.orbitalMechanics.astro.angles import (
    nu_to_E,
    E_to_M,
    M_to_E,
    E_to_nu,
    nu_to_D,
    D_to_M,
    D_to_M_near_parabolic,
    M_to_D,
    M_to_D_near_parabolic,
    D_to_nu,
    nu_to_F,
    F_to_M,
    M_to_F,
    F_to_nu
)

# See: https://github.com/poliastro/poliastro/blob/main/src/poliastro/core/propagation/farnocchia.py

def farnocchia_rv(mu, r0, v0, tof):
    coe = rv2coe(mu, r0, v0)
    nu = farnocchia_coe(mu, coe['p'], coe['ecc'], coe['inc'], coe['raan'], coe['argp'], coe['nu'], tof)
    return coe2rv(mu, coe['p'], coe['ecc'], coe['inc'], coe['raan'], coe['argp'], nu)

def farnocchia_coe(mu, p, ecc, inc, raan, argp, nu, tof):
    q = p / (1 + ecc)
    delta_t0 = delta_t_from_nu(nu, ecc, mu, q)
    delta_t = delta_t0 + tof
    return nu_from_delta_t(delta_t, ecc, mu, q)

def delta_t_from_nu(nu, ecc, mu=1, q=1, delta=1e-2):
    if ecc < 0:
        raise ValueError('ecc must be in [0, ∞)')
    if nu >= pi or nu < -pi:
        raise ValueError('nu must be in [-pi, pi)')
    
    if ecc < 1 - delta:
        # Strong elliptic
        E = nu_to_E(nu, ecc)  # (-pi, pi]
        M = E_to_M(E, ecc)  # (-pi, pi]
        n = sqrt(mu * (1 - ecc) ** 3 / q ** 3)
    elif ecc < 1:
        E = nu_to_E(nu, ecc)  # (-pi, pi]

        if delta <= 1 - ecc * cos(E):
            # Strong elliptic
            M = E_to_M(E, ecc)  # (-pi, pi]
            n = sqrt(mu * (1 - ecc) ** 3 / q ** 3)
        else:
            # Near parabolic
            D = nu_to_D(nu)  # (-∞, ∞)
            M = D_to_M_near_parabolic(D, ecc)
            n = sqrt(mu / (2 * q ** 3))
    elif ecc == 1:
        # Parabolic
        D = nu_to_D(nu)  # (-∞, ∞)
        M = D_to_M(D)  # (-∞, ∞)
        n = sqrt(mu / (2 * q ** 3))
    elif 1 + ecc * cos(nu) < 0:
        # Unfeasible region
        return float('nan')
    elif ecc <= 1 + delta:
        F = nu_to_F(nu, ecc)  # (-∞, ∞)

        if delta <= ecc * cosh(F) - 1:
            # Strong hyperbolic
            M = F_to_M(F, ecc)  # (-∞, ∞)
            n = sqrt(mu * (ecc - 1) ** 3 / q ** 3)
        else:
            # Near parabolic
            D = nu_to_D(nu)  # (-∞, ∞)
            M = D_to_M_near_parabolic(D, ecc)  # (-∞, ∞)
            n = sqrt(mu / (2 * q ** 3))
    else:
        # Strong hyperbolic
        F = nu_to_F(nu, ecc)  # (-∞, ∞)
        M = F_to_M(F, ecc)  # (-∞, ∞)
        n = sqrt(mu * (ecc - 1) ** 3 / q ** 3)

    return M / n

def nu_from_delta_t(delta_t, ecc, mu=1, q=1, delta=1e-2):
    if ecc < 1 - delta:
        # Strong elliptic
        n = sqrt(mu * (1 - ecc) ** 3 / q ** 3)
        M = n * delta_t
        E = M_to_E(modulo((M + pi), (2 * pi)) - pi, ecc)
        nu = E_to_nu(E, ecc)
    elif ecc < 1:
        E_delta = acos((1 - delta) / ecc)
        n = sqrt(mu * (1 - ecc) ** 3 / q ** 3)
        M = n * delta_t

        if E_to_M(E_delta, ecc) <= abs(M):
            E = M_to_E(modulo((M + pi), (2 * pi)) - pi, ecc)
            nu = E_to_nu(E, ecc)
        else:
            D = M_to_D_near_parabolic(M, ecc)
            nu = D_to_nu(D)
    elif ecc == 1:
        n = sqrt(mu / (2 * q ** 3))
        M = n * delta_t
        D = M_to_D(M)
        nu = D_to_nu(D)
    elif ecc <= 1 + delta:
        F_delta = acosh((1 + delta) / ecc)
        n = sqrt(mu * (ecc - 1) ** 3 / q ** 3)
        M = n * delta_t

        if F_to_M(F_delta, ecc) <= abs(M):
            F = M_to_F(M, ecc)
            nu = F_to_nu(F, ecc)
        else:
            D = M_to_D_near_parabolic(M, ecc)
            nu = D_to_nu(D)
    else:
        n = sqrt(mu * (ecc - 1) ** 3 / q ** 3)
        M = n * delta_t
        F = M_to_F(M, ecc)
        nu = F_to_nu(F, ecc)

    return nu

delta_t_from_nu, nu_from_delta_t, farnocchia_coe, farnocchia_rv = (
    delta_t_from_nu,
    nu_from_delta_t,
    farnocchia_coe,
    farnocchia_rv,
)
