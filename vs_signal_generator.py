"""
signal_generator.py
Generates realistic diesel engine vibration signals for a 6-cylinder
diesel engine running at 1800 RPM.

Physics:
  - Firing frequency  = (RPM / 60) * (cylinders / 2) = 90 Hz (4-stroke)
  - Harmonics at 2x, 3x, 4x firing frequency
  - Bearing fault frequencies (BPFO, BPFI, BSF) from geometry
  - Cylinder misfire = suppressed firing harmonic for that cylinder

Signal types:
  1. healthy      – clean vibration, normal harmonics
  2. misfire      – cylinder 3 misfires → asymmetric harmonic pattern
  3. bearing_worn – outer-race bearing fault (BPFO impulses + sidebands)
  4. resonance    – structural resonance near 420 Hz amplified
"""

import numpy as np


# ── Engine constants (6-cyl diesel @ 1800 RPM) ──────────────────────────────
RPM             = 1800
N_CYLINDERS     = 6
SAMPLE_RATE     = 10_000          # Hz — must be > 2× highest frequency of interest
DURATION        = 2.0             # seconds of signal
FIRING_FREQ     = (RPM / 60) * (N_CYLINDERS / 2)   # 90 Hz for 4-stroke 6-cyl

# Bearing geometry (typical deep-groove bearing, SKF 6205)
BPFO = 3.585 * (RPM / 60)        # Ball-Pass Frequency Outer race ≈ 107.6 Hz
BPFI = 5.415 * (RPM / 60)        # Ball-Pass Frequency Inner race ≈ 162.5 Hz
BSF  = 2.357 * (RPM / 60)        # Ball Spin Frequency             ≈  70.7 Hz


def _time_axis():
    return np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)


def generate_healthy():
    """Normal engine: fundamental + harmonics, small broadband noise."""
    t = _time_axis()
    sig = np.zeros_like(t)

    # Firing harmonics (decaying amplitude with harmonic order)
    for order, amp in [(1, 1.0), (2, 0.55), (3, 0.30), (4, 0.18),
                       (5, 0.10), (6, 0.07), (7, 0.04), (8, 0.02)]:
        sig += amp * np.sin(2 * np.pi * FIRING_FREQ * order * t
                            + np.random.uniform(0, 2 * np.pi))

    # Low-level broadband noise
    sig += 0.05 * np.random.randn(len(t))
    return t, sig / np.max(np.abs(sig))   # normalise to ±1


def generate_misfire(misfiring_cylinder: int = 3):
    """
    Cylinder misfire: one cylinder fails to fire every other revolution.
    Creates asymmetric spectrum — half-order components appear.
    """
    t = _time_axis()
    sig = np.zeros_like(t)

    # Full complement of harmonics
    for order, amp in [(1, 1.0), (2, 0.55), (3, 0.30), (4, 0.18), (5, 0.10)]:
        sig += amp * np.sin(2 * np.pi * FIRING_FREQ * order * t)

    # Half-order components from skipped firing events
    for half_order in [0.5, 1.5, 2.5, 3.5]:
        sig += 0.25 * np.sin(2 * np.pi * FIRING_FREQ * half_order * t)

    # Suppress the harmonic corresponding to misfiring cylinder
    cyl_harmonic = (misfiring_cylinder / N_CYLINDERS)
    sig -= 0.4 * np.sin(2 * np.pi * FIRING_FREQ * cyl_harmonic * t)

    sig += 0.06 * np.random.randn(len(t))
    return t, sig / np.max(np.abs(sig))


def generate_bearing_fault():
    """
    Outer-race bearing fault (BPFO): periodic impulses at BPFO with
    exponential decay (ring-down) and random phase modulation.
    """
    t = _time_axis()
    sig = np.zeros_like(t)

    # Base engine harmonics (reduced amplitude — bearing degradation)
    for order, amp in [(1, 0.7), (2, 0.38), (3, 0.20), (4, 0.12)]:
        sig += amp * np.sin(2 * np.pi * FIRING_FREQ * order * t)

    # BPFO impulse train with ring-down
    impulse_period = int(SAMPLE_RATE / BPFO)
    for start in range(0, len(t), impulse_period):
        decay_len = min(impulse_period, len(t) - start)
        decay = np.exp(-60 * np.arange(decay_len) / SAMPLE_RATE)
        sig[start:start + decay_len] += 1.2 * decay * np.sin(
            2 * np.pi * 2200 * np.arange(decay_len) / SAMPLE_RATE)

    # BPFO sidebands (±1×, ±2× shaft frequency)
    shaft_freq = RPM / 60
    for sideband in [-2, -1, 1, 2]:
        sig += 0.15 * np.sin(2 * np.pi * (BPFO + sideband * shaft_freq) * t)

    sig += 0.07 * np.random.randn(len(t))
    return t, sig / np.max(np.abs(sig))


def generate_resonance():
    """
    Structural resonance: engine mount or exhaust manifold resonance
    near 420 Hz excited when RPM sweep crosses critical speed.
    """
    t = _time_axis()
    sig = np.zeros_like(t)

    # Normal harmonics
    for order, amp in [(1, 0.8), (2, 0.44), (3, 0.24), (4, 0.14)]:
        sig += amp * np.sin(2 * np.pi * FIRING_FREQ * order * t)

    # Resonance peak at 420 Hz — high Q (narrow, high amplitude)
    resonance_freq = 420.0
    q_factor       = 25
    envelope       = 0.8 + 0.2 * np.sin(2 * np.pi * 1.2 * t)   # amplitude modulation
    sig += 1.8 * envelope * np.sin(2 * np.pi * resonance_freq * t) * np.exp(
        -np.pi * resonance_freq / q_factor * 0.001)

    # Sidebands around resonance
    for sideband in [-FIRING_FREQ, FIRING_FREQ]:
        sig += 0.3 * np.sin(2 * np.pi * (resonance_freq + sideband) * t)

    sig += 0.05 * np.random.randn(len(t))
    return t, sig / np.max(np.abs(sig))


ALL_CONDITIONS = {
    "healthy":      generate_healthy,
    "misfire":      generate_misfire,
    "bearing_worn": generate_bearing_fault,
    "resonance":    generate_resonance,
}

if __name__ == "__main__":
    for name, fn in ALL_CONDITIONS.items():
        t, sig = fn()
        print(f"{name:15s} | samples={len(sig)} | peak={sig.max():.4f} | rms={np.sqrt(np.mean(sig**2)):.4f}")
