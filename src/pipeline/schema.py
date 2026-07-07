"""
schema.py — declarative, dependency-free schema validation for the pipeline's
artefacts (closes WS1 audit gap 5: "assertion-based tests only, no schema
enforcement"). Deliberately implemented without pandera to honour the
no-new-dependencies rule; the check vocabulary below covers what the project
actually needs: column presence, kind (numeric/bool/string), nullability,
ranges, key uniqueness, row-count expectations, set membership, and
cross-column identities.

Usage (wired into run_pipeline / run_analysis / export_ws3_inputs):
    from .schema import validate, BOROUGH_FEATURES
    validate(df, BOROUGH_FEATURES, "borough_features")   # raises SchemaError

Every failure is collected before raising, so one run reports ALL problems.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


class SchemaError(AssertionError):
    """Raised when an artefact violates its declared schema."""


@dataclass
class Col:
    """Expectations for one column."""
    name: str
    kind: str = "any"                 # numeric | bool | string | any
    nullable: bool = True
    min: float | None = None          # applied to non-null numeric values
    max: float | None = None
    unique: bool = False
    isin: set | None = None           # allowed values (non-null)
    prefix: str | None = None         # string prefix (non-null)


@dataclass
class Schema:
    cols: list[Col]
    n_rows: int | None = None         # exact expected row count (None = any)
    min_rows: int = 1
    checks: list = field(default_factory=list)   # [(label, fn(df)->bool)]


def _kind_ok(s: pd.Series, kind: str) -> bool:
    if kind == "any":
        return True
    if kind == "numeric":
        return pd.to_numeric(s, errors="coerce").notna().sum() >= s.notna().sum()
    if kind == "bool":
        return s.dropna().astype(str).str.lower().isin(["true", "false", "0", "1"]).all()
    if kind == "string":
        return True                    # anything renders as string; presence is the check
    raise ValueError(f"unknown kind {kind!r}")


def validate(df: pd.DataFrame, schema: Schema, name: str, verbose: bool = True) -> int:
    """Validate df against schema; raise SchemaError listing every failure.
    Returns the number of checks performed (for the sanity block)."""
    fails: list[str] = []
    n_checks = 0

    n_checks += 1
    if schema.n_rows is not None and len(df) != schema.n_rows:
        fails.append(f"row count {len(df)} != expected {schema.n_rows}")
    elif len(df) < schema.min_rows:
        fails.append(f"row count {len(df)} < minimum {schema.min_rows}")

    for c in schema.cols:
        n_checks += 1
        if c.name not in df.columns:
            fails.append(f"missing column: {c.name}")
            continue
        s = df[c.name]
        if not _kind_ok(s, c.kind):
            fails.append(f"{c.name}: not {c.kind}")
        if not c.nullable and s.isna().any():
            fails.append(f"{c.name}: {int(s.isna().sum())} nulls (declared non-nullable)")
        if c.kind == "numeric" and (c.min is not None or c.max is not None):
            v = pd.to_numeric(s, errors="coerce").dropna()
            if c.min is not None and (v < c.min).any():
                fails.append(f"{c.name}: {int((v < c.min).sum())} values < {c.min}")
            if c.max is not None and (v > c.max).any():
                fails.append(f"{c.name}: {int((v > c.max).sum())} values > {c.max}")
        if c.unique and s.dropna().duplicated().any():
            fails.append(f"{c.name}: duplicate values in key column")
        if c.isin is not None and (~s.dropna().isin(c.isin)).any():
            bad = sorted(set(s.dropna()) - c.isin)[:3]
            fails.append(f"{c.name}: values outside allowed set, e.g. {bad}")
        if c.prefix is not None and (~s.dropna().astype(str).str.startswith(c.prefix)).any():
            fails.append(f"{c.name}: values without prefix {c.prefix!r}")

    for label, fn in schema.checks:
        n_checks += 1
        try:
            if not bool(fn(df)):
                fails.append(f"cross-check failed: {label}")
        except Exception as e:                      # noqa: BLE001 — report, don't crash
            fails.append(f"cross-check errored: {label} ({e})")

    if fails:
        raise SchemaError(f"[schema:{name}] {len(fails)} violation(s):\n  - "
                          + "\n  - ".join(fails))
    if verbose:
        print(f"[schema:{name}] OK — {n_checks} checks, {len(df)} rows")
    return n_checks


# ------------------------------------------------------------------ pct helper
def _pcts(names: list[str]) -> list[Col]:
    return [Col(n, "numeric", min=0.0, max=1.0) for n in names]


QUADRANTS = {"priority", "high_need_served", "low_low", "well_served"}

# ------------------------------------------------------------------ schemas
BOROUGH_FEATURES = Schema(
    n_rows=33,
    cols=[
        Col("lad_code", "string", nullable=False, unique=True, prefix="E09"),
        Col("lad_name", "string", nullable=False),
        Col("population", "numeric", nullable=False, min=1_000, max=1_000_000),
        *_pcts(["pct_aged_65_plus", "pct_disabled", "pct_bad_health",
                "pct_econ_inactive", "pct_ethnic_minority",
                "pct_inactive_adults", "pct_sessions_free"]),
        Col("imd_avg_score", "numeric", min=0, max=60),
        Col("n_sessions", "numeric", min=0),
        Col("sessions_per_10k", "numeric", min=0),
        Col("mean_ptal", "numeric", min=0, max=8),
        Col("median_price_paid", "numeric", min=0.01),   # paid-only by construction;
                                                          # a 0 here = zeros contamination
        Col("is_city_of_london", "bool", nullable=False),
    ],
    checks=[
        ("exactly one City of London flag",
         lambda d: d["is_city_of_london"].astype(str).str.lower().isin(["true", "1"]).sum() == 1),
        ("sessions sum plausible (>0 overall)",
         lambda d: pd.to_numeric(d["n_sessions"], errors="coerce").fillna(0).sum() > 0),
    ],
)

GAP_INDEX = Schema(
    n_rows=33,
    cols=[
        Col("lad_code", "string", nullable=False, unique=True, prefix="E09"),
        Col("need_score_z", "numeric", nullable=False, min=-6, max=6),
        Col("provision_score_z", "numeric", min=-6, max=6),
        Col("gap_index_z", "numeric", min=-8, max=8),
        Col("gap_index_rank", "numeric", min=1, max=33),
        Col("gap_quadrant", "string", isin=QUADRANTS),   # NA allowed (City)
        Col("is_city_of_london", "bool", nullable=False),
    ],
    checks=[
        ("gap identity: gap = need - provision (scored rows, 1e-9)",
         lambda d: ((pd.to_numeric(d.gap_index_z, errors="coerce")
                     - (pd.to_numeric(d.need_score_z, errors="coerce")
                        - pd.to_numeric(d.provision_score_z, errors="coerce")))
                    .abs().dropna() < 1e-9).all()),
        ("ranks are a permutation of 1..n_scored",
         lambda d: sorted(pd.to_numeric(d.gap_index_rank, errors="coerce").dropna()
                          .astype(int)) == list(range(1, int(
                              pd.to_numeric(d.gap_index_rank, errors="coerce").notna().sum()) + 1))),
        ("unscored rows (City) carry no quadrant",
         lambda d: d.loc[pd.to_numeric(d.provision_score_z, errors="coerce").isna(),
                         "gap_quadrant"].isna().all()),
    ],
)

LONDON_SESSIONS = Schema(
    min_rows=100,
    cols=[
        Col("id", nullable=False, unique=True),
        Col("latitude", "numeric", nullable=False, min=51.2, max=51.8),
        Col("longitude", "numeric", nullable=False, min=-0.6, max=0.4),
        Col("price", "numeric", min=0),
        Col("is_free", "bool", nullable=False),
        Col("location_name", "string", nullable=False),
        Col("coord_valid", "bool", nullable=False),
    ],
    checks=[
        ("is_free consistent with price==0 (where price present)",
         lambda d: (d.loc[pd.to_numeric(d.price, errors="coerce").notna(), "is_free"]
                    .astype(str).str.lower().eq("true")
                    == pd.to_numeric(d.price, errors="coerce").dropna().eq(0)).all()),
    ],
)

WS3_ENRICHED = Schema(
    min_rows=100,
    cols=[
        Col("id", nullable=False, unique=True),
        Col("lad_code", "string", nullable=False, prefix="E09"),
        Col("gap_index_z", "numeric", nullable=False),
        Col("gap_quadrant", "string", nullable=False, isin=QUADRANTS),
        Col("is_priority_borough", "bool", nullable=False),
        Col("price", "numeric", min=0),
    ],
    checks=[
        ("priority flag consistent with quadrant",
         lambda d: (d.is_priority_borough.astype(str).str.lower().eq("true")
                    == d.gap_quadrant.eq("priority")).all()),
    ],
)
