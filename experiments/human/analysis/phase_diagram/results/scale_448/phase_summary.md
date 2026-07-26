# Phase diagram -- sign fraction x spectral radius (human N=448)

Order parameters oriented so **higher = connectome advantage**; primary = `edge` / `stratified`. Panel A reads the MC task, Panel B the Lorenz task.

## Primary: `edge` / stratified

### Panel A -- memory

**dD** (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | -134.75 | +329.44 | +295.95 |
| 0.25 | -86.37 | -0.70 | +4.33 |
| 0.5 | -75.54 | -0.09 | +2.35 |

**dMC** (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | -0.70 | +8.65 | +9.01 |
| 0.25 | -0.52 | +1.09 | +1.01 |
| 0.5 | -0.37 | +1.54 | +0.99 |

**dNARMA** (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | +0.26 | +0.26 | +0.13 |
| 0.25 | +0.00 | +0.03 | +0.02 |
| 0.5 | +0.03 | +0.01 | +0.01 |

### Panel B -- generative

**dStraight** (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | +0.00 | +0.00 | +0.00 |
| 0.25 | +2.32 | +0.11 | +0.06 |
| 0.5 | +1.41 | +0.07 | +0.03 |

**dVPT** (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | +0.70 | +0.35 | -0.37 |
| 0.25 | +2.65 | +0.18 | +0.00 |
| 0.5 | +1.47 | +0.00 | +0.00 |

**dClimate** (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | -0.00 | -1.62 | -9.30 |
| 0.25 | +3.22 | +7.02 | +30.98 |
| 0.5 | +1.27 | +38.85 | +15.36 |

## Secondary sign mode: `dale` / stratified

### Panel A -- memory

**dD** (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | -134.75 | +329.44 | +295.95 |
| 0.25 | -58.86 | -0.54 | +0.25 |
| 0.5 | -18.29 | -0.00 | +0.00 |

**dMC** (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | -0.70 | +8.65 | +9.01 |
| 0.25 | -1.05 | +0.64 | +1.43 |
| 0.5 | -0.17 | -0.37 | +1.02 |

**dNARMA** (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | +0.26 | +0.26 | +0.13 |
| 0.25 | -0.04 | +0.11 | +0.05 |
| 0.5 | -0.05 | -0.04 | +0.09 |

### Panel B -- generative

**dStraight** (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | +0.00 | +0.00 | +0.00 |
| 0.25 | +0.42 | +0.02 | +0.40 |
| 0.5 | -0.03 | -0.19 | -0.16 |

**dVPT** (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | +0.70 | +0.35 | -0.37 |
| 0.25 | +1.05 | +0.45 | +0.19 |
| 0.5 | +0.69 | +0.08 | +0.00 |

**dClimate** (f x sr)

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0 | -0.00 | -1.62 | -9.30 |
| 0.25 | -0.94 | +2.90 | +25.91 |
| 0.5 | -0.76 | +5.87 | +78.81 |

## Order parameter vs spectral predictor (Spearman, `dale`, stratified, supercritical)

| panel | order param | predictor | r_s | n |
|---|---|---|---|---|
| B_generative | dClimate | B_effective_radius | +0.46 | 429 |
| B_generative | dClimate | B_mean_gain | -0.11 | 429 |
| B_generative | dClimate | B_abs_mean_state | -0.09 | 429 |
| B_generative | dClimate | bulk95 | +0.08 | 429 |
| B_generative | dClimate | perron_root | -0.03 | 429 |
| A_memory | dD | A_mean_gain | -0.71 | 429 |
| A_memory | dD | A_abs_mean_state | +0.59 | 429 |
| A_memory | dD | A_effective_radius | +0.44 | 429 |
| A_memory | dD | bulk95 | -0.04 | 429 |
| A_memory | dD | perron_root | +0.00 | 429 |
| A_memory | dMC | A_abs_mean_state | +0.80 | 429 |
| A_memory | dMC | A_mean_gain | -0.76 | 429 |
| A_memory | dMC | A_effective_radius | +0.29 | 429 |
| A_memory | dMC | perron_root | +0.27 | 429 |
| A_memory | dMC | bulk95 | -0.23 | 429 |
| A_memory | dNARMA | A_abs_mean_state | +0.75 | 429 |
| A_memory | dNARMA | A_mean_gain | -0.52 | 429 |
| A_memory | dNARMA | perron_root | +0.50 | 429 |
| A_memory | dNARMA | bulk95 | -0.41 | 429 |
| A_memory | dNARMA | A_effective_radius | +0.00 | 429 |
| B_generative | dStraight | perron_root | +0.47 | 429 |
| B_generative | dStraight | bulk95 | -0.43 | 429 |
| B_generative | dStraight | B_abs_mean_state | +0.35 | 429 |
| B_generative | dStraight | B_effective_radius | -0.22 | 429 |
| B_generative | dStraight | B_mean_gain | -0.04 | 429 |
| B_generative | dVPT | bulk95 | -0.14 | 429 |
| B_generative | dVPT | perron_root | +0.13 | 429 |
| B_generative | dVPT | B_mean_gain | +0.11 | 429 |
| B_generative | dVPT | B_abs_mean_state | +0.10 | 429 |
| B_generative | dVPT | B_effective_radius | +0.08 | 429 |

## Order parameter vs spectral predictor (Spearman, `edge`, stratified, supercritical)

| panel | order param | predictor | r_s | n |
|---|---|---|---|---|
| B_generative | dClimate | B_effective_radius | +0.51 | 429 |
| B_generative | dClimate | bulk95 | +0.48 | 429 |
| B_generative | dClimate | B_abs_mean_state | -0.43 | 429 |
| B_generative | dClimate | perron_root | -0.09 | 429 |
| B_generative | dClimate | B_mean_gain | +0.01 | 429 |
| A_memory | dD | A_mean_gain | -0.92 | 429 |
| A_memory | dD | A_abs_mean_state | +0.90 | 429 |
| A_memory | dD | A_effective_radius | +0.33 | 429 |
| A_memory | dD | bulk95 | -0.29 | 429 |
| A_memory | dD | perron_root | +0.10 | 429 |
| A_memory | dMC | A_abs_mean_state | +0.82 | 429 |
| A_memory | dMC | A_mean_gain | -0.78 | 429 |
| A_memory | dMC | bulk95 | -0.36 | 429 |
| A_memory | dMC | A_effective_radius | +0.29 | 429 |
| A_memory | dMC | perron_root | +0.24 | 429 |
| A_memory | dNARMA | A_abs_mean_state | +0.81 | 429 |
| A_memory | dNARMA | bulk95 | -0.64 | 429 |
| A_memory | dNARMA | A_mean_gain | -0.55 | 429 |
| A_memory | dNARMA | perron_root | +0.27 | 429 |
| A_memory | dNARMA | A_effective_radius | -0.05 | 429 |
| B_generative | dStraight | B_abs_mean_state | -0.31 | 429 |
| B_generative | dStraight | perron_root | +0.30 | 429 |
| B_generative | dStraight | B_effective_radius | +0.29 | 429 |
| B_generative | dStraight | B_mean_gain | +0.22 | 429 |
| B_generative | dStraight | bulk95 | +0.04 | 429 |
| B_generative | dVPT | B_abs_mean_state | -0.31 | 429 |
| B_generative | dVPT | B_mean_gain | +0.30 | 429 |
| B_generative | dVPT | B_effective_radius | +0.15 | 429 |
| B_generative | dVPT | bulk95 | +0.10 | 429 |
| B_generative | dVPT | perron_root | +0.01 | 429 |

## Boundary agreement (mean |f*_observed - f*_predicted|)

| sign_mode | targeting | comparison | mean abs df* | n sr |
|---|---|---|---|---|
| dale | hub_first | A_vs_meanstate | 0.089 | 13 |
| dale | hub_first | B_vs_effradius | 0.166 | 7 |
| dale | hub_first | B_vs_meanstate | 0.111 | 7 |
| dale | hub_first | A_vs_B | 0.022 | 7 |
| dale | periphery_first | A_vs_meanstate | 0.445 | 1 |
| dale | periphery_first | B_vs_effradius | -- | 0 |
| dale | periphery_first | B_vs_meanstate | 0.272 | 1 |
| dale | periphery_first | A_vs_B | 0.103 | 13 |
| dale | stratified | A_vs_meanstate | 0.205 | 12 |
| dale | stratified | B_vs_effradius | 0.208 | 8 |
| dale | stratified | B_vs_meanstate | 0.166 | 13 |
| dale | stratified | A_vs_B | 0.097 | 13 |
| edge | hub_first | A_vs_meanstate | 0.181 | 13 |
| edge | hub_first | B_vs_effradius | -- | 0 |
| edge | hub_first | B_vs_meanstate | 0.245 | 1 |
| edge | hub_first | A_vs_B | 0.183 | 1 |
| edge | periphery_first | A_vs_meanstate | -- | 0 |
| edge | periphery_first | B_vs_effradius | -- | 0 |
| edge | periphery_first | B_vs_meanstate | 0.391 | 1 |
| edge | periphery_first | A_vs_B | 0.019 | 6 |
| edge | stratified | A_vs_meanstate | 0.167 | 12 |
| edge | stratified | B_vs_effradius | 0.103 | 7 |
| edge | stratified | B_vs_meanstate | 0.126 | 10 |
| edge | stratified | A_vs_B | 0.092 | 10 |

