"""
gap_index.py — WS2 analytical core.

Reads the borough feature table (data/processed/borough_features.csv, built by the
pipeline) and produces the activity-gap index and its companions:

  need_score_z      standardised need composite (deprivation + demographics; inactivity held out)
  provision_score_z standardised community-session provision (transformed before standardising)
  gap_index_z       z(need) - z(provision)            <- the activity-gap index
  gap_index_rank    1 = widest gap
  gap_pct_based     rank/percentile-based version (robustness)
  gap_quadrant      need-vs-provision typology: priority | high_need_served | low_low | well_served

It also runs:
  - a SENSITIVITY analysis over alternative need weightings (rank stability), and
  - a VALIDATION against held-out signals: does the gap ranking agree with signals that
    were NOT used to build it — chiefly adult inactivity, the activity outcome held out of
    the need composite — and does the facility layer corroborate it? (D-012)

Design notes carried from the proposal / D-010, D-012:
  - provision is the COMMUNITY-SESSION layer only; the facility layer is used for
    corroboration, never merged into the gap index.
  - need EXCLUDES adult inactivity: it is held out of the composite so it can serve as an
    INDEPENDENT validation outcome. A validation anchor must never also be a need input,
    or the check is circular (D-012). Deprivation stays IN need and so is deliberately NOT
    a validation anchor. NB pct_econ_inactive (economic inactivity, Census) is a need
    demographic and is distinct from pct_inactive_adults (physical inactivity, held out).
  - provision is log-transformed before standardising (right-skewed even at borough).
  - City of London is an outlier (tiny residential population); by default it is
    excluded from the standardisation parameters and flagged, then placed on that scale.
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd

# ----------------------------------------------------------------- analysis config
# Need indicators, grouped. All are oriented so that HIGHER = MORE NEED.
# NB: adult inactivity (pct_inactive_adults) is deliberately NOT a need group — it is held
# out as the independent validation outcome (D-012). Adding it here would make the
# validation circular. Deprivation and demographics are the only need constructs.
NEED_GROUPS = {
    "deprivation": ["imd_avg_score"],
    "demographic": ["pct_aged_65_plus", "pct_disabled", "pct_bad_health", "pct_econ_inactive"],
}
# Group-level weightings. The base is "equal"; the others probe sensitivity.
# With inactivity held out (D-012), the surviving need groups are deprivation + demographic;
# the alternatives probe how the ranking moves when each is emphasised in turn.
NEED_WEIGHTINGS = {
    "equal":           {"deprivation": 1, "demographic": 1},
    "deprivation_led": {"deprivation": 2, "demographic": 1},
    "demographic_led": {"deprivation": 1, "demographic": 2},
}
BASE_WEIGHTING = "equal"

PROVISION_PRIMARY = "sessions_per_10k"     # community-session provision (Layer 1)
PROVISION_TRANSFORM = "log1p"              # transform-before-standardise

# Validation anchors must be HELD OUT of the need composite (D-012), else the check is
# circular. Inactivity is held out for exactly this purpose; deprivation is a need input and
# is intentionally NOT listed. Add only further held-out OUTCOME columns here (e.g. OHID
# Fingertips activity indicators not used in need) — never a need input.
VALIDATION_SIGNALS = ["pct_inactive_adults"]
FACILITY_MEASURE = "facilities_per_10k"    # Layer 2, corroboration only
PRIORITY_K = 10                            # "priority" boroughs = top-K by gap (for stability)
EXCLUDE_CITY_FROM_SCALING = True           # compute z params on non-City boroughs


# ----------------------------------------------------------------- helpers
def _num(s):
    return pd.to_numeric(s, errors="coerce")


def zscore(s: pd.Series, mask: pd.Series | None = None) -> pd.Series:
    """Standardise. If mask given, mean/sd are computed on the masked subset only."""
    s = _num(s)
    base = s[mask] if mask is not None else s
    mu, sd = base.mean(), base.std(ddof=0)
    if not np.isfinite(sd) or sd == 0:
        return s * 0.0
    return (s - mu) / sd


def _transform(s: pd.Series) -> pd.Series:
    s = _num(s)
    if PROVISION_TRANSFORM == "log1p":
        return np.log1p(s.clip(lower=0))
    if PROVISION_TRANSFORM == "sqrt":
        return np.sqrt(s.clip(lower=0))
    return s


# ----------------------------------------------------------------- need composite
def build_need(df: pd.DataFrame, weighting: str, scale_mask=None) -> pd.Series:
    """Weighted, standardised need composite. Indicators already higher = more need."""
    w = NEED_WEIGHTINGS[weighting]
    group_scores, weights = [], []
    for group, cols in NEED_GROUPS.items():
        present = [c for c in cols if c in df.columns and df[c].notna().any()]
        if not present:
            continue
        z = pd.concat([zscore(df[c], scale_mask) for c in present], axis=1)
        group_scores.append(z.mean(axis=1))        # equal weight within a group
        weights.append(w[group])
    if not group_scores:
        return pd.Series(np.nan, index=df.index)
    stacked = pd.concat(group_scores, axis=1)
    raw = np.average(stacked, axis=1, weights=weights)
    return zscore(pd.Series(raw, index=df.index), scale_mask)   # re-standardise


# ----------------------------------------------------------------- provision score
def build_provision(df: pd.DataFrame, scale_mask=None) -> pd.Series:
    if PROVISION_PRIMARY not in df.columns:
        warnings.warn(f"provision column '{PROVISION_PRIMARY}' missing; provision = NaN")
        return pd.Series(np.nan, index=df.index)
    return zscore(_transform(df[PROVISION_PRIMARY]), scale_mask)


# ----------------------------------------------------------------- typology
def quadrant(need_z: pd.Series, prov_z: pd.Series) -> pd.Series:
    nh = need_z > need_z.median()
    ph = prov_z > prov_z.median()
    out = pd.Series(index=need_z.index, dtype="object")
    out[nh & ~ph] = "priority"               # high need, low provision
    out[nh & ph] = "high_need_served"
    out[~nh & ~ph] = "low_low"
    out[~nh & ph] = "well_served"
    return out


# ----------------------------------------------------------------- orchestrate
def run(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    df = df.copy().reset_index(drop=True)
    if "is_city_of_london" not in df.columns:
        df["is_city_of_london"] = df.get("lad_code", pd.Series(index=df.index)).eq("E09000001")
    mask = ~df["is_city_of_london"].astype(bool) if EXCLUDE_CITY_FROM_SCALING else None

    need = build_need(df, BASE_WEIGHTING, mask)
    prov = build_provision(df, mask)
    gap = need - prov

    out = pd.DataFrame({"lad_code": df.get("lad_code"), "lad_name": df.get("lad_name")})
    out["need_score_z"] = need
    out["provision_score_z"] = prov
    out["gap_index_z"] = gap
    out["gap_index_rank"] = gap.rank(ascending=False, method="min").astype("Int64")
    # rank/percentile-based version (robustness): need percentile minus provision percentile
    out["gap_pct_based"] = need.rank(pct=True) - prov.rank(pct=True)
    out["gap_quadrant"] = quadrant(need, prov)
    out["is_city_of_london"] = df["is_city_of_london"].values

    # ---- sensitivity: gap ranking under each weighting, vs the base ----
    rankings = {}
    for wname in NEED_WEIGHTINGS:
        g = build_need(df, wname, mask) - prov
        rankings[wname] = g.rank(ascending=False, method="min")
        out[f"gap_rank_{wname}"] = rankings[wname].astype("Int64")
    base_rank = rankings[BASE_WEIGHTING]
    sens = {w: round(base_rank.corr(r, method="spearman"), 3)
            for w, r in rankings.items() if w != BASE_WEIGHTING}
    # boroughs in the top-K gap under EVERY weighting (the stable priority set)
    topk_sets = [set(r.nsmallest(PRIORITY_K).index) for r in rankings.values()]
    stable_idx = set.intersection(*topk_sets) if topk_sets else set()
    stable_priority = sorted(out.loc[list(stable_idx), "lad_code"].dropna().tolist())

    # ---- validation by triangulation ----
    val_mask = ~df["is_city_of_london"].astype(bool)     # judge agreement on non-outlier boroughs
    validation = {}
    for sig in VALIDATION_SIGNALS:
        if sig in df.columns and df[sig].notna().sum() > 2:
            validation[sig] = round(gap[val_mask].corr(_num(df[sig])[val_mask], method="spearman"), 3)
    # facility corroboration: thin sessions AND thin facilities = compounded disadvantage
    facility = {}
    if FACILITY_MEASURE in df.columns and df[FACILITY_MEASURE].notna().sum() > 2:
        fac = _num(df[FACILITY_MEASURE])
        facility["spearman_gap_vs_facilities"] = round(
            gap[val_mask].corr(fac[val_mask], method="spearman"), 3)   # expect NEGATIVE
        out["facility_corroborates"] = (gap > gap.median()) & (fac < fac.median())

    report = {
        "sensitivity_spearman_vs_base": sens,
        "stable_priority_boroughs": stable_priority,
        "validation_spearman": validation,
        "facility_corroboration": facility,
        "n_boroughs": int(len(df)),
        "city_excluded_from_scaling": bool(EXCLUDE_CITY_FROM_SCALING),
    }
    return out.sort_values("gap_index_rank").reset_index(drop=True), report
