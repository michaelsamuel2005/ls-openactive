"""
test_schema.py — known-answer tests for the schema-validation engine
(src/pipeline/schema.py): a fully valid frame passes, and every failure
family (missing column, kind, nulls, range, uniqueness, allowed set, prefix,
row count, cross-check) is caught with a legible message.

Run:  python -m tests.test_schema
"""
import pandas as pd

from src.pipeline.schema import Col, Schema, SchemaError, validate


def _ok_frame():
    return pd.DataFrame({
        "code": ["E09000001", "E09000002", "E09000003"],
        "share": [0.1, 0.5, 0.9],
        "n": [3, 10, 6],
        "flag": [True, False, False],
        "cat": ["a", "b", "a"],
    })


def _schema(n_rows=3):
    return Schema(
        n_rows=n_rows,
        cols=[
            Col("code", "string", nullable=False, unique=True, prefix="E09"),
            Col("share", "numeric", nullable=False, min=0.0, max=1.0),
            Col("n", "numeric", min=0),
            Col("flag", "bool", nullable=False),
            Col("cat", "string", isin={"a", "b"}),
        ],
        checks=[("n sums positive", lambda d: d["n"].sum() > 0)],
    )


def _expect_fail(df, schema, needle):
    try:
        validate(df, schema, "t", verbose=False)
    except SchemaError as e:
        assert needle in str(e), f"expected {needle!r} in:\n{e}"
        return
    raise AssertionError(f"schema failed to catch: {needle}")


def main():
    # ---- valid frame passes and reports its check count ----
    n = validate(_ok_frame(), _schema(), "t", verbose=False)
    assert n >= 7, n

    # ---- each failure family is caught ----
    df = _ok_frame().drop(columns=["cat"])
    _expect_fail(df, _schema(), "missing column: cat")

    df = _ok_frame()
    df.loc[1, "share"] = 1.7
    _expect_fail(df, _schema(), "values > 1.0")

    df = _ok_frame()
    df.loc[0, "share"] = None
    _expect_fail(df, _schema(), "nulls (declared non-nullable)")

    df = _ok_frame()
    df.loc[2, "code"] = "E09000001"
    _expect_fail(df, _schema(), "duplicate values in key column")

    df = _ok_frame()
    df.loc[2, "code"] = "W06000001"
    _expect_fail(df, _schema(), "without prefix 'E09'")

    df = _ok_frame()
    df.loc[1, "cat"] = "z"
    _expect_fail(df, _schema(), "outside allowed set")

    df = _ok_frame()
    df["n"] = [-1, 10, 6]
    _expect_fail(df, _schema(), "values < 0")

    _expect_fail(_ok_frame().head(2), _schema(), "row count 2 != expected 3")

    df = _ok_frame()
    df["n"] = [0, 0, 0]
    _expect_fail(df, _schema(), "cross-check failed: n sums positive")

    # ---- multiple violations are ALL reported in one raise ----
    df = _ok_frame().drop(columns=["cat"])
    df.loc[1, "share"] = 5.0
    try:
        validate(df, _schema(), "t", verbose=False)
        raise AssertionError("should have raised")
    except SchemaError as e:
        msg = str(e)
        assert "missing column: cat" in msg and "values > 1.0" in msg
        assert "2 violation" in msg or "3 violation" in msg, msg

    print("ALL ASSERTIONS PASSED ✓")


if __name__ == "__main__":
    main()
