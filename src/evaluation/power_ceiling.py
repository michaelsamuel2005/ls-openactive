"""
Crossed-design power: variance, maximum attainable power, and the p × q surface.
Implements CA-01.A9. Basis: Westfall, Judd & Kenny (2014), attested row 1.

Notation:
    p = number of participants
    q = number of tasks (stimuli)
    A = participant-side variance component (participant × condition)
    B = stimulus-side variance component (stimulus × condition)
    C = participant × stimulus interaction + residual
    d = standardized effect size
"""

import math


def se_squared(p, q, A, B, C):
    """
    Variance of the estimated effect for a crossed design.

    SE² = A/p + B/q + C/(p*q)
    """
    return A / p + B / q + C / (p * q)


def se_squared_ceiling(q, B):
    """
    The variance floor as p → ∞ with q fixed.

    SE²_floor = B/q
    """
    return B / q


def se(p, q, A, B, C):
    """Standard error."""
    return math.sqrt(se_squared(p, q, A, B, C))


def ceiling_se(q, B):
    """Smallest achievable standard error for a fixed q."""
    return math.sqrt(se_squared_ceiling(q, B))


# Example
if __name__ == "__main__":
    A = 0.40
    B = 0.25
    C = 0.35

    p = 200
    q = 20

    print("SE² =", se_squared(p, q, A, B, C))
    print("SE  =", se(p, q, A, B, C))
    print("Variance floor =", se_squared_ceiling(q, B))
    print("SE floor =", ceiling_se(q, B))