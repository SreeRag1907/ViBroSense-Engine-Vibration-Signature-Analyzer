"""
fft_analyzer.py
Frequency-domain analysis of diesel engine vibration signals.

Techniques:
  1. FFT spectrum               – identify dominant frequencies
  2. Power Spectral Density     – energy distribution across frequencies
  3. Harmonic extraction        – amplitude at each firing harmonic
  4. Envelope analysis (Hilbert) – detect bearing impulse periodicity
  5. Spectral kurtosis          – localise non-Gaussian (fault) energy
  6. Fault frequency matching   – compare peaks to known fault signatures
"""

import numpy as np
from scipy.signal import hilbert, welch
from scipy.fft import fft, fftfreq
from signal_generator import (
    SAMPLE_RATE, FIRING_FREQ, BPFO, BPFI, BSF, RPM
)


# ── FFT ─────────────────────────────────────────────────────────────────────

def compute_fft(signal: np.ndarray):
    """
    Compute one-sided FFT magnitude spectrum.
    Returns (frequencies, magnitudes) arrays.
    """
    n   = len(signal)
    win = np.hanning(n)
    X   = fft(signal * win)
    freqs = fftfreq(n, 1 / SAMPLE_RATE)

    # One-sided (positive frequencies only)
    pos = freqs >= 0
    freqs = freqs[pos]
    mags  = (2 / n) * np.abs(X[pos])    # scale for one-sided
    return freqs, mags


# ── PSD (Welch) ──────────────────────────────────────────────────────────────

def compute_psd(signal: np.ndarray, nperseg: int = 1024):
    """Welch power spectral density estimate — smoother than raw FFT."""
    freqs, psd = welch(signal, fs=SAMPLE_RATE, nperseg=nperseg,
                       window="hann", scaling="density")
    return freqs, psd


# ── Harmonic extraction ──────────────────────────────────────────────────────

def extract_harmonics(freqs: np.ndarray, mags: np.ndarray,
                      n_harmonics: int = 8, tolerance_hz: float = 3.0):
    """
    Return amplitude at each integer multiple of firing frequency.
    tolerance_hz: search window around expected harmonic centre.
    """
    results = {}
    for h in range(1, n_harmonics + 1):
        target = FIRING_FREQ * h
        mask   = np.abs(freqs - target) < tolerance_hz
        if mask.any():
            results[f"H{h} ({target:.1f} Hz)"] = float(mags[mask].max())
        else:
            results[f"H{h} ({target:.1f} Hz)"] = 0.0
    return results


# ── Envelope analysis (Hilbert) ──────────────────────────────────────────────

def envelope_analysis(signal: np.ndarray):
    """
    Compute the analytic signal envelope via Hilbert transform.
    Useful for detecting bearing impulse periodicity.
    Returns (envelope_signal, fft_of_envelope).
    """
    analytic  = hilbert(signal)
    envelope  = np.abs(analytic)
    # Remove DC
    envelope -= envelope.mean()
    env_freqs, env_mags = compute_fft(envelope)
    return envelope, env_freqs, env_mags


# ── Spectral kurtosis ────────────────────────────────────────────────────────

def spectral_kurtosis(signal: np.ndarray, n_bands: int = 50):
    """
    Divide spectrum into bands, compute kurtosis of each band's
    time-domain samples. High SK → impulsive (fault) energy in that band.
    Returns (band_centres, kurtosis_values).
    """
    n          = len(signal)
    band_size  = n // n_bands
    centres, kurtoses = [], []

    for i in range(n_bands):
        band = signal[i * band_size: (i + 1) * band_size]
        mu   = band.mean()
        std  = band.std()
        if std < 1e-9:
            k = 0.0
        else:
            k = float(np.mean(((band - mu) / std) ** 4))
        freq_centre = (i + 0.5) * (SAMPLE_RATE / 2) / n_bands
        centres.append(freq_centre)
        kurtoses.append(k)

    return np.array(centres), np.array(kurtoses)


# ── Fault signature matching ─────────────────────────────────────────────────

FAULT_SIGNATURES = {
    "Outer-Race Bearing Fault (BPFO)": BPFO,
    "Inner-Race Bearing Fault (BPFI)": BPFI,
    "Ball Spin Fault (BSF)":           BSF,
    "Shaft Imbalance (1×)":            RPM / 60,
    "Cylinder Misfire (0.5×)":         FIRING_FREQ * 0.5,
    "Resonance (420 Hz)":              420.0,
}


def match_fault_signatures(freqs: np.ndarray, mags: np.ndarray,
                            threshold_ratio: float = 0.15,
                            tolerance_hz: float = 5.0):
    """
    Check if known fault frequencies appear as peaks above threshold.
    threshold_ratio: peak must exceed this fraction of spectrum max.
    Returns dict of fault_name → (detected: bool, peak_amplitude).
    """
    max_mag   = mags.max()
    threshold = threshold_ratio * max_mag
    findings  = {}

    for fault, freq in FAULT_SIGNATURES.items():
        mask = np.abs(freqs - freq) < tolerance_hz
        if mask.any():
            peak = float(mags[mask].max())
            findings[fault] = {
                "detected":  peak > threshold,
                "amplitude": round(peak, 5),
                "freq_hz":   freq,
                "threshold": round(threshold, 5),
            }

    return findings


# ── Summary report ────────────────────────────────────────────────────────────

def analyze(signal: np.ndarray, label: str = ""):
    freqs, mags     = compute_fft(signal)
    harmonics       = extract_harmonics(freqs, mags)
    faults          = match_fault_signatures(freqs, mags)
    envelope, ef, em = envelope_analysis(signal)
    sk_centres, sk  = spectral_kurtosis(signal)

    detected = [name for name, info in faults.items() if info["detected"]]

    return {
        "label":      label,
        "freqs":      freqs,
        "mags":       mags,
        "harmonics":  harmonics,
        "faults":     faults,
        "detected":   detected,
        "envelope":   envelope,
        "env_freqs":  ef,
        "env_mags":   em,
        "sk_centres": sk_centres,
        "sk_values":  sk,
    }


if __name__ == "__main__":
    from signal_generator import ALL_CONDITIONS

    print(f"\nEngine: {int(RPM)} RPM | Firing freq: {FIRING_FREQ} Hz\n")
    print("=" * 60)

    for name, fn in ALL_CONDITIONS.items():
        _, sig = fn()
        result = analyze(sig, label=name)
        print(f"\n[{name.upper()}]")
        print("  Harmonics (top 4):")
        for k, v in list(result["harmonics"].items())[:4]:
            print(f"    {k}: {v:.4f}")
        print("  Detected faults:")
        if result["detected"]:
            for f in result["detected"]:
                print(f"    ⚠  {f}")
        else:
            print("    ✓  No faults detected")
