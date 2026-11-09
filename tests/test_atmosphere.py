import pytest
import numpy as np
from aeroengineer.atmosphere import StandardAtmosphere

def test_properties_scalar():
    T, P, rho = StandardAtmosphere.properties(0)
    assert abs(T - 288.15) < 0.1
    assert abs(P - 101325) < 10

def test_properties_array():
    altitudes = np.array([0, 11000, 20000])
    T, P, rho = StandardAtmosphere.properties(altitudes)
    assert T.shape == altitudes.shape
    assert P.shape == altitudes.shape
