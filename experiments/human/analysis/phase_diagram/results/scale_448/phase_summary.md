# Phase diagram -- sign fraction x spectral radius (human N=448)

Order parameters oriented so **higher = connectome advantage**; primary = `edge` / `stratified`. Panel A reads the MC task, Panel B the Lorenz task.

## Panel A -- memory

### dD (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | -134.75 | +329.44 | +295.95 |
| 0.25 | -86.37 | -0.70 | +4.33 |
| 0.5 | -75.54 | -0.09 | +2.35 |

### dMC (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | -0.70 | +8.65 | +9.01 |
| 0.25 | -0.52 | +1.09 | +1.01 |
| 0.5 | -0.37 | +1.54 | +0.99 |

### dNARMA (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | +0.26 | +0.26 | +0.13 |
| 0.25 | +0.00 | +0.03 | +0.02 |
| 0.5 | +0.03 | +0.01 | +0.01 |

## Panel B -- generative

### dStraight (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | +0.00 | +0.00 | +0.00 |
| 0.25 | +2.32 | +0.11 | +0.06 |
| 0.5 | +1.41 | +0.07 | +0.03 |

### dVPT (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | +0.70 | +0.35 | -0.37 |
| 0.25 | +2.65 | +0.18 | +0.00 |
| 0.5 | +1.47 | +0.00 | +0.00 |

### dClimate (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | -0.00 | -1.62 | -9.30 |
| 0.25 | +3.22 | +7.02 | +30.98 |
| 0.5 | +1.27 | +38.85 | +15.36 |

## Order parameter vs spectral predictor (Spearman, stratified, supercritical)

| panel | order param | predictor | r_s | n |
|---|---|---|---|---|
| B_generative | dClimate | B_effective_radius | +0.72 | 143 |
| B_generative | dClimate | bulk95 | +0.65 | 143 |
| B_generative | dClimate | B_abs_mean_state | -0.40 | 143 |
| B_generative | dClimate | perron_root | -0.23 | 143 |
| B_generative | dClimate | B_mean_gain | -0.09 | 143 |
| A_memory | dD | A_mean_gain | -0.94 | 143 |
| A_memory | dD | A_abs_mean_state | +0.79 | 143 |
| A_memory | dD | A_effective_radius | +0.43 | 143 |
| A_memory | dD | bulk95 | -0.30 | 143 |
| A_memory | dD | perron_root | +0.09 | 143 |
| A_memory | dMC | A_mean_gain | -0.76 | 143 |
| A_memory | dMC | A_abs_mean_state | +0.68 | 143 |
| A_memory | dMC | A_effective_radius | +0.33 | 143 |
| A_memory | dMC | bulk95 | -0.25 | 143 |
| A_memory | dMC | perron_root | +0.04 | 143 |
| A_memory | dNARMA | A_abs_mean_state | +0.77 | 143 |
| A_memory | dNARMA | bulk95 | -0.64 | 143 |
| A_memory | dNARMA | A_mean_gain | -0.45 | 143 |
| A_memory | dNARMA | perron_root | +0.20 | 143 |
| A_memory | dNARMA | A_effective_radius | -0.14 | 143 |
| B_generative | dStraight | B_effective_radius | +0.57 | 143 |
| B_generative | dStraight | bulk95 | +0.44 | 143 |
| B_generative | dStraight | B_abs_mean_state | -0.25 | 143 |
| B_generative | dStraight | B_mean_gain | +0.12 | 143 |
| B_generative | dStraight | perron_root | -0.04 | 143 |
| B_generative | dVPT | B_mean_gain | +0.50 | 143 |
| B_generative | dVPT | B_abs_mean_state | -0.29 | 143 |
| B_generative | dVPT | bulk95 | +0.19 | 143 |
| B_generative | dVPT | perron_root | -0.03 | 143 |
| B_generative | dVPT | B_effective_radius | +0.02 | 143 |

## Boundary agreement (mean |f*_observed - f*_predicted|)

| targeting | comparison | mean abs df* | n sr |
|---|---|---|---|
| stratified | A_vs_meanstate | 0.167 | 12 |
| stratified | B_vs_effradius | 0.103 | 7 |
| stratified | B_vs_meanstate | 0.126 | 10 |
| stratified | A_vs_B | 0.092 | 10 |

