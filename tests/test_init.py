import pytest

import pandas as pd

from eclx._init import (
    load_init_intehead,
)


def test_load_init_intehead(eclipse_runs):
    filepath = eclipse_runs.with_suffix(".INIT")

    intehead = load_init_intehead(filepath)
    assert isinstance(intehead, dict)
    for var in ("NI", "NJ", "NK"):
        assert var in intehead
