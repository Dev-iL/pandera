"""Regression guard for ``pandera[polars]`` in a pandas-free environment.

Run with plain ``python`` (no pytest) in an env where ``polars`` is installed
but ``numpy``/``pandas`` are NOT. Exits non-zero on any failure.

This guards against the regression in issue #2387 (re-regression of #2291):
building a schema with a builtin check raised ``KeyError`` because the polars
builtin-check functions were never registered when pandas was absent. A bare
``import pandera.polars`` smoke test does not catch this — the failure surfaces
only when a builtin check is constructed and a frame is validated.
"""

import sys


def main() -> int:
    # Guard: this check is meaningless if pandas/numpy are present (the bug is
    # masked because importing pandera registers check functions via the pandas
    # path). Fail loudly rather than passing a false negative.
    for masking_mod in ("numpy", "pandas"):
        try:
            __import__(masking_mod)
        except ImportError:
            continue
        print(
            f"ERROR: {masking_mod!r} is installed; this guard must run in a "
            "pandas-free environment to be meaningful.",
            file=sys.stderr,
        )
        return 1

    import polars as pl

    import pandera.errors as errors
    import pandera.polars as pa
    from pandera.polars import Column, DataFrameSchema

    # 1. Constructing builtin checks must register their functions (no KeyError).
    schema = DataFrameSchema(
        {
            "i": Column(pl.Int64, pa.Check.ge(0)),
            "s": Column(pl.Utf8, pa.Check.isin(["x", "y"])),
        }
    )

    # 2. Validating a conforming frame must pass end to end.
    schema.validate(pl.DataFrame({"i": [0, 1, 2], "s": ["x", "y", "x"]}))

    # 3. Validating a violating frame must raise SchemaErrors reporting the
    #    offending value -- not a swallowed ImportError/ModuleNotFoundError.
    try:
        schema.validate(
            pl.DataFrame({"i": [-1, 0, 1], "s": ["x", "y", "z"]}), lazy=True
        )
    except errors.SchemaErrors as err:
        failure_cases = str(err.failure_cases)
        assert "-1" in failure_cases, (
            "expected offending value -1 in failure cases, got: "
            f"{failure_cases}"
        )
    else:
        print(
            "ERROR: expected SchemaErrors for violating frame", file=sys.stderr
        )
        return 1

    print("SUCCESS: pandera[polars] builtin checks work without pandas/numpy")
    return 0


if __name__ == "__main__":
    sys.exit(main())
