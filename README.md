# SAPM Monte Carlo — FX Fixing / Self-Referential Pricing Trap

**Public replication repository for quantitative results in:**

> Postnieks, E. (2026). *FX Fixing (Self-Referential Pricing Trap).* SAPM Working Paper. SSRN.

> **Note**: Formerly 'LIBOR fixing'; expanded to cover WM/Reuters FX fixing, gold fix, and benchmark rate manipulation broadly.

This repository provides everything needed to independently reproduce, audit,
and extend the Monte Carlo simulation underlying the paper's core results.
The paper is available on SSRN.

---

## Results (N = 100,000 draws, seed = 42)

| Statistic | Value |
|-----------|-------|
| **β_W median** | **7.26** |
| β_W mean | 7.32 |
| β_W std | 1.01 |
| **90% CI** | **[5.77, 9.07]** |
| 99% CI | [5.24, 9.94] |
| P(β_W < 1) | 0.0000% |
| **ΔW median** | **$206.1B/yr** |
| Π (revenue) | $28.4B/yr |

**β_W = 7.26** means the fx fixing industry destroys **$7.26 in system
welfare for every $1.00 in revenue** — across 6 channels and 100,000 Monte Carlo draws.

**Classification**: Class 2 — Intractability

---

## What Is β_W?

```
β_W = ΔW / Π
```

- **ΔW** = total annualized welfare destruction ($B/yr) across all channels
- **Π** = annual industry **revenue** ($B/yr) — not profit

β_W > 1: industry destroys more welfare than it captures in revenue.
β_W > 3: Strong Intractability threshold — reform requires structural replacement.

---

## Quick Start

```bash
git clone https://github.com/epostnieks/sapm-mc-fx-fixing.git
cd sapm-mc-fx-fixing
pip install numpy scipy
python mc_simulation.py
```

Expected output: `β_W median : 7.26` and `ΔW median : $206.1B/yr`

---

## Welfare Channels

| Channel | Median ($B/yr) | 90% CI | Distribution |
|---------|---------------|--------|--------------|
| C1_direct_transfer | $51.9B | [$38.5B, $69.9B] | Lognormal |
| C2_hedging_inefficiency | $44.0B | [$32.2B, $60.1B] | Lognormal |
| C3_monetary_signal | $38.0B | [$26.3B, $55.0B] | Lognormal |
| C4_regulatory_deadweight | $22.0B | [$14.7B, $33.0B] | Lognormal |
| C5_litigation_transition | $18.0B | [$12.0B, $26.9B] | Lognormal |
| C6_trust_erosion | $30.0B | [$19.0B, $41.0B] | Normal |
| **Total ΔW** | **$206.1B** | **[$163.9B, $257.6B]** | Correlated (ρ=0.3) |

---

## Repository Contents

| File | Description |
|------|-------------|
| `mc_simulation.py` | Self-contained simulation — no private pipeline imports |
| `mc_results.json` | Pre-run results (100K draws, seed=42) — matches paper |
| `mc_histogram.json` | Binned β_W distribution (80 bins) for companion chart |
| `assumptions.md` | Every parameter: value, derivation, source |
| `data_sources.md` | Full citation list for all empirical inputs |

---

## Replication Notes

Results are seeded and deterministic. Tested with:
```
numpy==1.26.4  scipy==1.12.0  Python 3.11.9
```

The `median` and `ci_90` (to 1 decimal) match exactly across compatible versions.

---

## License

CC BY 4.0. Cite as:

> Postnieks, E. (2026). *SAPM Monte Carlo — FX Fixing (Self-Referential Pricing Trap)*.
> GitHub: epostnieks/sapm-mc-fx-fixing.
> https://github.com/epostnieks/sapm-mc-fx-fixing
