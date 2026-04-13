# Data Sources — FX Fixing Monte Carlo Simulation

Channel parameters in `mc_simulation.py` trace to the sources listed here.
The paper (FX Fixing: Self-Referential Pricing Trap) is available on SSRN and contains the full
reference list and §4 calibration narrative.

---

## Channel Sources

### `C1_direct_transfer`

Direct counterparty transfer deadweight. Paper §4.1: central $52B/yr. DOJ/CFTC enforcement; Jefferson County; $6B US municipal losses.

*Full citations: paper §4 (available SSRN).*

### `C2_hedging_inefficiency`

Hedging failure/capital misallocation. Paper §4.2: central $44B/yr. Berndt/Duffie/Zhu: 15-30B implied; FX TCA differential.

*Full citations: paper §4 (available SSRN).*

### `C3_monetary_signal`

Monetary policy signal distortion. Paper §4.3: central $38B/yr. Central bank rate-setting error amplified through credit markets.

*Full citations: paper §4 (available SSRN).*

### `C4_regulatory_deadweight`

Regulatory/compliance deadweight. Paper §4.4: central $22B/yr. $550M/yr lobbying + enforcement overhead + compliance burden.

*Full citations: paper §4 (available SSRN).*

### `C5_litigation_transition`

Litigation and SOFR transition costs. Paper §4.5: central $18B/yr. $20B+ fines amortized + transition infrastructure.

*Full citations: paper §4 (available SSRN).*

### `C6_trust_erosion`

Institutional trust erosion/governance failure. Paper §4.6: central $30B/yr. Reputational contagion; benchmark confidence discount.

*Full citations: paper §4 (available SSRN).*

---

## Industry Revenue (Π)

The private payoff Π = $28.4B/yr is global annual industry revenue.
Source: paper §2 and §4. See paper §DA-1 (Decision Audit Field 7) for full
revenue source documentation.

---

## SAPM Framework

- Postnieks, E. (2026). *The Private Pareto Theorem*. SAPM Foundation Paper. SSRN.
- Postnieks, E. (2026). *FX Fixing (Self-Referential Pricing Trap)*. SAPM Working Paper. SSRN.

---

## Distribution Methodology

- Iman, R. L., & Conover, W. J. (1982). A distribution-free approach to
  inducing rank correlation among input variables. *Communications in
  Statistics — Simulation and Computation*, 11(3), 311–334.
- Cooke, R. M. (1991). *Experts in Uncertainty*. Oxford University Press.
