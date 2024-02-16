import math
# See: https://github.com/poliastro/poliastro/blob/main/src/poliastro/core/angles.py

# Converts eccentric anomaly to mean anomaly
def E_to_M(E, ecc):
    return E - ecc * math.sin(E)

# Converts mean anomaly to eccentric anomaly
def M_to_E(M, ecc):
    E1, fVal, fDer, step = 0, 0, 0, 0
    E = M - ecc if M < 0 else M + ecc  # Initial guess for elliptical eccentric anomaly

    for i in range(50):
        fVal = E_to_M(E, ecc) - M
        fDer = 1 - ecc * math.cos(E)
        step = fVal / fDer
        E1 = E - step

        if abs(E1 - E) < 1e-7:
            break
        else:
            E = E1

    return E1

# Converts eccentric anomaly to true anomaly
def E_to_nu(E, ecc):
    return 2 * math.atan(math.sqrt((1 + ecc) / (1 - ecc)) * math.tan(E / 2))

# Converts true anomaly to eccentric anomaly
def nu_to_E(nu, ecc):
    return 2 * math.atan(math.sqrt((1 - ecc) / (1 + ecc)) * math.tan(nu / 2))

# Converts true anomaly to hyperbolic eccentric anomaly
def F_to_M(F, ecc):
    return ecc * math.sinh(F) - F

# Converts mean anomaly to hyperbolic eccentric anomaly
def M_to_F(M, ecc):
    F1, fVal, fDer, step = 0, 0, 0, 0
    F = math.asinh(M / ecc)  # Initial guess for hyperbolic eccentric anomaly

    for i in range(50):
        fVal = F_to_M(F, ecc) - M
        fDer = ecc * math.cosh(F) - 1
        step = fVal / fDer
        F1 = F - step

        if abs(F1 - F) < 1e-7:
            break
        else:
            F = F1

    return F

# Converts hyperbolic eccentric anomaly to true anomaly
def F_to_nu(F, ecc):
    return 2 * math.atan(math.sqrt((ecc + 1) / (ecc - 1)) * math.tanh(F / 2))

# Converts true anomaly to hyperbolic eccentric anomaly
def nu_to_F(nu, ecc):
    return 2 * math.atanh(math.sqrt((ecc - 1) / (ecc + 1)) * math.tan(nu / 2))

# Converts mean anomaly to true anomaly
def M_to_nu(M, ecc, delta=1e-2):
    if ecc < 1 - delta:
        # Elliptical
        M = (M + math.pi) % (2 * math.pi) - math.pi
        return E_to_nu(M_to_E(M, ecc), ecc)
    elif ecc < 1:
        # Near parabolic low
        return D_to_nu(M_to_D_near_parabolic(M, ecc))
    elif ecc == 1:
        # Parabolic
        return D_to_nu(M_to_D(M))
    elif ecc < 1 + delta:
        # Near parabolic high
        return D_to_nu(M_to_D_near_parabolic(M, ecc))
    else:
        # Hyperbolic
        return F_to_nu(M_to_F(M, ecc), ecc)

# Converts true anomaly to mean anomaly
def nu_to_M(nu, ecc, delta=1e-2):
    if ecc < 1 - delta:
        # Elliptical
        return E_to_M(nu_to_E(nu, ecc), ecc)
    elif ecc < 1:
        # Near parabolic low
        return D_to_M_near_parabolic(nu_to_D(nu), ecc)
    elif ecc == 1:
        # Parabolic
        return D_to_M(nu_to_D(nu))
    elif ecc < 1 + delta:
        # Near parabolic high
        return D_to_M_near_parabolic(nu_to_D(nu), ecc)
    else:
        # Hyperbolic
        return F_to_M(nu_to_F(nu, ecc), ecc)

# Converts parabolic anomaly to mean anomaly
def D_to_M(D):
    return D + D ** 3 / 3

def D_to_M_near_parabolic(D, ecc):
    x = (ecc - 1) / (ecc + 1) * (D ** 2)
    if abs(x) >= 1:
        raise ValueError('abs(x) must be less than 1')
    S = _S_x(ecc, x)
    return math.sqrt(2 / (1 + ecc)) * D + math.sqrt(2 / (1 + ecc) ** 3) * (D**3) * S

# Parabolic eccentric anomaly from mean anomaly, near parabolic case.
def M_to_D_near_parabolic(M, ecc):
    D1, fVal, fDer, step = 0, 0, 0, 0
    D = M_to_D(M)  # initial guess for parabolic eccentric anomaly

    for i in range(50):
        fVal = D_to_M_near_parabolic(D, ecc) - M
        fDer = _kepler_equation_prime_near_parabolic(D, ecc)
        step = fVal / fDer
        D1 = D - step

        if abs(D1 - D) < 1.48e-8:
            break
        else:
            D = D1

    return D

# Converts mean anomaly to parabolic anomaly
def M_to_D(M):
    B = 3 * M / 2
    A = (B + (1 + B ** 2) ** 0.5) ** (2 / 3)
    return 2 * A * B / (1 + A + A ** 2)

# Converts parabolic anomaly to true anomaly
def D_to_nu(D):
    return 2 * math.atan(D)

# Converts true anomaly to parabolic anomaly
def nu_to_D(nu):
    return math.tan(nu / 2)

def _kepler_equation_prime_near_parabolic(D, ecc):
    x = (ecc - 1) / (ecc + 1) * (D ** 2)
    if abs(x) >= 1:
        raise ValueError('abs(x) must be less than 1')
    S = _dS_x_alt(ecc, x)
    return math.sqrt(2 / (1 + ecc)) + math.sqrt(2 / (1 + ecc) ** 3) * (D ** 2) * S

def _S_x(ecc, x, atol=1e-12):
    if abs(x) >= 1:
        raise ValueError('abs(x) must be less than 1')
    S = 0
    k = 0

    while True:
        S_old = S
        S += (ecc - 1 / (2 * k + 3)) * x ** k
        k += 1

        if abs(S - S_old) < atol:
            return S

def _dS_x_alt(ecc, x, atol=1e-12):
    if abs(x) >= 1:
        raise ValueError('abs(x) must be less than 1')
    S = 0
    k = 0

    while True:
        S_old = S
        S += (ecc - 1 / (2 * k + 3)) * (2 * k + 3) * x**k
        k += 1

        if abs(S - S_old) < atol:
            return S

__all__ = [
    'E_to_M',
    'M_to_E',
    'E_to_nu',
    'nu_to_E',
    'F_to_M',
    'M_to_F',
    'F_to_nu',
    'nu_to_F',
    'M_to_nu',
    'nu_to_M',
    'D_to_M',
    'M_to_D',
    'D_to_nu',
    'nu_to_D',
    'M_to_D_near_parabolic',
    'D_to_M_near_parabolic'
]
