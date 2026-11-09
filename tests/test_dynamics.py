import pytest
import numpy as np
from aeroengineer.dynamics import GasDynamics

def test_mach_velocity_consistency():
    gd = GasDynamics()
    T = 288.15  # Kelvin
    v = 340     # m/s
    M = gd.mach_from_velocity(v, T)
    v_calc = gd.velocity_from_mach(M, T)
    assert abs(v - v_calc) < 1e-3

def test_isentropic_ratios():
    gd = GasDynamics()
    M = 2.0
    p_ratio = gd.isentropic_pressure_ratio(M)
    T_ratio = gd.isentropic_temperature_ratio(M)
    d_ratio = gd.density_ratio(M)
    assert 0 < p_ratio < 1
    assert 0 < T_ratio < 1
    assert 0 < d_ratio < 1
