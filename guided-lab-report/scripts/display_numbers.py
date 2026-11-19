"""Display helpers for calibrated results. Workbook calculations stay full precision."""


from decimal import Decimal, ROUND_HALF_UP, localcontext


DISPLAY_BOUND = "0.0001"


def fixed(value, *, signed=False):
    """Use at most four fractional digits and remove trailing zeros."""
    with localcontext() as context:
        context.rounding = ROUND_HALF_UP
        label = f"{Decimal(str(value)):.4f}".rstrip("0").rstrip(".")
    if label in ("-0", "0"):
        return "0"
    if signed and value > 0:
        label = "+" + label
    return label.replace("-", "−")


def tiny(value):
    return value != 0 and fixed(value) == "0"


def bounded(value):
    """Use an open interval when fixed-decimal display would erase the sign."""
    if tiny(value):
        return f"(0, {DISPLAY_BOUND})" if value > 0 else f"(−{DISPLAY_BOUND}, 0)"
    return fixed(value)


def tick(value):
    if not tiny(value):
        return fixed(value)
    # Keep distinct small axis ticks without adding fractional digits.
    decimal = Decimal(str(value))
    exponent = decimal.adjusted()
    mantissa = fixed(decimal.scaleb(-exponent))
    return f"{mantissa}e{exponent}".replace("-", "−")
