"""
visualize.py  —  ViBroSense
Generates 5 diagnostic charts:
  1. Time-domain waveforms (4 conditions side-by-side)
  2. FFT spectra with harmonic markers
  3. Envelope spectra with BPFO marker
  4. Spectral kurtosis comparison
  5. Fault detection heatmap (conditions × signatures)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

from signal_generator import ALL_CONDITIONS, FIRING_FREQ, BPFO, BPFI, BSF, SAMPLE_RATE
from fft_analyzer import analyze, FAULT_SIGNATURES

os.makedirs("plots", exist_ok=True)

COLORS = {
    "healthy":      "#1B3A6B",
    "misfire":      "#E67E22",
    "bearing_worn": "#C0392B",
    "resonance":    "#8E44AD",
}
LABELS = {
    "healthy":      "Healthy",
    "misfire":      "Cylinder Misfire",
    "bearing_worn": "Bearing Worn (BPFO)",
    "resonance":    "Structural Resonance",
}
plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "--",
})

# ── Pre-compute ───────────────────────────────────────────────────────────────
signals, results = {}, {}
for name, fn in ALL_CONDITIONS.items():
    t, sig = fn()
    signals[name] = (t, sig)
    results[name] = analyze(sig, label=name)


# ── 1. Time-domain waveforms ──────────────────────────────────────────────────
def plot_waveforms():
    fig, axes = plt.subplots(2, 2, figsize=(16, 7), sharex=True, sharey=True)
    for ax, (name, (t, sig)) in zip(axes.flat, signals.items()):
        show = int(0.05 * SAMPLE_RATE)   # 50 ms window
        ax.plot(t[:show] * 1000, sig[:show], color=COLORS[name], lw=0.8)
        ax.set_title(LABELS[name], fontsize=11, fontweight="bold", color=COLORS[name])
        ax.set_xlabel("Time (ms)"); ax.set_ylabel("Amplitude (normalised)")
    fig.suptitle("ViBroSense — Time-Domain Vibration Signals (50 ms window)",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("plots/01_waveforms.png", dpi=150, bbox_inches="tight")
    plt.close(); print("  ✓ 01_waveforms.png")


# ── 2. FFT spectra with harmonic markers ──────────────────────────────────────
def plot_fft_spectra():
    fig, axes = plt.subplots(2, 2, figsize=(16, 9), sharey=False)
    for ax, (name, res) in zip(axes.flat, results.items()):
        freqs, mags = res["freqs"], res["mags"]
        mask = freqs < 600
        ax.plot(freqs[mask], mags[mask], color=COLORS[name], lw=0.9)

        # Mark firing harmonics
        for h in range(1, 9):
            hf = FIRING_FREQ * h
            if hf < 600:
                ax.axvline(hf, color="#1B3A6B", lw=0.8, linestyle="--", alpha=0.4)
                ax.text(hf + 2, mags[mask].max() * 0.92,
                        f"H{h}", fontsize=7, color="#1B3A6B", alpha=0.7)

        # Mark BPFO for bearing condition
        if name == "bearing_worn":
            ax.axvline(BPFO, color="#C0392B", lw=1.5, linestyle="-",
                       label=f"BPFO ({BPFO:.1f} Hz)")
            ax.legend(fontsize=8)

        # Mark resonance peak
        if name == "resonance":
            ax.axvline(420, color="#8E44AD", lw=1.5, linestyle="-",
                       label="Resonance (420 Hz)")
            ax.legend(fontsize=8)

        ax.set_title(LABELS[name], fontsize=11, fontweight="bold", color=COLORS[name])
        ax.set_xlabel("Frequency (Hz)"); ax.set_ylabel("|FFT| Magnitude")

    fig.suptitle("ViBroSense — FFT Frequency Spectra (0–600 Hz)",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("plots/02_fft_spectra.png", dpi=150, bbox_inches="tight")
    plt.close(); print("  ✓ 02_fft_spectra.png")


# ── 3. Envelope spectra (bearing fault detection) ─────────────────────────────
def plot_envelope():
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    for ax, name in zip(axes, ["healthy", "bearing_worn"]):
        res   = results[name]
        ef, em = res["env_freqs"], res["env_mags"]
        mask  = ef < 400
        ax.plot(ef[mask], em[mask], color=COLORS[name], lw=0.9)
        ax.axvline(BPFO, color="#C0392B", lw=2, linestyle="--",
                   label=f"BPFO ({BPFO:.1f} Hz)")
        ax.axvline(BPFI, color="#E67E22", lw=1.5, linestyle=":",
                   label=f"BPFI ({BPFI:.1f} Hz)")
        ax.set_title(f"Envelope Spectrum — {LABELS[name]}",
                     fontsize=11, fontweight="bold", color=COLORS[name])
        ax.set_xlabel("Frequency (Hz)"); ax.set_ylabel("Envelope Magnitude")
        ax.legend(fontsize=9)
    fig.suptitle("ViBroSense — Hilbert Envelope Analysis (Bearing Fault Detection)",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("plots/03_envelope_analysis.png", dpi=150, bbox_inches="tight")
    plt.close(); print("  ✓ 03_envelope_analysis.png")


# ── 4. Spectral kurtosis ──────────────────────────────────────────────────────
def plot_spectral_kurtosis():
    fig, axes = plt.subplots(2, 2, figsize=(16, 7), sharex=True)
    for ax, (name, res) in zip(axes.flat, results.items()):
        centres = res["sk_centres"]
        sk      = res["sk_values"]
        mask    = centres < 2000
        ax.bar(centres[mask], sk[mask], width=50, color=COLORS[name], alpha=0.8)
        ax.axhline(3.0, color="black", lw=1, linestyle="--",
                   label="Gaussian baseline (SK=3)")
        ax.set_title(f"SK — {LABELS[name]}", fontsize=11,
                     fontweight="bold", color=COLORS[name])
        ax.set_xlabel("Frequency (Hz)"); ax.set_ylabel("Kurtosis")
        ax.legend(fontsize=8)
    fig.suptitle("ViBroSense — Spectral Kurtosis (High SK = Impulsive Fault Energy)",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("plots/04_spectral_kurtosis.png", dpi=150, bbox_inches="tight")
    plt.close(); print("  ✓ 04_spectral_kurtosis.png")


# ── 5. Fault detection heatmap ────────────────────────────────────────────────
def plot_fault_heatmap():
    condition_names = [LABELS[k] for k in results]
    fault_names     = list(FAULT_SIGNATURES.keys())
    matrix          = np.zeros((len(results), len(fault_names)))

    for i, (cond, res) in enumerate(results.items()):
        for j, fname in enumerate(fault_names):
            info = res["faults"].get(fname, {})
            if info.get("detected"):
                matrix[i, j] = 1.0
            elif info.get("amplitude", 0) > 0:
                matrix[i, j] = info["amplitude"] / 0.01   # partial brightness

    fig, ax = plt.subplots(figsize=(13, 5))
    im = ax.imshow(matrix, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(range(len(fault_names)));  ax.set_xticklabels(fault_names, rotation=25, ha="right", fontsize=9)
    ax.set_yticks(range(len(condition_names))); ax.set_yticklabels(condition_names, fontsize=10)

    for i in range(len(condition_names)):
        for j in range(len(fault_names)):
            val = matrix[i, j]
            ax.text(j, i, "✓ DETECTED" if val >= 1 else ("~" if val > 0.1 else "—"),
                    ha="center", va="center", fontsize=9,
                    color="white" if val > 0.5 else "black", fontweight="bold")

    ax.set_title("ViBroSense — Fault Signature Detection Matrix",
                 fontsize=14, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, fraction=0.03)
    cbar.set_label("Detection Confidence", fontsize=9)
    plt.tight_layout()
    plt.savefig("plots/05_fault_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close(); print("  ✓ 05_fault_heatmap.png")


if __name__ == "__main__":
    print("Rendering ViBroSense plots...")
    plot_waveforms()
    plot_fft_spectra()
    plot_envelope()
    plot_spectral_kurtosis()
    plot_fault_heatmap()
    print("\nAll plots saved to /plots/")
