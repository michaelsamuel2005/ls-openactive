"""
F-06 — paired binary sizing for the restated H-P.

Sizes the number of TEMPLATES (q) needed for a one-sided paired test of
usefulness, one designated presentation arm vs P0, alpha = .05, power 0.80.

q counts templates, not task rows and not judgments.

Inputs are a declared range, not estimates: no pilot data exists for the
discordant rate, so min-q is reported across a grid as a sensitivity.

Fahmi Alshahabi, 29 August 2026.
"""
import math


def min_templates(p_disc, p_fav):
    """p_disc: proportion of templates where the arms disagree.
       p_fav:  of those, proportion favouring the designated arm."""
    n_disc = ((1.645 * 0.5 + 0.84 * math.sqrt(p_fav * (1 - p_fav))) / (p_fav - 0.5)) ** 2
    q_min = n_disc / p_disc
    return math.ceil(q_min)


p_disc_values = [0.20, 0.30, 0.40, 0.50]
p_fav_values = [0.60, 0.65, 0.70, 0.75, 0.80]

print("min templates (q) by discordant rate and favourable share")
print("p_disc", p_fav_values)
for p_disc in p_disc_values:
    print(p_disc, [min_templates(p_disc, p_fav) for p_fav in p_disc_values and p_fav_values])