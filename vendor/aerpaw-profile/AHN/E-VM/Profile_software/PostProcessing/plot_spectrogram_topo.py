import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np


def load_iq_fc32(filename, num_samples):
    return np.fromfile(filename, dtype=np.complex64, count=num_samples, offset=1500 * 8)


def compute_stft(iq_samples, fft_size, hop_size):
    num_frames = (len(iq_samples) - fft_size) // hop_size + 1
    stft_matrix = np.empty((fft_size // 2, num_frames), dtype=np.float32)

    for i in range(num_frames):
        start = i * hop_size
        windowed = iq_samples[start : start + fft_size] * np.hanning(fft_size)
        spectrum = np.fft.fft(windowed, n=fft_size)
        power_db = 20 * np.log10(np.abs(spectrum[: fft_size // 2]) + 1e-12)
        stft_matrix[:, i] = power_db

    return stft_matrix


def plot_3d_spectrogram(stft_matrix, sample_rate, fft_size, hop_size):
    num_bins, num_frames = stft_matrix.shape
    freqs = np.fft.fftfreq(fft_size, d=1 / sample_rate)[: fft_size // 2]
    times = np.arange(num_frames) * hop_size / sample_rate * 1000  # in ms

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    for t in range(num_frames):
        xs = np.full(num_bins, times[t])
        ys = freqs
        zs = stft_matrix[:, t]
        ax.plot(xs, ys, zs, color=cm.viridis(t / num_frames))

    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_zlabel("Power (dB)")
    plt.title("3D Spectrogram of IQ Data")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Plot 3D Spectrogram from fc32 IQ data")
    parser.add_argument("filename", help="Path to IQ binary file (.fc32 format)")
    parser.add_argument("--sample_rate", type=float, default=15.36e6, help="Sample rate in Hz")
    parser.add_argument("--fft_size", type=int, default=512, help="FFT size")
    parser.add_argument("--hop_size", type=int, default=256, help="Hop size between FFT windows")
    parser.add_argument("--samples", type=int, default=10_000_000, help="Number of samples to read")
    args = parser.parse_args()

    iq = load_iq_fc32(args.filename, args.samples)
    stft = compute_stft(iq, args.fft_size, args.hop_size)
    plot_3d_spectrogram(stft, args.sample_rate, args.fft_size, args.hop_size)
