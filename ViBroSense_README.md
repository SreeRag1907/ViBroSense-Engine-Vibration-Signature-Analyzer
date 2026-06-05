# 🔊 ViBroSense — Engine Vibration Signature Analyzer

> **FFT-based diagnostic tool that detects diesel engine faults — cylinder misfires, bearing failures, and structural resonance — purely from vibration signal analysis. Uses the same signal processing techniques as MATLAB-based industrial diagnostics.**

---

## 📋 Overview

ViBroSense applies frequency-domain signal processing to analyse diesel engine vibration data and automatically diagnose four fault conditions:

| Condition | Detection Method | Key Indicator |
|---|---|---|
| ✅ Healthy | Harmonic pattern check | Clean integer harmonics of firing freq |
| 🔥 Cylinder Misfire | Half-order component detection | 0.5× firing frequency component |
| ⚙️ Bearing Worn (BPFO) | Hilbert envelope + impulse analysis | Peaks at BPFO (107.6 Hz) & sidebands |
| 📳 Structural Resonance | Peak frequency scan | Amplified energy near 420 Hz |

---

## 🔬 Signal Processing Techniques

1. **Fast Fourier Transform (FFT)** — converts time-domain vibration to frequency spectrum
2. **Power Spectral Density (Welch method)** — noise-robust energy distribution
3. **Harmonic Extraction** — amplitude at each engine firing harmonic (H1–H8)
4. **Hilbert Envelope Analysis** — demodulates bearing impulse periodicity
5. **Spectral Kurtosis** — localises non-Gaussian (impulsive) energy bands
6. **Fault Frequency Matching** — compares spectrum peaks to BPFO, BPFI, BSF signatures

---

## ⚙️ Engine Modelled

- **Type:** 6-cylinder, 4-stroke diesel engine
- **Speed:** 1800 RPM
- **Firing frequency:** 90 Hz
- **Bearing:** SKF 6205 geometry (BPFO = 107.6 Hz, BPFI = 162.5 Hz)
- **Sample rate:** 10,000 Hz

---

## 📊 Output Charts

| Chart | Description |
|---|---|
| `01_waveforms.png` | Time-domain signals for all 4 conditions (50 ms window) |
| `02_fft_spectra.png` | Frequency spectra with harmonic and fault frequency markers |
| `03_envelope_analysis.png` | Hilbert envelope comparison: healthy vs bearing fault |
| `04_spectral_kurtosis.png` | Impulsive energy localisation across frequency bands |
| `05_fault_heatmap.png` | Fault detection confidence matrix (conditions × signatures) |

---

## 🗂️ Project Structure

```
vibrosense/
├── signal_generator.py   # Physics-based vibration signal synthesis
├── fft_analyzer.py       # Full frequency-domain analysis engine
├── visualize.py          # All 5 diagnostic charts
├── plots/                # Generated output charts
└── README.md
```

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt

# Run full diagnostic + generate all charts
python visualize.py

# Run fault detection report in terminal
python fft_analyzer.py
```

---

## 📌 Relevance to Industrial Diagnostics

This project replicates the signal processing workflow used in MATLAB-based industrial condition monitoring:

| ViBroSense (Python) | MATLAB Equivalent |
|---|---|
| `scipy.fft` | `fft()` |
| `scipy.signal.welch` | `pwelch()` |
| `scipy.signal.hilbert` | `hilbert()` |
| Spectral Kurtosis | `kurtogram()` |
| Fault frequency matching | Bearing Toolbox |

> Rolls-Royce Power Systems uses vibration signature analysis on MTU diesel engines for predictive maintenance — this project demonstrates that exact workflow in Python.

---

*Built by C Sreerag — demonstrating FFT-based condition monitoring applicable to emission-reduction equipment in high-power diesel engines.*
