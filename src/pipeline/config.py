"""
config.py — the single place to set paths and map source columns.

Everything the pipeline needs to know about WHERE files are and WHAT their
columns are called lives here. When a real file's column name differs from the
default below, change it here only — never in the pipeline logic.

Verify the *_CONTAINS substrings against your actual files (open the CSV header
or the metadata .txt that came in each Census zip). They use case-insensitive
"contains" matching, so they are robust to punctuation, but the words must match.
"""
from pathlib import Path

# ---------------------------------------------------------------- paths
# Repo-root-relative. RAW is read-only inputs; PROCESSED is pipeline output.
ROOT = Path(__file__).resolve().parents[2]          # .../ls-openactive
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

PATHS = {
    "lookup":        RAW / "ons_lookup" / "oa_lsoa_msoa_lad_dec2021.csv",
    "boundaries":    RAW / "boundaries" / "lad_2021_bgc.geojson",   # ONS LAD polygons (UK; filtered to E09)
    "census_dir":    RAW / "census2021",     # holds tsXXX/census2021-tsXXX-ltla.csv
    "iod_la":        RAW / "iod2025" / "File_10_-_IoD2025_Local_Authority_District_Summaries__lower-tier__v2.xlsx",
    "sessions":      PROCESSED / "london_sessions_2026-06-30.csv",     # FROZEN 2026-06-30 snapshot (494 rows) — do not repoint without a decision-log entry
    "ap_sites":      RAW / "active_places" / "sites.csv",
    "ap_facilities": RAW / "active_places" / "facilities.csv",
    "ap_facility_types": RAW / "active_places" / "facilitytype.csv",  # code->name lookup shipped in the extract
    "inactivity":    RAW / "active_lives" / "inactivity_la.csv",        # from Fingertips/Active Lives
    "ptal":          RAW / "ptal" / "2015  PTALs Grid Values 280515.xlsx",  # TfL 2015 100m grid (see docs/data-sources.md §8)
    "output":        PROCESSED / "borough_features.csv",
}

# ---------------------------------------------------------------- geography
# London = 33 local authorities. Their LAD codes are E09000001..E09000033.
LONDON_LAD_PREFIX = "E09"
PER_CAPITA_BASE = 10_000          # rates expressed "per 10,000 residents"

# ---------------------------------------------------------------- randomness
# THE single seed for any stochastic step (project rule: seeds live here and
# nowhere else). Currently used only by the validation bootstrap in
# src/ws2_metrics.py; the pipeline itself is deterministic.
RANDOM_SEED = 42

# Column names inside the ONS lookup (check your file's header).
LOOKUP_COLS = {"lsoa": "LSOA21CD", "lad": "LAD22CD", "lad_name": "LAD22NM"}

# ---------------------------------------------------------------- census shares
# Each entry builds one column. `table` is the tsXXX folder name.
# `numerator_contains`: category columns whose header contains ANY of these.
# `denominator`: "total" = auto-detected Total column (else sum of all categories).
CENSUS = {
    "population":        {"table": "ts001",  "take": "total"},
    "pct_aged_65_plus":  {"table": "ts007a", "denominator": "total", "numerator_contains":
                          ["65 to 69", "70 to 74", "75 to 79", "80 to 84", "85 years and over"]},
    "pct_disabled":      {"table": "ts038", "numerator_contains": ["Limited a lot", "Limited a little"],
                          "denominator": "total"},
    "pct_bad_health":    {"table": "ts037", "numerator_contains": ["Bad health", "Very bad health"],
                          "denominator": "total"},
    "pct_econ_inactive": {"table": "ts066", "denominator": "total",
                          "numerator_exact": ["Economic activity status: Economically inactive"]},
    "pct_ethnic_minority": {"table": "ts021", "denominator": "total", "numerator_exact": [
                            "Ethnic group: Asian, Asian British or Asian Welsh",
                            "Ethnic group: Black, Black British, Black Welsh, Caribbean or African",
                            "Ethnic group: Mixed or Multiple ethnic groups",
                            "Ethnic group: Other ethnic group"]},
}

# ---------------------------------------------------------------- IoD (LA summary file)
# NOTE: build_iod() now AUTO-DETECTS the sheet and columns in File 10 (.xlsx) by meaning
# ('average score' for the score; 'rank of average score' for its rank), so it survives
# the IoD2019→IoD2025 header rename (2025 uses 'Local Authority District code (2024)').
# The dict below is kept only as documentation of the expected concepts — it is not used
# for matching. A hand-exported CSV of the IMD sheet works too (same auto-detection).
IOD_COLS = {
    "lad": "Local Authority District code (2024)",   # 2025 vintage; auto-detected regardless
    "avg_score": "IMD - Average score",
    "rank_of_avg": "IMD - Rank of average score",
}

# ---------------------------------------------------------------- point sources (lon/lat + CRS)
# Sessions and Active Places are points -> assigned to borough by point-in-polygon.
SESSIONS_COLS = {"lon": "longitude", "lat": "latitude",
                 "price": "price", "activity": "activity_type",
                 "venue": "location_name", "access": "has_access_info"}
SESSIONS_CRS = "EPSG:4326"

# Verified against the real 2026-07-07 Active Places extract (registered download).
# sites.csv is NOT read by the pipeline (audit F6/F7) — dict kept as documentation.
AP_SITE_COLS = {"lon": "long", "lat": "lat", "site_id": "Site ID"}
AP_FAC_COLS = {"lon": "Longitude", "lat": "Latitude", "site_id": "Site ID",
               "type": "Facility Type", "community": "Accessibility Type Group (Text)",
               "status": "Operational Status"}
AP_CRS = "EPSG:4326"   # verified: Latitude 49.9–55.8, Longitude −6.4–1.8 (WGS84)

# 'Facility Type' arrives as a NUMERIC CODE; the extract ships its own lookup
# (facilitytype.csv: 'Facility Type ID' -> 'Facility Type Name') which
# build_facilities merges before matching. PATHS["ap_facility_types"] points at it.
#
# 'Operational Status' is also coded. Decode VERIFIED 2026-07-07 by exact
# count-match against the text-labelled ArcGIS Hub export of the same vintage
# (124,839 rows in both):
#   1=Planned  2=Under Construction  3=Operational  4=Temporarily Closed
#   5=Closed   7=No Grass Pitches Currently Marked Out  8=Not Known
# Only code 3 counts as current provision (excluding 4/5/7 removes ~21% of rows
# nationally that are not currently usable). Decision-log entry required if changed.
AP_OPERATIONAL_KEEP = {3}

# Community-use flag: 'Accessibility Type Group (Text)' ∈ {Public Access, Private,
# Not Known}. Values (lower-cased) counting as community-accessible:
AP_COMMUNITY_TRUE = {"public access"}

# Facility types to count as their own columns — substring match on the DECODED
# type name. NOTE 'Grass Pitches' (plural, verbatim from the lookup): the
# singular 'Grass Pitch' would also match 'Artificial Grass Pitch' (a separate
# type, ID 8) — verified hazard, do not "simplify" the needle.
AP_FAC_TYPES = {
    "n_fac_sports_halls":   ["Sports Hall"],
    "n_fac_swimming_pools": ["Swimming Pool"],
    "n_fac_grass_pitches":  ["Grass Pitches"],
    "n_fac_health_fitness": ["Health and Fitness"],
}

# ---------------------------------------------------------------- inactivity (LA level)
# NOTE: build_inactivity() auto-detects columns from an OHID Fingertips CSV export
# (real headers carry spaces: 'Area Code', 'Lower CI 95.0 limit'), filters Sex='Persons',
# and takes the latest time period per borough. The dict is documentation only.
INACTIVITY_COLS = {"lad": "Area Code", "value": "Value",
                   "ci_lower": "Lower CI 95.0 limit", "ci_upper": "Upper CI 95.0 limit"}

# ---------------------------------------------------------------- PTAL
# TfL 2015 grid workbook columns: X/Y = BNG Easting/Northing; PTAL2015 = grade
# bands; AI2015 = continuous access index (kept available for E2SFCA later).
PTAL_COLS = {"lon": "X", "lat": "Y", "grade": "PTAL2015"}
PTAL_CRS = "EPSG:27700"   # verified: X 503k–562k, Y 156k–201k (British National Grid)
# PTAL grades are bands (0,1a,1b,2,...,6b). Map to a numeric scale for averaging:
PTAL_GRADE_MAP = {"0": 0, "1a": 1, "1b": 2, "2": 3, "3": 4,
                  "4": 5, "5": 6, "6a": 7, "6b": 8}
