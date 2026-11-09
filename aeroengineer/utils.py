def to_float_array(x):
    """
    Convert input to a numpy float array for internal processing.
    """
    import numpy as np
    return np.asarray(x, dtype=float)
