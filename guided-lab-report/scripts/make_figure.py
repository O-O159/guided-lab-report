"""Draw a synthetic calibration figure from a verified workbook JSON export.

Usage: python scripts/make_figure.py readings.json figure.png
Requires Python 3.10+ and Pillow 10.1+. This script checks the data/fit alignment
and draws the exported fitted values. It also checks the workbook's range flag,
measurement concentration and dilution correction. It never estimates a new fit.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from io import BytesIO
import json
import math
from pathlib import Path
from statistics import fmean

from PIL import Image, ImageDraw, ImageFont

from display_numbers import tick


@dataclass(frozen=True)
class FitCriteria:
    minimum_r_squared: float
    maximum_absolute_residual: float


@dataclass(frozen=True)
class Calibration:
    slope: float
    intercept: float
    r_squared: float | None
    unknown_absorbance: float
    measurement_concentration: float
    dilution_factor: float
    in_calibration_range: bool
    unknown_concentration: float | None
    standards: tuple[tuple[float, float], ...]
    fitted: tuple[float, ...]
    sample_sd: tuple[float | None, ...]
    reference_concentration: float | None
    fit_criteria: FitCriteria | None
    fit_status: str
    maximum_absolute_residual: float


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    return float(value)


def close(actual, expected):
    return math.isclose(actual, expected, rel_tol=1e-8, abs_tol=1e-12)


def validate_ols(points, slope, intercept):
    """Check the exported OLS coefficients without changing the plotted line."""
    x_mean = fmean(x for x, _ in points)
    y_mean = fmean(y for _, y in points)
    dx = [x - x_mean for x, _ in points]
    dy = [y - y_mean for _, y in points]
    expected_slope = math.fsum(x * y for x, y in zip(dx, dy)) / math.fsum(x * x for x in dx)
    expected_intercept = y_mean - expected_slope * x_mean
    offset_scale = max(abs(y_mean), abs(expected_slope * x_mean))
    if not math.isclose(slope, expected_slope, rel_tol=1e-8) or not math.isclose(
        intercept, expected_intercept, rel_tol=1e-8, abs_tol=32 * math.ulp(offset_scale)
    ):
        raise ValueError("exported coefficients do not match the ordinary least-squares fit of the standards")


def residual_r_squared(points, fitted):
    """Evaluate the imported line against the observations, without refitting."""
    observed = [y for _, y in points]
    if min(observed) == max(observed):
        return None
    center = fmean(observed)
    spread = math.hypot(*(y - center for y in observed))
    if spread == 0:
        return None
    error = math.hypot(*(y - predicted for y, predicted in zip(observed, fitted)))
    return 1 - (error / spread) ** 2


def read_criteria(raw):
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ValueError("fit_criteria must be an object or null")
    minimum_r_squared = number(raw["minimum_r_squared"], "minimum_r_squared")
    maximum_absolute_residual = number(raw["maximum_absolute_residual"], "maximum_absolute_residual")
    if not 0 <= minimum_r_squared <= 1 or maximum_absolute_residual < 0:
        raise ValueError("fit criteria require 0 <= minimum_r_squared <= 1 and a nonnegative residual limit")
    return FitCriteria(minimum_r_squared, maximum_absolute_residual)


def fit_outcome(criteria, r_squared, maximum_residual):
    if criteria is None:
        return "unverified"
    r_squared_margin = 1e-12 * max(1, abs(criteria.minimum_r_squared))
    residual_margin = 1e-12 * max(1, abs(criteria.maximum_absolute_residual))
    if (
        r_squared is not None
        and r_squared >= criteria.minimum_r_squared - r_squared_margin
        and maximum_residual <= criteria.maximum_absolute_residual + residual_margin
    ):
        return "accepted"
    return "rejected"


def load_calibration(path):
    """Validate the workbook export without changing its points or model."""
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("readings.json must contain a JSON object")
    raw_points = data["standards"]
    if not isinstance(raw_points, list) or len(raw_points) < 2:
        raise ValueError("standards must contain at least two concentration/response pairs")
    points = []
    for index, pair in enumerate(raw_points):
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError(f"standards[{index}] must be [concentration, mean_absorbance]")
        points.append(tuple(number(value, f"standards[{index}]") for value in pair))
    if len({x for x, _ in points}) < 2:
        raise ValueError("standards must cover at least two distinct concentrations")

    raw_fit = data["fitted"]
    raw_sd = data.get("sample_sd")
    if raw_sd is None:
        raw_sd = [None] * len(points)
    if any(not isinstance(values, list) or len(values) != len(points) for values in (raw_fit, raw_sd)):
        raise ValueError("fitted and supplied sample_sd must align with standards")
    fitted = tuple(number(value, "fitted") for value in raw_fit)
    sample_sd = tuple(None if value is None else number(value, "sample_sd") for value in raw_sd)
    if any(value is not None and value < 0 for value in sample_sd):
        raise ValueError("sample_sd cannot be negative")

    slope = number(data["slope"], "slope")
    intercept = number(data["intercept"], "intercept")
    if slope == 0:
        raise ValueError("slope must be nonzero for inverse calibration")
    validate_ols(points, slope, intercept)
    if any(not close(y_fit, slope * x + intercept) for (x, _), y_fit in zip(points, fitted)):
        raise ValueError("exported fitted points disagree with slope and intercept")
    r_squared = residual_r_squared(points, fitted)
    supplied_r_squared = data.get("r_squared")
    if supplied_r_squared is not None:
        supplied_r_squared = number(supplied_r_squared, "r_squared")
        if r_squared is None or not close(supplied_r_squared, r_squared):
            raise ValueError("exported r_squared disagrees with the plotted observations and fit")
    if r_squared is not None and not -1e-12 <= r_squared <= 1:
        raise ValueError("residual-based r_squared is outside [0, 1] for this linear model")
    fit_criteria = read_criteria(data.get("fit_criteria"))
    maximum_residual = max(abs(y - prediction) for (_, y), prediction in zip(points, fitted))
    fit_status = data["fit_status"]
    if fit_status != fit_outcome(fit_criteria, r_squared, maximum_residual):
        raise ValueError("fit_status disagrees with the supplied criteria and measured fit diagnostics")

    absorbance = number(data["unknown_absorbance"], "unknown_absorbance")
    measurement = number(data["measurement_concentration"], "measurement_concentration")
    if not close(measurement, (absorbance - intercept) / slope):
        raise ValueError("measurement_concentration disagrees with the exported linear model")
    dilution = number(data["dilution_factor"], "dilution_factor")
    if dilution <= 0:
        raise ValueError("dilution_factor must be greater than zero")
    in_range = data["in_calibration_range"]
    if not isinstance(in_range, bool):
        raise ValueError("in_calibration_range must be true or false")
    low, high = min(x for x, _ in points), max(x for x, _ in points)
    margin = 1e-12 * max(1, abs(low), abs(high))
    if in_range != (low - margin <= measurement <= high + margin):
        raise ValueError("in_calibration_range disagrees with the measured solution and standards")
    concentration = data["unknown_concentration"]
    if in_range and fit_status == "accepted":
        concentration = number(concentration, "unknown_concentration")
        if not close(concentration, measurement * dilution):
            raise ValueError("unknown_concentration disagrees with measurement_concentration × dilution_factor")
    elif concentration is not None:
        raise ValueError("unknown_concentration must be null if the fit is unaccepted or the sample is out of range")

    reference = data.get("reference_concentration")
    reference = None if reference is None else number(reference, "reference_concentration")
    if reference is not None and reference < 0:
        raise ValueError("reference_concentration must be nonnegative")
    return Calibration(
        slope=slope, intercept=intercept, r_squared=r_squared, unknown_absorbance=absorbance,
        measurement_concentration=measurement, dilution_factor=dilution, in_calibration_range=in_range,
        unknown_concentration=concentration, standards=tuple(points), fitted=fitted,
        sample_sd=sample_sd, reference_concentration=reference, fit_criteria=fit_criteria,
        fit_status=fit_status, maximum_absolute_residual=maximum_residual,
    )


def axis_ticks(values):
    low, high = min(values), max(values)
    span = high - low
    if span <= 0 or not math.isfinite(span):
        raise ValueError("axis data must have a finite, nonzero range")
    target = span / 5
    base = 10 ** math.floor(math.log10(target))
    step = next((base * k for k in (1, 2, 2.5, 5, 10) if base * k >= target), 10 * base)
    start, end = math.floor(low / step), math.ceil(high / step)
    return [i * step for i in range(start, end + 1)]


def font(size):
    for family in ("DejaVuSans.ttf", "LiberationSans-Regular.ttf", "Arial.ttf"):
        try:
            return ImageFont.truetype(family, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def render_figure(calibration):
    """Return a 300 dpi PNG in memory for reuse by the Word demo."""
    points = sorted((x, observed, expected) for (x, observed), expected in
                    zip(calibration.standards, calibration.fitted))
    x_ticks = axis_ticks([x for x, _, _ in points])
    y_ticks = axis_ticks([y for _, observed, expected in points for y in (observed, expected)])
    image = Image.new("RGB", (1500, 790), "white")
    draw = ImageDraw.Draw(image)
    body, axis_font = font(34), font(39)
    ink, teal, grid = "#17272C", "#155D65", "#D8E2E3"
    left, right, top, bottom = 211, 1418, 108, 629

    def scale(value, ticks, start, end):
        # Small padding keeps a marker centered on an end tick fully visible.
        fraction = (value - ticks[0]) / (ticks[-1] - ticks[0])
        return start + (end - start) * (0.033 + fraction * 0.934)

    def position(x, y):
        return scale(x, x_ticks, left, right), scale(y, y_ticks, bottom, top)

    for y in y_ticks:
        _, py = position(x_ticks[0], y)
        draw.line([(left, py), (right, py)], fill=grid, width=2)
        draw.text((left - 19, py), tick(y), font=body, fill=ink, anchor="rm")
    for x in x_ticks:
        px, _ = position(x, y_ticks[0])
        draw.line([(px, bottom), (px, bottom + 11)], fill=ink, width=2)
        draw.text((px, bottom + 25), tick(x), font=body, fill=ink, anchor="mt")
    draw.line([(left, top), (left, bottom), (right, bottom)], fill=ink, width=3)
    draw.line([position(x, fit) for x, _, fit in points], fill=teal, width=6)
    for x, observed, _ in points:
        px, py = position(x, observed)
        draw.ellipse((px - 11, py - 11, px + 11, py + 11), fill="white", outline=ink, width=4)

    draw.text((left, 55), "Mean absorbance", font=axis_font, fill=ink, anchor="lm")
    draw.text(((left + right) // 2, 758), "Standard concentration (mg/L)",
              font=axis_font, fill=ink, anchor="ms")
    draw.ellipse((861, 46, 882, 67), fill="white", outline=ink, width=4)
    draw.text((898, 56), "Standards", font=body, fill=ink, anchor="lm")
    draw.line([(1123, 56), (1187, 56)], fill=teal, width=6)
    draw.text((1205, 56), "Workbook fit", font=body, fill=ink, anchor="lm")

    result = BytesIO()
    image.save(result, format="PNG", dpi=(300, 300))
    result.seek(0)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readings", type=Path)
    parser.add_argument("figure", type=Path)
    args = parser.parse_args()
    try:
        if args.figure.suffix.lower() != ".png":
            raise ValueError("figure output must have a .png extension")
        args.figure.write_bytes(render_figure(load_calibration(args.readings)).getvalue())
    except (OSError, KeyError, ValueError, OverflowError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
