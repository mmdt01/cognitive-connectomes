# Placement robustness: degree vs eigenvector-centrality score

Memory-collapse `f*` (mean over supercritical sr >= 3); the placement claim is `hub_first < stratified < periphery_first`.

| sign_mode | score | hub_first | stratified | periphery_first | hub<strat<peri |
|---|---|---|---|---|---|
| edge | degree | 0.179 | 0.133 | 0.248 | no |
| edge | eigenvector | 0.176 | 0.129 | 0.268 | no |
| dale | degree | 0.087 | 0.124 | 0.164 | yes |
| dale | eigenvector | 0.103 | 0.118 | 0.219 | yes |

