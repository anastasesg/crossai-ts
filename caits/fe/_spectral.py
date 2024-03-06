import numpy as np
import scipy


def spectral_centroid(array: np.ndarray, fs: int) -> float:
    """Computes the spectral centroid of a signal.

    Args:
        array: The input signal as a numpy.ndarray.
        fs: The sampling frequency of the signal.

    Returns:
        float: The spectral centroid of the signal.
    """
    magnitudes, freqs, sum_mag = underlying_spectral(array, fs)

    return np.sum(magnitudes * freqs) / sum_mag


def spectral_rolloff(array: np.ndarray, fs: int, perc: 0.95) -> float:
    """Computes the spectral rolloff of a signal, meaning the frequency below
    which a certain percentage of the total spectral energy, e.g. 85%, is
    contained.

    Args:
        array: The input signal as a numpy.ndarray.
        fs: The sampling frequency of the signal.
        perc: The percentage of the total spectral energy.

    Returns:
        float: The spectral rolloff of the signal.
    """
    magnitudes, _, sum_mag = underlying_spectral(array, fs)
    cumsum_mag = np.cumsum(magnitudes)
    return np.min(np.where(cumsum_mag >= perc * sum_mag)[0])


def spectral_spread(array: np.ndarray, fs: int) -> float:
    """Computes the spectral spread of a signal, meaning the weighted
    standard deviation of frequencies wrt FFT value.

    Args:
        array: The input signal as a numpy.ndarray.
        fs: The sampling frequency of the signal.

    Returns:
        float: The spectral spread of the signal.
    """
    magnitudes, freqs, sum_mag = underlying_spectral(array, fs)
    spec_centroid = spectral_centroid(array, fs)

    return np.sqrt(np.sum(((freqs - spec_centroid) ** 2) * magnitudes) /
                   sum_mag)


def spectral_skewness(array: np.ndarray, fs: int) -> float:
    """Computes the spectral skewness of a signal, meaning the distribution
    of the spectrum around its mean.

    Args:
        array: The input signal as a numpy.ndarray.
        fs: The sampling frequency of the signal.

    Returns:
        float: The spectral skewness of the signal.
    """
    magnitudes, freqs, sum_mag = underlying_spectral(array, fs)
    spec_centroid = spectral_centroid(array, fs)
    spec_spread = spectral_spread(array, fs)

    return (np.sum(((freqs - spec_centroid)**3) * magnitudes) /
            ((spec_spread**3) * sum_mag))


def spectral_kurtosis(array: np.ndarray, fs: int) -> float:
    """Computes the spectral kurtosis of a signal, meaning the distribution
    of the spectrum around its mean.

    Args:
        array: The input signal as a numpy.ndarray.
        fs: The sampling frequency of the signal.

    Returns:
        float: The spectral kurtosis of the signal.
    """
    magnitudes, freqs, sum_mag = underlying_spectral(array, fs)
    spec_centroid = spectral_centroid(array, fs)
    spec_spread = spectral_spread(array, fs)

    return (np.sum(((freqs - spec_centroid)**4) * magnitudes) /
            ((spec_spread**4) * sum_mag))


def spectral_bandwidth(
        array: np.ndarray,
        fs: int,
        p: int = 2
) -> float:
    """Computes the spectral bandwith of a signal, meaning the width of the
    spectrum.

    Args:
        array: The input signal as a numpy.ndarray.
        fs: The sampling frequency of the signal.
        p: The exponent of the Minkowski distance.

    Returns:
        float: The spectral bandwith of the signal.
    """
    magnitudes, freqs, _ = underlying_spectral(array, fs)
    spec_centroid = spectral_centroid(array, fs)

    return (np.sum(magnitudes*(freqs - spec_centroid)**p))**(1/p)


def underlying_spectral(
    array: np.ndarray,
    fs: int
) -> tuple[np.ndarray, np.ndarray, float]:
    magnitudes = np.abs(
        np.fft.rfft(array))  # magnitudes of positive frequencies
    length = len(array)
    freqs = np.abs(np.fft.fftfreq(length, 1.0 / fs)[
                   :length // 2 + 1])  # positive frequencies

    sum_mag = np.sum(magnitudes)

    return magnitudes, freqs, sum_mag


def spectral_flatness(
    array: np.ndarray,
    fs: int
) -> float:

    nperseg = min(900, len(array))
    noverlap = min(600, int(nperseg/2))
    freqs, psd = scipy.signal.welch(array, fs, nperseg=nperseg,
                                    noverlap=noverlap)
    psd_len = len(psd)
    gmean = np.exp((1/psd_len)*np.sum(np.log(psd + 1e-17)))
    amean = (1/psd_len)*np.sum(psd)

    return gmean/amean


def spectral_std(
    array: np.ndarray,
    fs: int
) -> float:
    nperseg = min(900, len(array))
    noverlap = min(600, int(nperseg / 2))
    _, psd = scipy.signal.welch(array, fs, nperseg=nperseg, noverlap=noverlap)

    return np.std(psd)


def spectral_values(
        array: np.ndarray,
        fs: int,
        perc: float = 0.95,
        p: int = 2
) -> dict:
    """Computes the underlying spectral values of a signal.

    Args:
        array: The input signal as a numpy.ndarray.
        fs: The sampling frequency of the signal.
        perc: The percentage of the total spectral energy.
        p: The exponent of the Minkowski distance.

    Returns:
        dict: A dictionary containing the spectral centroid, spectral rolloff,
        spectral spread, spectral skewness, spectral kurtosis, and spectral
        bandwidth of the signal.
    """
    return {
        "spectral_centroid": spectral_centroid(array, fs),
        "spectral_rolloff": spectral_rolloff(array, fs, perc),
        "spectral_spread": spectral_spread(array, fs),
        "spectral_skewness": spectral_skewness(array, fs),
        "spectral_kurtosis": spectral_kurtosis(array, fs),
        "spectral_bandwidth": spectral_bandwidth(array, fs, p),
        "spectral_flatness": spectral_flatness(array, fs),
        "spectral_std": spectral_std(array, fs)
    }


