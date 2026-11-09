import numpy as np

class StandardAtmosphere:
    """
    Provides standard atmosphere properties up to 86 km altitude.

    Based on the International Standard Atmosphere 1976 (ISA).
    Units are SI by default:
    - altitude: meters
    - temperature: Kelvin
    - pressure: Pascal
    - density: kg/m^3
    """

    # Layer base altitudes (m) and lapse rates (K/m)
    _layers = [
        (0, 288.15, 101325, 0.0065),
        (11000, 216.65, 22632.1, 0.0),
        (20000, 216.65, 5474.89, -0.001),
        (32000, 228.65, 868.02, -0.0028),
        (47000, 270.65, 110.91, 0.0),
        (51000, 270.65, 66.94, 0.0028),
        (71000, 214.65, 3.96, 0.0),
        (84852, 186.95, 0.37, 0.0),
    ]

    R = 287.05  # Gas constant for air, J/(kg·K)
    g0 = 9.80665  # gravity acceleration, m/s^2

    @classmethod
    def properties(cls, altitude_m):
        """
        Calculate temperature (K), pressure (Pa), and density (kg/m³) at given altitude(s).

        Parameters:
            altitude_m : float or array-like
                Altitude(s) in meters (0 - 86,000 m)

        Returns:
            temperature : float or numpy.ndarray
            pressure : float or numpy.ndarray
            density : float or numpy.ndarray
        """
        alt = np.atleast_1d(altitude_m)
        temperature = np.empty_like(alt, dtype=float)
        pressure = np.empty_like(alt, dtype=float)

        for i, h in enumerate(alt):
            # Clip altitude max to 86 km
            h = min(max(h, 0.0), 86000.0)

            # Find layer of altitude
            for j in range(len(cls._layers) - 1):
                base_h, base_t, base_p, lapse = cls._layers[j]
                next_base_h = cls._layers[j + 1][0]
                if base_h <= h < next_base_h:
                    break
            else:
                # Above highest defined layer
                base_h, base_t, base_p, lapse = cls._layers[-1]

            dh = h - base_h

            if lapse == 0.0:
                # Isothermal layer
                temperature[i] = base_t
                pressure[i] = base_p * np.exp(-cls.g0 * dh / (cls.R * base_t))
            else:
                # Gradient layer
                temperature[i] = base_t - lapse * dh
                pressure[i] = base_p * (temperature[i] / base_t) ** (cls.g0 / (lapse * cls.R))

        density = pressure / (cls.R * temperature)
        if np.isscalar(altitude_m):
            return temperature[0], pressure[0], density[0]
        return temperature, pressure, density
