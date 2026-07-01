"""
test_incremental_validity.py — verify the incremental-validity statistics against
INDEPENDENT computations and known-answer constructions, so we trust the numbers
before they touch the real data.

  - ols() vs scikit-learn (coefficients, R²) and a hand-computed standard error;
  - partial_spearman() vs its rank-residual definition;
  - nested F-test + partial correlation on an orthogonal construction where provision
    provably DOES / DOES NOT add signal;
  - the end-to-end verdict on both scenarios;
  - Moran's I direction on a path graph (clustered vs alternating fields).

Run:  python -m tests.test_incremental_validity
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from src.incremental_validity import (
    morans_i,
    nested_f,
    ols,
    partial_spearman,
    run,
)


def _orthogonal_design(n: int = 48):
    """Deterministic need, provision (⊥ need) and a third component (⊥ both). No RNG."""
    need = np.linspace(-2.0, 2.0, n)
    nc = need - need.mean()
    prov = np.cos(np.arange(n))
    prov = prov - (prov @ nc) / (nc @ nc) * nc          # remove the need component
    prov = prov - prov.mean()
    third = np.sin(np.arange(n) * 0.7)
    third = third - (third @ nc) / (nc @ nc) * nc
    third = third - (third @ prov) / (prov @ prov) * prov
    third = third - third.mean()
    return need, prov, third


def test_ols_matches_sklearn_and_hand_se():
    need, prov, third = _orthogonal_design()
    y = 1.0 * need - 1.5 * prov + 0.3 * third
    X = np.column_stack([need, prov])
    res = ols(X, y, ["need", "prov"])

    lr = LinearRegression().fit(X, y)
    assert np.allclose(res["beta"][1:], lr.coef_, atol=1e-9), (res["beta"], lr.coef_)
    assert abs(res["beta"][0] - lr.intercept_) < 1e-9
    assert abs(res["r2"] - lr.score(X, y)) < 1e-9

    # hand-computed SE of the slope in a SIMPLE regression y ~ need
    s = ols(need, y, ["need"])
    xbar = need.mean()
    Sxx = float(((need - xbar) ** 2).sum())
    b1 = float(((need - xbar) * (y - y.mean())).sum() / Sxx)
    b0 = float(y.mean() - b1 * xbar)
    resid = y - (b0 + b1 * need)
    sigma2 = float((resid ** 2).sum() / (len(y) - 2))
    se_hand = np.sqrt(sigma2 / Sxx)
    assert abs(s["se"][1] - se_hand) < 1e-9, (s["se"][1], se_hand)
    assert abs(s["beta"][1] - b1) < 1e-9


def test_partial_spearman_matches_residual_definition():
    need, prov, third = _orthogonal_design()
    y = 1.0 * need - 1.5 * prov + 0.3 * third

    def indep_partial(x, yy, z):
        from scipy.stats import rankdata
        rx, ry, rz = rankdata(x), rankdata(yy), rankdata(z)

        def resid(a, b):
            A = np.column_stack([np.ones(len(b)), b])
            coef, *_ = np.linalg.lstsq(A, a, rcond=None)
            return a - A @ coef
        return float(np.corrcoef(resid(rx, rz), resid(ry, rz))[0, 1])

    got = partial_spearman(prov, y, need)["r"]
    exp = indep_partial(prov, y, need)
    assert abs(got - exp) < 1e-9, (got, exp)


def test_provision_adds_signal_when_it_should():
    need, prov, third = _orthogonal_design()
    y = 1.0 * need - 1.5 * prov + 0.05 * third          # provision matters a lot

    pc = partial_spearman(prov, y, need)
    assert pc["r"] < -0.9 and pc["p"] < 0.01, pc        # strong, significant, correct sign

    m1 = ols(need, y, ["need"])
    m2 = ols(np.column_stack([need, prov]), y, ["need", "prov"])
    f = nested_f(m1["rss"], m2["rss"], m1["k"], m2["k"], len(y))
    assert f["p"] < 0.01, f                              # provision improves the model
    assert m2["r2"] - m1["r2"] > 0.3                     # material incremental R²


def test_provision_adds_nothing_when_it_should_not():
    need, prov, third = _orthogonal_design()
    y = 1.0 * need + 0.5 * third                         # provision plays NO role

    pc = partial_spearman(prov, y, need)
    assert abs(pc["r"]) < 0.25 and pc["p"] > 0.1, pc     # ~0, not significant

    m1 = ols(need, y, ["need"])
    m2 = ols(np.column_stack([need, prov]), y, ["need", "prov"])
    f = nested_f(m1["rss"], m2["rss"], m1["k"], m2["k"], len(y))
    assert f["p"] > 0.2, f                               # provision does not improve the model


def _frame(y, need, prov):
    """Build borough_features/borough_gap_index look-alikes for run()."""
    n = len(y)
    codes = [f"E090{i:05d}" for i in range(n)]
    gap = pd.DataFrame({
        "lad_code": codes, "need_score_z": need, "provision_score_z": prov,
        "gap_index_z": need - prov, "is_city_of_london": False,
    })
    feats = pd.DataFrame({"lad_code": codes, "pct_inactive_adults": 0.20 + 0.02 * y})
    return feats, gap


def test_end_to_end_verdict():
    need, prov, third = _orthogonal_design()
    feats_a, gap_a = _frame(1.0 * need - 1.5 * prov + 0.05 * third, need, prov)
    res_a = run(feats_a, gap_a, boundaries=None)
    assert res_a["verdict"]["provision_adds_signal_rankbased"] is True, res_a["verdict"]

    feats_n, gap_n = _frame(1.0 * need + 0.5 * third, need, prov)
    res_n = run(feats_n, gap_n, boundaries=None)
    assert res_n["verdict"]["provision_adds_signal_rankbased"] is False, res_n["verdict"]


def test_morans_i_direction():
    n = 12
    W = np.zeros((n, n))
    for i in range(n - 1):                               # 1-D path graph
        W[i, i + 1] = W[i + 1, i] = 1.0
    W = W / W.sum(axis=1, keepdims=True)

    clustered = morans_i(np.arange(n, dtype=float), W)   # smooth gradient → positive autocorr
    assert clustered["I"] > clustered["EI"] and clustered["z"] > 1.0, clustered

    alternating = morans_i(np.array([0.0, 1.0] * (n // 2)), W)  # checkerboard → negative
    assert alternating["I"] < alternating["EI"] and alternating["z"] < 0, alternating


def main():
    test_ols_matches_sklearn_and_hand_se()
    test_partial_spearman_matches_residual_definition()
    test_provision_adds_signal_when_it_should()
    test_provision_adds_nothing_when_it_should_not()
    test_end_to_end_verdict()
    test_morans_i_direction()
    print("ALL ASSERTIONS PASSED ✓")


if __name__ == "__main__":
    main()
