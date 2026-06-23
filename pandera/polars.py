"""A flexible and expressive polars validation library for Python."""

# Eagerly register the polars builtin-check *functions* (name -> dispatcher) in
# the shared CHECK_FUNCTION_REGISTRY so ``pa.Check.ge(0)`` and friends resolve at
# construction time, even in a polars-only env where pandas/numpy are absent and
# ``import pandera`` therefore never populated the registry via the pandas path.
# This imports check functions only; validation *backends* stay lazily registered
# (toggleable via set_config) per the registration design.
import pandera.backends.polars.builtin_checks  # noqa: F401
from pandera import config, errors
from pandera.api.checks import Check
from pandera.api.dataframe.model_components import (
    Field,
    check,
    dataframe_check,
)
from pandera.api.polars.components import Column
from pandera.api.polars.container import DataFrameSchema
from pandera.api.polars.model import DataFrameModel
from pandera.api.polars.types import PolarsData
from pandera.decorators import check_input, check_io, check_output, check_types
from pandera.schema_inference.polars import (
    infer_dataframe_schema,
    infer_schema,
)
from pandera.typing import polars as typing

__all__ = [
    "check_input",
    "check_io",
    "check_output",
    "check_types",
    "check",
    "Check",
    "Column",
    "dataframe_check",
    "DataFrameModel",
    "DataFrameSchema",
    "errors",
    "Field",
    "infer_dataframe_schema",
    "infer_schema",
    "PolarsData",
    "set_config",
]
