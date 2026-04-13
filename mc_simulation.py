#!/usr/bin/env python3
"""
SAPM Monte Carlo Simulation — FX Fixing / Self-Referential Pricing Trap
=========================================

Reproduces all quantitative results in:

  Postnieks, E. (2026). SAPM Working Paper: FX Fixing (Self-Referential Pricing Trap).
  Available: SSRN.

This script is self-contained. Dependencies: numpy, scipy only.
Seeded at seed=42 — produces bit-identical results on any machine
with numpy>=1.24, scipy>=1.10.

Usage
-----
  pip install numpy scipy
  python mc_simulation.py

Theory
------
β_W = ΔW / Π  where:
  Π  = annual industry revenue ($B/yr) — never profit
  ΔW = total annualized welfare destruction ($B/yr)
     = Σ_i W_i across all channels, sampled with correlation ρ=0.3

Classification: Class 2 — Intractability
"""

import json
import numpy as np
from pathlib import Path
from scipy import stats

CONFIG = {
    "paper_id": "libor",
    "domain_name": "FX Fixing",
    "theorem": "Self-Referential Pricing Trap",
    "classification": "Class 2 \u2014 Intractability",
    "seed": 42,
    "n_draws": 100000,
    "correlation_rho": 0.3,
    "private_payoff_B": 28.4,
    "channels": {
        "C1_direct_transfer": {
            "dist": "lognormal",
            "low": 35.0,
            "mid": 52.0,
            "high": 70.0,
            "weight": 0.255,
            "description": "Direct counterparty transfer deadweight. Paper \u00a74.1: central $52B/yr. DOJ/CFTC enforcement; Jefferson County; $6B US municipal losses."
        },
        "C2_hedging_inefficiency": {
            "dist": "lognormal",
            "low": 30.0,
            "mid": 44.0,
            "high": 60.0,
            "weight": 0.216,
            "description": "Hedging failure/capital misallocation. Paper \u00a74.2: central $44B/yr. Berndt/Duffie/Zhu: 15-30B implied; FX TCA differential."
        },
        "C3_monetary_signal": {
            "dist": "lognormal",
            "low": 25.0,
            "mid": 38.0,
            "high": 55.0,
            "weight": 0.186,
            "description": "Monetary policy signal distortion. Paper \u00a74.3: central $38B/yr. Central bank rate-setting error amplified through credit markets."
        },
        "C4_regulatory_deadweight": {
            "dist": "lognormal",
            "low": 14.0,
            "mid": 22.0,
            "high": 33.0,
            "weight": 0.108,
            "description": "Regulatory/compliance deadweight. Paper \u00a74.4: central $22B/yr. $550M/yr lobbying + enforcement overhead + compliance burden."
        },
        "C5_litigation_transition": {
            "dist": "lognormal",
            "low": 11.0,
            "mid": 18.0,
            "high": 27.0,
            "weight": 0.088,
            "description": "Litigation and SOFR transition costs. Paper \u00a74.5: central $18B/yr. $20B+ fines amortized + transition infrastructure."
        },
        "C6_trust_erosion": {
            "dist": "normal",
            "low": 20.0,
            "mid": 30.0,
            "high": 42.0,
            "weight": 0.147,
            "description": "Institutional trust erosion/governance failure. Paper \u00a74.6: central $30B/yr. Reputational contagion; benchmark confidence discount."
        }
    },
    "impossibility_floor": 3.0
}

# ─────────────────────────────────────────────────────────────────────────────
# SIMULATION ENGINE (identical across all SAPM domains)
# ─────────────────────────────────────────────────────────────────────────────

def generate_correlated_draws(config, rng):
    channels = config["channels"]
    n_draws  = config["n_draws"]
    rho      = config["correlation_rho"]
    n_ch     = len(channels)
    corr     = np.full((n_ch, n_ch), rho)
    np.fill_diagonal(corr, 1.0)
    L        = np.linalg.cholesky(corr)
    Z        = rng.standard_normal((n_draws, n_ch))
    Z_corr   = Z @ L.T
    draws    = np.zeros((n_draws, n_ch))
    names    = list(channels.keys())
    for i, (name, p) in enumerate(channels.items()):
        U    = stats.norm.cdf(Z_corr[:, i])
        dist, low, mid, high = p["dist"], p["low"], p["mid"], p["high"]
        if dist == "lognormal":
            sigma = np.log(high / mid) / 1.645
            draws[:, i] = stats.lognorm.ppf(U, s=sigma, scale=mid)
        elif dist == "normal":
            sigma = (high - low) / (2 * 1.645)
            draws[:, i] = stats.norm.ppf(U, loc=mid, scale=sigma)
        elif dist == "triangular":
            c = (mid - low) / (high - low)
            draws[:, i] = stats.triang.ppf(U, c, loc=low, scale=high - low)
        else:
            raise ValueError(f"Unknown distribution: {dist}")
    return draws, names


def build_sensitivity_matrix(config):
    channels = config["channels"]
    names    = list(channels.keys())
    mids     = [channels[n]["mid"] for n in names]
    vsl_idx  = mids.index(max(mids))
    pi       = config["private_payoff_B"]
    matrix   = []
    for vm in [0.5, 0.75, 1.0, 1.25, 1.5]:
        row = {"vsl_multiplier": vm, "values": {}}
        for dc in [0.0, 0.10, 0.20, 0.30, 0.40]:
            total = sum(mids[i] * (vm if i == vsl_idx else 1.0) for i in range(len(names)))
            row["values"][f"dc_{int(dc*100)}pct"] = round(total * (1 - dc) / pi, 2)
        matrix.append(row)
    return matrix


def build_histogram(beta_draws, n_bins=80):
    counts, edges = np.histogram(beta_draws, bins=n_bins)
    return [
        {"bin_low": round(float(edges[i]),3), "bin_high": round(float(edges[i+1]),3),
          "bin_mid": round(float((edges[i]+edges[i+1])/2),3),
          "count": int(counts[i]), "density": round(float(counts[i]/len(beta_draws)),6)}
        for i in range(len(counts))
    ]


def run():
    cfg = CONFIG
    rng = np.random.default_rng(seed=cfg["seed"])
    print(f"SAPM Monte Carlo — {cfg['domain_name']} ({cfg['theorem']})")
    print(f"  N={cfg['n_draws']:,}  seed={cfg['seed']}  ρ={cfg['correlation_rho']}  Π=${cfg['private_payoff_B']:,}B")
    draws, names = generate_correlated_draws(cfg, rng)
    total       = np.sum(draws, axis=1)
    beta        = total / cfg["private_payoff_B"]
    p5, p95     = np.percentile(beta, [5, 95])
    p1, p99     = np.percentile(beta, [1, 99])
    pi_sa       = total - cfg["private_payoff_B"]
    floor       = cfg.get("impossibility_floor")
    p_floor     = float(np.mean(beta < floor)) if floor else None
    ch_stats    = {
        n: {"median": round(float(np.median(draws[:,i])),1),
             "mean":   round(float(np.mean(draws[:,i])),1),
             "p5":     round(float(np.percentile(draws[:,i],5)),1),
             "p95":    round(float(np.percentile(draws[:,i],95)),1),
             "std":    round(float(np.std(draws[:,i])),1)}
        for i, n in enumerate(names)
    }
    results = {
        "paper_id": cfg["paper_id"],
        "domain_name": cfg["domain_name"],
        "theorem": cfg["theorem"],
        "classification": cfg["classification"],
        "seed": cfg["seed"], "n_draws": cfg["n_draws"],
        "n_channels": len(cfg["channels"]),
        "correlation_rho": cfg["correlation_rho"],
        "private_payoff_B": cfg["private_payoff_B"],
        "beta_w": {
            "median": round(float(np.median(beta)),2),
            "mean":   round(float(np.mean(beta)),2),
            "std":    round(float(np.std(beta)),2),
            "p1":  round(float(p1),2), "p5":  round(float(p5),2),
            "p95": round(float(p95),2), "p99": round(float(p99),2),
            "ci_90": [round(float(p5),1), round(float(p95),1)],
            "ci_99": [round(float(p1),1), round(float(p99),1)],
            "p_below_1": round(float(np.mean(beta < 1.0)),6),
            "p_below_1_pct": f"{np.mean(beta < 1.0)*100:.4f}%",
        },
        "impossibility_floor": {
            "floor_value": floor,
            "p_below_floor": round(p_floor,6) if p_floor is not None else None,
            "p_below_floor_pct": f"{p_floor*100:.4f}%" if p_floor is not None else None,
        } if floor else None,
        "welfare_cost": {
            "total_median_B": round(float(np.median(total)),1),
            "total_mean_B":   round(float(np.mean(total)),1),
            "total_p5_B":     round(float(np.percentile(total,5)),1),
            "total_p95_B":    round(float(np.percentile(total,95)),1),
        },
        "pi_sa": {
            "median_B": round(float(np.median(pi_sa)),1),
            "mean_B":   round(float(np.mean(pi_sa)),1),
            "p5_B":     round(float(np.percentile(pi_sa,5)),1),
            "p95_B":    round(float(np.percentile(pi_sa,95)),1),
        },
        "channel_statistics": ch_stats,
        "sensitivity_matrix": build_sensitivity_matrix(cfg),
    }
    bw = results["beta_w"]
    wc = results["welfare_cost"]
    print(f"  β_W median : {bw['median']}")
    print(f"  90% CI     : {bw['ci_90']}")
    print(f"  P(β_W < 1) : {bw['p_below_1_pct']}")
    print(f"  ΔW median  : ${wc['total_median_B']:,.1f}B/yr")
    return results


if __name__ == "__main__":
    results = run()
    out = Path(__file__).parent / "mc_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"  Wrote: {out}")
    rng2 = np.random.default_rng(seed=CONFIG["seed"])
    d2, _ = generate_correlated_draws(CONFIG, rng2)
    t2    = np.sum(d2, axis=1)
    b2    = t2 / CONFIG["private_payoff_B"]
    hist  = build_histogram(b2)
    hout  = Path(__file__).parent / "mc_histogram.json"
    hout.write_text(json.dumps(hist, indent=2), encoding="utf-8")
    print(f"  Wrote: {hout}")
    bw = results["beta_w"]
    print(f"\nVerify: beta_w.median = {bw['median']}  ci_90 = {bw['ci_90']}")
