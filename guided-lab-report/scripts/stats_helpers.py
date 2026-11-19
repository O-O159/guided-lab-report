"""Small numerical checks for an agreed lab analysis. Requires NumPy.

Import summary, linear_regression, or propagate_uncertainty from this module.
CLI: python stats_helpers.py request.json (or - to read JSON from stdin).
Requests:
  {"operation":"summary", "values":[1,2,3]}
  {"operation":"regression", "x":[1,2,3], "y":[2,4,6]}
  {"operation":"uncertainty", "gradient":[3,2],
   "standard_uncertainties":[0.1,0.2]}
For correlated inputs, replace standard_uncertainties with a covariance matrix.

No missing-value removal, exclusion, model selection, weighting, or unit
conversion is performed. Regression is ordinary least squares WITH an intercept.
Inputs must be real numbers. Parse and verify any text values before passing them in.
Propagation is first-order local propagation using user-supplied derivatives
and STANDARD uncertainties, not confidence intervals or expanded uncertainties.
These results check, rather than replace, the formula-driven workbook.
"""

import argparse
import json
import math
import sys
from numbers import Real
from pathlib import Path

import numpy as np


def _numeric_array(values, name, dimensions):
    # Object dtype keeps booleans and strings visible before float conversion.
    raw = np.asarray(values, dtype=object)
    if raw.ndim != dimensions or raw.size == 0:
        raise ValueError(f"{name} must be a nonempty {dimensions}-dimensional array")
    if any(isinstance(value, (bool, np.bool_)) or not isinstance(value, Real)
           for value in raw.flat):
        raise ValueError(f"{name} must contain only real numbers")
    result = raw.astype(float)
    if not np.isfinite(result).all():
        raise ValueError(f"{name} must contain only finite numbers")
    return result


def _vector(values, name):
    return _numeric_array(values, name, 1)


def summary(values):
    """Mean, sample SD (ddof=1), and SEM for independent replicates.

    Grouping/independence must be established by the caller. A singleton has
    an observed mean but no estimated sample SD/SEM (returned as None).
    """
    data = _vector(values, "values")
    n = int(data.size)
    mean = float(np.mean(data))
    sd = float(np.std(data, ddof=1)) if n > 1 else None
    return {"n": n, "mean": mean, "sample_sd": sd,
            "sem": sd / math.sqrt(n) if sd is not None else None}


def linear_regression(x, y):
    """OLS y=slope*x+intercept, paired inputs, no automatic exclusions.

    SEs/covariance are residual-based homoscedastic OLS estimates. They do not
    include input measurement uncertainty. Two points provide no residual df.
    R² is undefined for a constant response and is returned as None.
    Parameter covariance order is [slope, intercept].
    """
    x = _vector(x, "x")
    y = _vector(y, "y")
    if x.size != y.size or x.size < 2:
        raise ValueError("x and y require equal lengths and at least two pairs")
    n = int(x.size)
    xm, ym = float(np.mean(x)), float(np.mean(y))
    xc, yc = x - xm, y - ym
    sxx = float(xc @ xc)
    if not math.isfinite(sxx) or sxx <= 0:
        raise ValueError("x must have finite nonzero variation")
    slope = float((xc @ yc) / sxx)
    intercept = ym - slope * xm
    fitted = slope * xc + ym
    residuals = y - fitted
    sse, sst = float(residuals @ residuals), float(yc @ yc)
    if not all(map(math.isfinite, (slope, intercept, sse, sst))):
        raise ValueError("regression overflowed; check units and numeric scale")
    residual_variance = sse / (n - 2) if n > 2 else None
    cov = None
    if residual_variance is not None:
        cov = residual_variance * np.array([
            [1 / sxx, -xm / sxx],
            [-xm / sxx, 1 / n + xm * xm / sxx],
        ])
    return {
        "n": n, "slope": slope, "intercept": intercept,
        "r_squared": 1 - sse / sst if sst > 0 else None,
        "residual_df": n - 2, "sse": sse,
        "residual_sd": math.sqrt(residual_variance)
        if residual_variance is not None else None,
        "slope_se": math.sqrt(float(cov[0, 0])) if cov is not None else None,
        "intercept_se": math.sqrt(float(cov[1, 1])) if cov is not None else None,
        "parameter_order": ["slope", "intercept"],
        "parameter_covariance": cov.tolist() if cov is not None else None,
        "fitted": fitted.tolist(), "residuals": residuals.tolist(),
    }


def propagate_uncertainty(gradient, standard_uncertainties=None, covariance=None):
    """Return sqrt(g.T @ covariance @ g) using a supplied local gradient.

    Supply exactly one of standard_uncertainties (independent inputs) or a
    symmetric positive-semidefinite covariance matrix (correlated inputs).
    Gradient/covariance variable order and compatible units are caller inputs.
    """
    g = _vector(gradient, "gradient")
    if (standard_uncertainties is None) == (covariance is None):
        raise ValueError("supply exactly one uncertainty representation")
    if standard_uncertainties is not None:
        u = _vector(standard_uncertainties, "standard_uncertainties")
        if u.size != g.size or (u < 0).any():
            raise ValueError("standard uncertainties must match gradient and be nonnegative")
        c = np.diag(u * u)
    else:
        c = _numeric_array(covariance, "covariance", 2)
        if c.shape != (g.size, g.size):
            raise ValueError("covariance must match gradient size")
    scale = float(np.max(np.abs(c)))
    tol = np.finfo(float).eps * scale * max(10, g.size * 10)
    if not np.allclose(c, c.T, rtol=1e-12, atol=tol):
        raise ValueError("covariance must be symmetric")
    if (np.diag(c) < 0).any():
        raise ValueError("covariance diagonal must be nonnegative")
    c = (c + c.T) / 2
    if float(np.min(np.linalg.eigvalsh(c))) < -tol:
        raise ValueError("covariance must be positive semidefinite")
    variance = float(g @ c @ g)
    if not math.isfinite(variance):
        raise ValueError("propagation overflowed; check units and numeric scale")
    if variance < 0:
        roundoff = np.finfo(float).eps * float(np.abs(g) @ np.abs(c) @ np.abs(g)) * 20
        if variance < -roundoff:
            raise ValueError("propagated variance is negative")
    return math.sqrt(max(0.0, variance))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", help="JSON file path, or - for stdin")
    args = parser.parse_args()
    try:
        request = json.loads(sys.stdin.read() if args.request == "-"
                             else Path(args.request).read_text(encoding="utf-8-sig"))
        operation = request["operation"]
        if operation == "summary":
            result = summary(request["values"])
        elif operation == "regression":
            result = linear_regression(request["x"], request["y"])
        elif operation == "uncertainty":
            result = {"standard_uncertainty": propagate_uncertainty(
                request["gradient"], request.get("standard_uncertainties"),
                request.get("covariance"))}
        else:
            raise ValueError(f"unsupported operation: {operation}")
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f"Invalid request: {exc}\n")


if __name__ == "__main__":
    main()
