"""
incremental_validity.py — is the activity-gap index *more than deprivation relabelled*?

The held-out validation (D-012) shows the gap correlates with adult inactivity it was
never built from. But because deprivation and demographics themselves predict inactivity,
the sharp question remains: does the *provision* layer add predictive signal for inactivity
BEYOND need alone? This module answers it on the 32 non-City boroughs, three ways:

  1. Partial Spearman correlation of provision (and of the gap) with inactivity, controlling
     for need — rank-based, robust at n=32.
  2. Nested OLS: M1 (inactivity ~ need) vs M2 (inactivity ~ need + provision) — the provision
     coefficient with its 95% CI, the incremental R², and the nested F-test; plus the
     single-predictor comparison R²(gap) vs R²(need).
  3. Moran's I on the M2 residuals (queen contiguity) — a spatial-autocorrelation caveat.

It reports effect sizes AND uncertainty (n=32 is small — never lean on p-values alone), makes
NO causal claim, and treats a null as a real finding. Reads the WS2 outputs; writes
reports/incremental_validity.csv (every number code-generated, per Rule Zero).

Run:  python -m src.incremental_validity
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from scipy import stats

from .pipeline import config as C

# The analysis set and the three roles (see docs/decision-log.md, D-012).
NEED = "need_score_z"
PROVISION = "provision_score_z"
GAP = "gap_index_z"
OUTCOME = "pct_inactive_adults"       # held-out validation target


# ============================================================ statistics
def _ranks(a: np.ndarray) -> np.ndarray:
    return stats.rankdata(np.asarray(a, float))


def partial_spearman(x, y, z) -> dict:
    """First-order partial Spearman correlation of x and y, controlling for z.

    Rank-transform, then apply the first-order partial-correlation formula. Returns the
    coefficient, its two-sided p-value (t with df = n - 3), and n.
    """
    rx, ry, rz = _ranks(x), _ranks(y), _ranks(z)
    rxy = np.corrcoef(rx, ry)[0, 1]
    rxz = np.corrcoef(rx, rz)[0, 1]
    ryz = np.corrcoef(ry, rz)[0, 1]
    denom = np.sqrt((1 - rxz**2) * (1 - ryz**2))
    r = (rxy - rxz * ryz) / denom if denom > 0 else np.nan
    n = len(rx)
    df = n - 3                         # n - 2 - (1 controlled variable)
    if np.isfinite(r) and abs(r) < 1 and df > 0:
        t = r * np.sqrt(df / (1 - r**2))
        p = float(2 * stats.t.sf(abs(t), df))
    else:
        p = np.nan
    return {"r": float(r), "p": p, "n": int(n), "df": int(df)}


def spearman(x, y) -> float:
    return float(stats.spearmanr(x, y).statistic)


def ols(X, y, names: list[str]) -> dict:
    """Ordinary least squares with an intercept, from first principles (numpy).

    X: (n, k) predictors WITHOUT an intercept column; `names` names those k columns.
    Returns coefficients (intercept first), standard errors, t, two-sided p, 95% CIs,
    R², adjusted R², residual sum of squares, residuals, and params/df. Cross-checked
    against scikit-learn and a hand computation in the test suite.
    """
    X = np.atleast_2d(np.asarray(X, float))
    if X.shape[0] != len(y):
        X = X.T
    y = np.asarray(y, float)
    n = len(y)
    Xd = np.column_stack([np.ones(n), X])           # add intercept
    k = Xd.shape[1]                                  # params incl. intercept
    beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    resid = y - Xd @ beta
    rss = float(resid @ resid)
    tss = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - rss / tss if tss > 0 else np.nan
    adj_r2 = 1 - (rss / (n - k)) / (tss / (n - 1)) if (tss > 0 and n > k) else np.nan
    sigma2 = rss / (n - k)
    xtx_inv = np.linalg.inv(Xd.T @ Xd)
    se = np.sqrt(np.diag(sigma2 * xtx_inv))
    with np.errstate(divide="ignore", invalid="ignore"):
        t = beta / se
    p = 2 * stats.t.sf(np.abs(t), df=n - k)
    tcrit = stats.t.ppf(0.975, df=n - k)
    return {
        "names": ["intercept", *names],
        "beta": beta, "se": se, "t": t, "p": p,
        "ci_low": beta - tcrit * se, "ci_high": beta + tcrit * se,
        "r2": float(r2), "adj_r2": float(adj_r2), "rss": rss,
        "resid": resid, "n": int(n), "k": int(k),
    }


def nested_f(rss_reduced: float, rss_full: float, k_reduced: int, k_full: int, n: int) -> dict:
    """F-test for the extra predictors in the full model vs the reduced (nested) model."""
    dfn = k_full - k_reduced
    dfd = n - k_full
    F = ((rss_reduced - rss_full) / dfn) / (rss_full / dfd)
    p = float(stats.f.sf(F, dfn, dfd))
    return {"F": float(F), "p": p, "dfn": int(dfn), "dfd": int(dfd)}


# ============================================================ spatial autocorrelation
def queen_weights(geoms) -> np.ndarray:
    """Row-standardised queen contiguity (polygons sharing any boundary point) for `geoms`,
    in the order given. A tiny buffer makes the touch test robust to boundary slivers."""
    geoms = list(geoms)
    n = len(geoms)
    W = np.zeros((n, n))
    buffered = [g.buffer(1e-6) for g in geoms]          # metres in EPSG:27700
    for a in range(n):
        for b in range(a + 1, n):
            if buffered[a].intersects(buffered[b]):
                W[a, b] = W[b, a] = 1.0
    rs = W.sum(axis=1, keepdims=True)
    rs[rs == 0] = 1.0                                    # isolate any island rather than divide by 0
    return W / rs


def morans_i(x, W) -> dict:
    """Moran's I with an analytic (normality) z-score. `W` is row-standardised.

    Returns I, its expectation E[I] = -1/(n-1), the variance, z and a two-sided p.
    A small-sample normal approximation — reported as a caveat, not a hard test.
    """
    x = np.asarray(x, float)
    n = len(x)
    z = x - x.mean()
    den = float((z**2).sum())
    S0 = float(W.sum())
    if den == 0 or S0 == 0:
        return {"I": np.nan, "EI": np.nan, "z": np.nan, "p": np.nan, "n": n}
    mi = (n / S0) * float(z @ (W @ z)) / den
    EI = -1.0 / (n - 1)
    S1 = 0.5 * float(((W + W.T) ** 2).sum())
    S2 = float(((W.sum(axis=1) + W.sum(axis=0)) ** 2).sum())
    var = (n**2 * S1 - n * S2 + 3 * S0**2) / ((n**2 - 1) * S0**2) - EI**2
    zscore = (mi - EI) / np.sqrt(var) if var > 0 else np.nan
    p = float(2 * stats.norm.sf(abs(zscore))) if np.isfinite(zscore) else np.nan
    return {"I": float(mi), "EI": float(EI), "var": float(var), "z": float(zscore), "p": p, "n": n}


# ============================================================ orchestration
def run(features: pd.DataFrame, gap: pd.DataFrame, boundaries=None) -> dict:
    """Run the incremental-validity analysis on the non-City boroughs.

    features: borough_features.csv (needs `pct_inactive_adults`).
    gap:      borough_gap_index.csv (needs need/provision/gap z-scores, is_city_of_london).
    boundaries: optional GeoDataFrame[lad_code, geometry] for Moran's I.
    """
    df = gap.merge(features[["lad_code", OUTCOME]], on="lad_code", how="left")
    df = df[~df["is_city_of_london"].astype(bool)].copy()
    df = df.dropna(subset=[NEED, PROVISION, GAP, OUTCOME]).reset_index(drop=True)
    n = len(df)
    need, prov, gapz, y = df[NEED], df[PROVISION], df[GAP], df[OUTCOME]

    # ---- 1. bivariate context (rank + linear) ----
    biv = {
        "spearman_need_vs_inact": spearman(need, y),
        "spearman_provision_vs_inact": spearman(prov, y),
        "spearman_gap_vs_inact": spearman(gapz, y),
        "spearman_provision_vs_need": spearman(prov, need),
        "pearson_need_vs_inact": float(np.corrcoef(need, y)[0, 1]),
        "pearson_gap_vs_inact": float(np.corrcoef(gapz, y)[0, 1]),
    }

    # ---- 2. partial correlations (the primary, robust test) ----
    partial = {
        "provision_given_need": partial_spearman(prov, y, need),
        "gap_given_need": partial_spearman(gapz, y, need),
    }

    # ---- 3. nested OLS: does provision add to need? ----
    m1 = ols(need.to_numpy(), y.to_numpy(), [NEED])
    m2 = ols(df[[NEED, PROVISION]].to_numpy(), y.to_numpy(), [NEED, PROVISION])
    ftest = nested_f(m1["rss"], m2["rss"], m1["k"], m2["k"], n)
    prov_idx = m2["names"].index(PROVISION)
    provision_coef = {
        "beta": float(m2["beta"][prov_idx]), "se": float(m2["se"][prov_idx]),
        "p": float(m2["p"][prov_idx]),
        "ci_low": float(m2["ci_low"][prov_idx]), "ci_high": float(m2["ci_high"][prov_idx]),
    }
    # single-predictor framing: gap vs need alone
    m_gap = ols(gapz.to_numpy(), y.to_numpy(), [GAP])
    models = {
        "M1_need": {"r2": m1["r2"], "adj_r2": m1["adj_r2"]},
        "M2_need_provision": {"r2": m2["r2"], "adj_r2": m2["adj_r2"]},
        "delta_r2": m2["r2"] - m1["r2"],
        "delta_adj_r2": m2["adj_r2"] - m1["adj_r2"],
        "nested_F": ftest,
        "provision_coef": provision_coef,
        "single_pred_r2_need": m1["r2"],
        "single_pred_r2_gap": m_gap["r2"],
    }

    # ---- 4. Moran's I on M2 residuals (spatial caveat) ----
    moran = None
    if boundaries is not None:
        b = boundaries.to_crs("EPSG:27700") if boundaries.crs and boundaries.crs.to_epsg() != 27700 else boundaries
        b = df[["lad_code"]].merge(b, on="lad_code", how="left")
        if b["geometry"].notna().all():
            import geopandas as gpd
            W = queen_weights(gpd.GeoSeries(b["geometry"], crs="EPSG:27700"))
            moran = morans_i(m2["resid"], W)
            moran["mean_neighbours"] = float((W > 0).sum(axis=1).mean())
        else:
            warnings.warn("Moran's I skipped: boundaries missing for some analysis boroughs.")

    # ---- 5. calibrated verdict ----
    pgn = partial["provision_given_need"]
    adds = (np.isfinite(pgn["r"]) and pgn["r"] < 0 and pgn["p"] < 0.05
            and models["delta_r2"] > 0
            and biv["spearman_gap_vs_inact"] > biv["spearman_need_vs_inact"])
    verdict = {
        "provision_adds_signal_rankbased": bool(adds),
        "headline": _headline(adds, pgn, models, biv),
    }

    return {"n": n, "bivariate": biv, "partial": partial, "models": models,
            "moran": moran, "verdict": verdict}


def _headline(adds: bool, pgn: dict, models: dict, biv: dict) -> str:
    par = f"partial ρ(provision, inactivity | need) = {pgn['r']:+.3f} (p={pgn['p']:.3f})"  # noqa
    fp = models["nested_F"]["p"]
    dr2 = models["delta_r2"]
    if adds:
        return (f"Provision ADDS independent signal beyond need — the gap is more than "
                f"deprivation relabelled (rank-based: {par}; gap·ι {biv['spearman_gap_vs_inact']:+.2f} "
                f"> need·ι {biv['spearman_need_vs_inact']:+.2f}). Parametric: ΔR²={dr2:+.3f}, "
                f"nested-F p={fp:.3f} — {'concordant' if fp < 0.05 else 'weaker (marginal at n=32)'}.")
    return (f"No clear incremental signal from provision beyond need (rank-based {par}; "
            f"ΔR²={dr2:+.3f}, nested-F p={fp:.3f}). Honest null at n=32 — report as a finding, "
            f"not a failure; low power means a modest effect cannot be excluded.")


def to_rows(res: dict) -> pd.DataFrame:
    """Flatten the result into a tidy metric/value/detail table for reports/."""
    rows = [("n_boroughs", res["n"], "non-City boroughs")]
    for k, v in res["bivariate"].items():
        rows.append((k, round(v, 4), "correlation"))
    for name, d in res["partial"].items():
        rows.append((f"partial_{name}_r", round(d["r"], 4), f"partial Spearman (p={d['p']:.4f})"))
    m = res["models"]
    rows += [
        ("R2_M1_need", round(m["M1_need"]["r2"], 4), "inactivity ~ need"),
        ("R2_M2_need_provision", round(m["M2_need_provision"]["r2"], 4), "inactivity ~ need + provision"),
        ("delta_R2", round(m["delta_r2"], 4), "incremental R² from provision"),
        ("delta_adj_R2", round(m["delta_adj_r2"], 4), "incremental adjusted R²"),
        ("nested_F", round(m["nested_F"]["F"], 4), f"df=({m['nested_F']['dfn']},{m['nested_F']['dfd']})"),
        ("nested_F_p", round(m["nested_F"]["p"], 4), "provision improves the model?"),
        ("provision_beta", round(m["provision_coef"]["beta"], 4), "M2 standardized coef"),
        ("provision_beta_ci", f"[{m['provision_coef']['ci_low']:.3f}, {m['provision_coef']['ci_high']:.3f}]", "95% CI"),
        ("provision_beta_p", round(m["provision_coef"]["p"], 4), "expect negative"),
        ("R2_single_need", round(m["single_pred_r2_need"], 4), "inactivity ~ need only"),
        ("R2_single_gap", round(m["single_pred_r2_gap"], 4), "inactivity ~ gap only"),
    ]
    if res["moran"]:
        mo = res["moran"]
        rows += [
            ("morans_I_residuals", round(mo["I"], 4), f"E[I]={mo['EI']:.4f}, mean nbrs={mo.get('mean_neighbours', float('nan')):.1f}"),
            ("morans_I_z", round(mo["z"], 4), f"p={mo['p']:.4f} (normal approx.)"),
        ]
    rows.append(("verdict", res["verdict"]["provision_adds_signal_rankbased"], res["verdict"]["headline"]))
    return pd.DataFrame(rows, columns=["metric", "value", "detail"])


def _figure(features: pd.DataFrame, gap: pd.DataFrame, dest) -> None:
    """Scatter of need-vs-inactivity and gap-vs-inactivity (best-effort; never blocks the run)."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        df = gap.merge(features[["lad_code", OUTCOME]], on="lad_code")
        df = df[~df["is_city_of_london"].astype(bool)]
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
        for ax, col, title in [(axes[0], NEED, "Need vs inactivity"),
                               (axes[1], GAP, "Gap vs inactivity")]:
            ax.scatter(df[col], df[OUTCOME] * 100, s=18)
            ax.set_xlabel(col)
            ax.set_ylabel("adult inactivity (%)")
            ax.set_title(title)
        fig.suptitle("Incremental validity — held-out inactivity (non-City, n=32)")
        fig.tight_layout()
        fig.savefig(dest, dpi=130)
        plt.close(fig)
    except Exception as e:                       # noqa: BLE001 — plotting must never fail the analysis
        warnings.warn(f"figure skipped: {e}")


def main() -> int:
    feats = C.PATHS["output"]
    gap_path = C.PROCESSED / "borough_gap_index.csv"
    if not feats.exists() or not gap_path.exists():
        print("ERROR: run `python -m src.run_pipeline` then `python -m src.run_analysis` first.")
        return 1
    features = pd.read_csv(feats)
    gap = pd.read_csv(gap_path)

    boundaries = None
    try:
        from .pipeline.pipeline import load_geography
        _, boundaries = load_geography()
    except Exception as e:                        # noqa: BLE001
        warnings.warn(f"boundaries unavailable; Moran's I skipped: {e}")

    if OUTCOME not in features.columns or features[OUTCOME].notna().sum() < 10:
        print(f"ERROR: '{OUTCOME}' not populated — acquire the Active Lives inactivity export first.")
        return 1

    res = run(features, gap, boundaries)
    table = to_rows(res)

    dest = C.ROOT / "reports" / "incremental_validity.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(dest, index=False)
    _figure(features, gap, dest.with_suffix(".png"))

    pd.set_option("display.width", 200, "display.max_colwidth", 60)
    print(f"\nIncremental-validity check — n={res['n']} non-City boroughs")
    print(f"Wrote {dest}\n")
    print(table.to_string(index=False))
    print("\n— Verdict —")
    print(" ", res["verdict"]["headline"])
    if res["moran"]:
        print(f"\n  Spatial check: Moran's I on residuals = {res['moran']['I']:+.3f} "
              f"(E[I]={res['moran']['EI']:.3f}, z={res['moran']['z']:+.2f}, p={res['moran']['p']:.3f}) — "
              f"{'little' if abs(res['moran']['z']) < 2 else 'notable'} residual spatial autocorrelation.")
    print("\n  Caveats: borough-level, observational (no causal claim); n=32 (low power — "
          "effect sizes and CIs lead, not p-values); inactivity held out of need (D-012).")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
