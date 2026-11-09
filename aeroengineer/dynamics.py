import numpy as np

class GasDynamics:
    """
    Common air/gas dynamics functions for compressible flow.
    Default is air with gamma=1.4, R=287.05 J/(kg·K).
    """

    def __init__(self, gamma: float = 1.4, R: float = 287.05):
        self.gamma = gamma
        self.R = R

    def mach_from_velocity(self, velocity, temperature):
        """
        Calculate Mach number from velocity and temperature.

        Parameters:
            velocity : float or numpy.ndarray
                Flow velocity in m/s
            temperature : float or numpy.ndarray
                Static temperature in Kelvin

        Returns:
            Mach number (float or numpy.ndarray)
        """
        a = np.sqrt(self.gamma * self.R * temperature)  # speed of sound
        return np.asarray(velocity) / a

    def velocity_from_mach(self, mach, temperature):
        """
        Calculate velocity from Mach number and temperature.

        Parameters:
            mach : float or numpy.ndarray
                Mach number
            temperature : float or numpy.ndarray
                Static temperature in Kelvin

        Returns:
            Velocity in m/s (float or numpy.ndarray)
        """
        a = np.sqrt(self.gamma * self.R * temperature)
        return np.asarray(mach) * a

    def isentropic_pressure_ratio(self, mach):
        """
        Pressure ratio (p / p0) across an isentropic flow.

        Parameters:
            mach : float or numpy.ndarray
                Mach number

        Returns:
            Pressure ratio (static pressure / total pressure)
        """
        g = self.gamma
        m = np.asarray(mach)
        return (1 + (g - 1) / 2 * m ** 2) ** (-g / (g - 1))

    def isentropic_temperature_ratio(self, mach):
        """
        Temperature ratio (T / T0) across isentropic flow.

        Parameters:
            mach : float or numpy.ndarray
                Mach number

        Returns:
            Temperature ratio (static / total)
        """
        g = self.gamma
        m = np.asarray(mach)
        return (1 + (g - 1) / 2 * m ** 2) ** -1

    def density_ratio(self, mach):
        """
        Density ratio (rho / rho0) across isentropic flow.

        Parameters:
            mach : float or numpy.ndarray
                Mach number

        Returns:
            Density ratio (static / total)
        """
        g = self.gamma
        m = np.asarray(mach)
        return (1 + (g - 1) / 2 * m ** 2) ** (-1 / (g - 1))
