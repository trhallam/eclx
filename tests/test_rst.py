import pytest

import pandas as pd

from eclx._rst import (
    is_restart_file,
    get_deck_restart_files,
    is_restart_unified,
    _get_restart_reports_unified,
    get_restart_reports,
    load_ecl_rst,
)


def test_is_restart_file(eclipse_runs):
    filepath = eclipse_runs.with_suffix(".UNRST")
    assert is_restart_file(filepath)
    with pytest.raises(AssertionError):
        filepath = eclipse_runs.with_suffix(".UNSMRY")
        assert is_restart_file(filepath)


def test_is_restart_unified(eclipse_runs_unified):
    filepath = eclipse_runs_unified.with_suffix(".UNRST")
    assert is_restart_unified(filepath)


def test_get_restart_reports_unified(eclipse_runs_unified):
    filepath = eclipse_runs_unified.with_suffix(".UNRST")
    reports = _get_restart_reports_unified(filepath)
    assert isinstance(reports, pd.DataFrame)
    assert reports.shape == (11, 7)


def test_get_restart_reports(eclipse_runs):
    filepath = eclipse_runs.with_suffix(".UNRST")
    reports = get_restart_reports(filepath)
    assert isinstance(reports, pd.DataFrame)
    assert reports.shape == (11, 7)


def test_load_ecl_rst(eclipse_runs):
    filepath = eclipse_runs.with_suffix(".UNRST")
    rst_df = load_ecl_rst(filepath)
    assert isinstance(rst_df, pd.DataFrame)
