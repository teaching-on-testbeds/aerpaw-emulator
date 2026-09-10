import argparse

import matplotlib.pyplot as plt
import numpy as np


def load_fc32(filename, num_samples, skip_samples=0):
    """Load complex64 IQ data from .fc32 file with optional skipping"""
    offset_bytes = skip_samples * 8  # each complex64 sample = 8 bytes
    return np.fromfile(filename, dtype=np.complex64, count=num_samples, offset=offset_bytes)


def plot_frequency_spectrum(iq_data, sample_rate):
    """Plot magnitude spectrum in dB"""
    n = len(iq_data)
    windowed = iq_data * np.hanning(n)
    spectrum = np.fft.fftshift(np.fft.fft(windowed))
    magnitude_db = 20 * np.log10(np.abs(spectrum) + 1e-12)

    freqs = np.fft.fftshift(np.fft.fftfreq(n, d=1 / sample_rate))

    plt.figure(figsize=(12, 6))
    plt.plot(freqs, magnitude_db, color="navy")
    plt.title("Frequency Domain (Magnitude Spectrum)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot frequency spectrum of fc32 IQ data")
    parser.add_argument("filename", help="Path to .fc32 IQ file")
    parser.add_argument("--sample_rate", type=float, default=15.36e6, help="Sample rate in Hz")
    parser.add_argument("--samples", type=int, default=4096, help="Number of IQ samples to read")
    parser.add_argument("--skip", type=int, default=0, help="Number of samples to skip at start")

    args = parser.parse_args()

    iq = load_fc32(args.filename, args.samples, args.skip)
    plot_frequency_spectrum(iq, args.sample_rate)
