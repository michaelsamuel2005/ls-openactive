"""
pipeline.py — load each source, resolve it to borough, and merge into one table.

Design choices:
- Every source is optional: if its file is missing, the pipeline WARNS and fills
  that source's columns with NaN, so you can run it before every file is in place.
- Small-area data (Census, IoD) is keyed on the LAD code directly (the bulk Census
  'ltla' files and the IoD LA-summary are already at borough level).
- Point data (sessions, facilities, PTAL) is assigned to a borough by point-in-polygon.
- The activity-gap index, z-scores and E2SFCA are NOT built here — they are the WS2
  analysis step, computed from this table. This pipeline outputs raw + per-capita features.
"""
from __future__ import annotations
import re
import warnings
import pandas as pd
import geopandas as gpd

from . import config as C

ECODE = re.compile(r"^[EWSN]\d{8}$")          # ONS area code pattern


# ============================================================ helpers
def _exists(key: str):
    p = C.PATHS[key]
    if not p.exists():
        warnings.warn(f"[skip] {key}: file not found at {p} — its columns will be NaN.")
        return None
    return p


def _find_code_col(df: pd.DataFrame) -> str:
    """Return the column holding ONS area codes (E09…), by name or by content."""
    for c in df.columns:
        if "code" in c.lower() and df[c].astype(str).str.match(ECODE).mean() > 0.8:
            return c
    for c in df.columns:                      # fallback: any column that looks like codes
        if df[c].astype(str).str.match(ECODE).mean() > 0.8:
            return c
    raise ValueError("No ONS area-code column found.")


def _to_london(df: pd.DataFrame, code_col: str) -> pd.DataFrame:
    """Keep only the 33 London boroughs and standardise the key to `lad_code`."""
    out = df[df[code_col].astype(str).str.startswith(C.LONDON_LAD_PREFIX)].copy()
    out = out.rename(columns={code_col: "lad_code"})
    return out


def _category_cols(df: pd.DataFrame) -> list[str]:
    """Numeric category columns of a Census table (everything except id/name cols)."""
    skip = {"date", "geography", "geography code"}
    cols = []
    for c in df.columns:
        if c.lower() in skip or c == "lad_code":
            continue
        if pd.api.types.is_numeric_dtype(pd.to_numeric(df[c], errors="coerce")):
            cols.append(c)
    return cols


def _match(cols: list[str], needles: list[str]) -> list[str]:
    """Columns whose header contains any needle (case-insensitive)."""
    low = {c: c.lower() for c in cols}
    return [c for c in cols if any(n.lower() in low[c] for n in needles)]


# ============================================================ geography
def load_geography():
    """Return (df[lad_code, lad_name, area_km2], boundaries GeoDataFrame in its own CRS)."""
    bpath = _exists("boundaries")
    if bpath is None:                         # be forgiving of the exact filename
        bdir = C.PATHS["boundaries"].parent
        cands = (sorted(bdir.glob("*.geojson")) + sorted(bdir.glob("*.json"))
                 + sorted(bdir.glob("*.gpkg")) + sorted(bdir.glob("*.shp")))
        if cands:
            bpath = cands[0]
            warnings.warn(f"[boundaries] '{C.PATHS['boundaries'].name}' not found; "
                          f"using '{bpath.name}' from {bdir}")

    if bpath is not None:
        gdf = gpd.read_file(bpath)
        code_col = _find_code_col(gdf)
        gdf = _to_london(gdf, code_col)
        name_col = next((c for c in gdf.columns if c.lower().endswith("nm") or "name" in c.lower()), None)
        gdf["lad_name"] = gdf[name_col] if name_col else gdf["lad_code"]
        # area in km^2 (reproject to a metric CRS first if needed)
        g_med = gdf.to_crs("EPSG:27700") if gdf.crs and gdf.crs.to_epsg() != 27700 else gdf
        gdf["area_km2"] = g_med.geometry.area / 1e6
        spine = gdf[["lad_code", "lad_name", "area_km2"]].reset_index(drop=True)
        return spine, gdf[["lad_code", "geometry"]]

    # No boundary polygons anywhere: fall back to the lookup just to build the borough list.
    lpath = _exists("lookup")
    if lpath is not None:
        lk = pd.read_csv(lpath)
        code = C.LOOKUP_COLS["lad"]
        spine = (lk[[code, C.LOOKUP_COLS["lad_name"]]]
                 .drop_duplicates().rename(columns={code: "lad_code",
                                                    C.LOOKUP_COLS["lad_name"]: "lad_name"}))
        spine = spine[spine.lad_code.str.startswith(C.LONDON_LAD_PREFIX)].reset_index(drop=True)
        spine["area_km2"] = pd.NA
        return spine, None

    raise FileNotFoundError(
        "No boundary file found. Put a LAD boundary file (any *.geojson) in "
        f"{C.PATHS['boundaries'].parent}, or set PATHS['boundaries'] to its exact path.")


# ============================================================ census
def _load_census_table(table: str) -> pd.DataFrame | None:
    p = C.PATHS["census_dir"] / table / f"census2021-{table}-ltla.csv"
    if not p.exists():                          # also accept a flat layout
        alt = C.PATHS["census_dir"] / f"census2021-{table}-ltla.csv"
        p = alt if alt.exists() else p
    if not p.exists():
        warnings.warn(f"[skip] census {table}: not found at {p}")
        return None
    df = pd.read_csv(p)
    df = _to_london(df, _find_code_col(df))
    return df


def _total(df: pd.DataFrame) -> pd.Series:
    cats = _category_cols(df)
    tot = _match(cats, ["Total"])
    if tot:                                     # prefer an explicit Total column
        return pd.to_numeric(df[tot[0]], errors="coerce")
    return df[cats].apply(pd.to_numeric, errors="coerce").sum(axis=1)


def build_census_features(spine: pd.DataFrame) -> pd.DataFrame:
    out = spine[["lad_code"]].copy()
    cache: dict[str, pd.DataFrame] = {}
    for col, spec in C.CENSUS.items():
        tbl = spec["table"]
        df = cache.get(tbl)
        if df is None:
            df = _load_census_table(tbl)
        if df is None:
            out[col] = pd.NA
            continue
        cache[tbl] = df
        df = df.set_index("lad_code")
        total = _total(df.reset_index().set_index("lad_code"))
        if spec.get("take") == "total":
            series = total
        else:
            if spec.get("numerator_exact"):
                num_cols = [c for c in spec["numerator_exact"] if c in df.columns]
            else:
                cats = _category_cols(df.reset_index())
                num_cols = _match(cats, spec.get("numerator_contains", []))
            if not num_cols:
                warnings.warn(f"census {col}: no numerator columns matched -> NaN")
                series = pd.Series(float("nan"), index=df.index)
            else:
                num = df[num_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1)
                series = num if spec.get("as") == "count" else (num / total)
        out = out.merge(series.rename(col), left_on="lad_code", right_index=True, how="left")
    return out


# ============================================================ deprivation (IoD)
def _read_iod_table(p) -> pd.DataFrame:
    """Return the IoD LA-summary table.

    IoD2025 ships File 10 as a multi-sheet .xlsx workbook (a Notes sheet plus one
    summary sheet per index: IMD, Income, Employment, …). We do not hard-code the
    sheet name or the header row: we scan every sheet and pick the first that
    carries BOTH an ONS-code column and an 'average score' column. If the sheet
    has title rows above the header, we re-read it locating the header row.
    A plain .csv (e.g. a hand-exported IMD sheet) is read directly.
    """
    if p.suffix.lower() not in (".xlsx", ".xls"):
        return pd.read_csv(p)

    book = pd.read_excel(p, sheet_name=None, dtype=object)      # needs openpyxl
    for name, sh in book.items():
        low = [str(c).lower() for c in sh.columns]
        has_code = any(sh[c].astype(str).str.match(ECODE).mean() > 0.5 for c in sh.columns)
        if any("average score" in c for c in low) and has_code:
            return sh
    # fallback: some sheets carry a few title rows before the real header
    xls = pd.ExcelFile(p)
    for name in xls.sheet_names:
        raw = pd.read_excel(p, sheet_name=name, header=None, dtype=object)
        for h in range(min(12, len(raw))):                     # search first 12 rows for the header
            header = raw.iloc[h].astype(str).str.lower()
            if header.str.contains("average score").any():
                sh = pd.read_excel(p, sheet_name=name, header=h, dtype=object)
                if any(sh[c].astype(str).str.match(ECODE).mean() > 0.5 for c in sh.columns):
                    return sh
    raise ValueError(
        f"IoD: no sheet in {p.name} has both an ONS-code column and an "
        f"'average score' column. Open the workbook, save the IMD summary sheet "
        f"as CSV, and point PATHS['iod_la'] at that CSV."
    )


def build_iod(spine: pd.DataFrame) -> pd.DataFrame:
    p = _exists("iod_la")
    if p is None:
        return spine[["lad_code"]].assign(imd_avg_score=pd.NA, imd_rank_of_avg=pd.NA)
    df = _read_iod_table(p)
    df = _to_london(df, _find_code_col(df))

    def _col(*needles, exclude=None):
        """First column whose lower-cased name contains all needles and not `exclude`."""
        for c in df.columns:
            cl = str(c).lower()
            if all(n in cl for n in needles) and (exclude is None or exclude not in cl):
                return c
        return None

    # 'IMD - Average score' (not 'rank of average score', not 'average rank')
    avg = _col("average score", exclude="rank")
    # 'IMD - Rank of average score' (full phrase disambiguates from 'rank of average rank')
    rnk = _col("rank of average score")

    out = df[["lad_code"]].copy()
    out["imd_avg_score"]   = pd.to_numeric(df[avg], errors="coerce") if avg else pd.NA
    out["imd_rank_of_avg"] = pd.to_numeric(df[rnk], errors="coerce") if rnk else pd.NA
    if avg is None:
        warnings.warn("IoD: no 'average score' column detected — imd_avg_score is NaN. "
                      "Check the summary sheet's headers.")
    return out


# ============================================================ point assignment
def _assign_to_borough(df: pd.DataFrame, lon, lat, src_crs, boundaries) -> pd.DataFrame:
    """Add a `lad_code` to each point via spatial join onto the borough polygons."""
    pts = gpd.GeoDataFrame(
        df.copy(),
        geometry=gpd.points_from_xy(df[lon], df[lat]),
        crs=src_crs,
    ).to_crs(boundaries.crs)
    joined = gpd.sjoin(pts, boundaries, how="left", predicate="within")
    return joined.drop(columns="index_right", errors="ignore")


# ============================================================ sessions (Open Sessions)
def build_sessions(spine, boundaries) -> pd.DataFrame:
    p = _exists("sessions")
    base = spine[["lad_code"]].copy()
    if p is None or boundaries is None:
        for c in ["n_sessions", "n_venues", "pct_sessions_free", "median_price_paid",
                  "activity_diversity", "pct_sessions_access_info"]:
            base[c] = pd.NA
        return base
    s = C.SESSIONS_COLS
    df = pd.read_csv(p)
    df = _assign_to_borough(df, s["lon"], s["lat"], C.SESSIONS_CRS, boundaries)
    df = df.dropna(subset=["lad_code"])
    price_num = pd.to_numeric(df[s["price"]], errors="coerce")
    # Free-status: the harvester already writes is_free (missing price counted
    # NOT free — the audited definition); reuse it as the single source of
    # truth. Recompute only as a fallback for inputs without the column.
    if "is_free" in df.columns:
        df["_free"] = df["is_free"].astype(str).str.strip().str.lower().isin(["true", "1"])
    else:
        df["_free"] = price_num.fillna(-1).eq(0)
    # Paid-only price (audit F1): median over price > 0 rows ONLY. The old
    # `median_price` mixed £0 sessions into the median — the exact
    # zeros-contamination this project corrected elsewhere. NaN is legitimate
    # for boroughs whose published sessions are all free.
    df["_paid_price"] = price_num.where(price_num > 0)
    df["_acc"] = df[s["access"]].astype(str).str.lower().isin(["1", "true", "yes"])
    g = df.groupby("lad_code")
    feat = pd.DataFrame({
        "n_sessions": g.size(),
        "n_venues": g[s["venue"]].nunique(),
        "pct_sessions_free": g["_free"].mean(),
        "median_price_paid": g["_paid_price"].median(),
        "activity_diversity": g[s["activity"]].nunique(),
        "pct_sessions_access_info": g["_acc"].mean(),
    })
    return base.merge(feat, on="lad_code", how="left")


# ============================================================ facilities (Active Places)
def build_facilities(spine, boundaries) -> pd.DataFrame:
    base = spine[["lad_code"]].copy()
    pf = _exists("ap_facilities")   # sites.csv is not read: n_sites derives
                                    # from the facilities file's site ids (audit F6)
    if pf is None or boundaries is None:
        for c in ["n_sites", "n_facilities", "pct_community_use", *C.AP_FAC_TYPES]:
            base[c] = pd.NA
        return base
    fc = C.AP_FAC_COLS
    fac = pd.read_csv(pf)
    fac = _assign_to_borough(fac, fc["lon"], fc["lat"], C.AP_CRS, boundaries).dropna(subset=["lad_code"])
    fac["_comm"] = fac[fc["community"]].astype(str).str.lower().isin(["1", "true", "yes"])
    g = fac.groupby("lad_code")
    feat = pd.DataFrame({"n_facilities": g.size(),
                         "n_sites": g[fc["site_id"]].nunique(),
                         "pct_community_use": g["_comm"].mean()})
    for col, needles in C.AP_FAC_TYPES.items():
        mask = fac[fc["type"]].astype(str).apply(lambda v: any(n.lower() in v.lower() for n in needles))
        feat[col] = fac[mask].groupby("lad_code").size()
    feat = feat.fillna({c: 0 for c in C.AP_FAC_TYPES})
    return base.merge(feat, on="lad_code", how="left")


# ============================================================ inactivity (LA level)
def build_inactivity(spine) -> pd.DataFrame:
    """Active Lives adult physical-inactivity %, per borough, from an OHID Fingertips
    export. Held OUT of the need composite (D-012): used only as a validation target.

    Fingertips CSVs are wide-and-tall: headers carry spaces ('Area Code',
    'Lower CI 95.0 limit') and there are multiple rows per area — one per Sex
    (Male/Female/Persons) and per time period. We therefore (a) match columns by
    their space-stripped lower-cased name, (b) keep Sex = Persons, and (c) take the
    most recent time period for each borough. Values are 0–100 → stored as a
    proportion to match the Census shares.
    """
    p = _exists("inactivity")
    if p is None:
        return spine[["lad_code"]].assign(pct_inactive_adults=pd.NA,
                                          inactive_ci_lower=pd.NA, inactive_ci_upper=pd.NA)
    df = pd.read_csv(p)

    def _col(*needles, exclude=None):
        for c in df.columns:
            cl = str(c).lower().replace(" ", "")
            if all(n.replace(" ", "") in cl for n in needles) and \
               (exclude is None or exclude.replace(" ", "") not in cl):
                return c
        return None

    code_col = _col("areacode") or _find_code_col(df)
    val_col  = _col("value", exclude="note")
    lo_col   = _col("lower", "ci")
    hi_col   = _col("upper", "ci")
    sex_col  = _col("sex")
    time_col = _col("timeperiod") or _col("time", exclude="sortable")

    df = _to_london(df, code_col)

    # keep the 'Persons' breakdown when a Sex column is present
    if sex_col is not None and df[sex_col].astype(str).str.contains("person", case=False).any():
        df = df[df[sex_col].astype(str).str.contains("person", case=False)]
    # collapse to one row per borough: latest period ('YYYY/YY' sorts chronologically)
    if time_col is not None:
        df = df.sort_values(time_col).groupby("lad_code", as_index=False).tail(1)
    else:
        df = df.drop_duplicates("lad_code")

    out = df[["lad_code"]].copy()
    out["pct_inactive_adults"] = pd.to_numeric(df[val_col], errors="coerce") / 100.0 if val_col else pd.NA
    out["inactive_ci_lower"]   = pd.to_numeric(df[lo_col],  errors="coerce") / 100.0 if lo_col  else pd.NA
    out["inactive_ci_upper"]   = pd.to_numeric(df[hi_col],  errors="coerce") / 100.0 if hi_col  else pd.NA
    if val_col is None:
        warnings.warn("Inactivity: no 'Value' column detected — pct_inactive_adults is NaN.")
    return out


# ============================================================ PTAL (mean grade per borough)
def build_ptal(spine, boundaries) -> pd.DataFrame:
    base = spine[["lad_code"]].copy()
    p = _exists("ptal")
    if p is None or boundaries is None:
        return base.assign(mean_ptal=pd.NA)
    pc = C.PTAL_COLS
    df = (pd.read_excel(p) if str(p).lower().endswith((".xlsx", ".xls"))
          else pd.read_csv(p))
    df["_grade_num"] = df[pc["grade"]].astype(str).map(C.PTAL_GRADE_MAP)
    df = df.dropna(subset=["_grade_num"])
    df = _assign_to_borough(df, pc["lon"], pc["lat"], C.PTAL_CRS, boundaries).dropna(subset=["lad_code"])
    mean = df.groupby("lad_code")["_grade_num"].mean().rename("mean_ptal")
    return base.merge(mean, on="lad_code", how="left")


# ============================================================ orchestrate
def build_features() -> pd.DataFrame:
    spine, boundaries = load_geography()
    df = (spine
          .merge(build_census_features(spine), on="lad_code", how="left")
          .merge(build_iod(spine), on="lad_code", how="left")
          .merge(build_sessions(spine, boundaries), on="lad_code", how="left")
          .merge(build_facilities(spine, boundaries), on="lad_code", how="left")
          .merge(build_inactivity(spine), on="lad_code", how="left")
          .merge(build_ptal(spine, boundaries), on="lad_code", how="left"))

    # ---- per-capita measures (need population to exist) ----
    pop = pd.to_numeric(df.get("population"), errors="coerce")
    if "n_sessions" in df:
        df["sessions_per_10k"] = pd.to_numeric(df["n_sessions"], errors="coerce") / pop * C.PER_CAPITA_BASE
    if "n_facilities" in df:
        df["facilities_per_10k"] = pd.to_numeric(df["n_facilities"], errors="coerce") / pop * C.PER_CAPITA_BASE

    df["is_city_of_london"] = df["lad_code"].eq("E09000001")
    return df.sort_values("lad_code").reset_index(drop=True)
