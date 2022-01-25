import pytest

import pandas as pd

from eclx._ecl_file import open_EclFile, get_ecl_property_keys, load_ecl_property, get_ecl_deck

from ecl.eclfile import EclFile


def test_open_EclFile_ok(eclipse_runs):
    filepath = eclipse_runs["INIT"][0]
    with open_EclFile(filepath) as efile:
        assert isinstance(efile, EclFile)


def test_open_EclFile_missing_file(eclipse_runs):
    filepath = eclipse_runs["INIT"][0]
    filepath = filepath.with_suffix(".INIS")
    with pytest.raises(FileNotFoundError):
        with open_EclFile(filepath) as efile:
            pass


def test_get_ecl_property_keys(eclipse_runs):
    filepath = eclipse_runs["INIT"][0]
    keys = get_ecl_property_keys(filepath)
    assert isinstance(keys, list)
    assert "PORO" in keys


def test_load_ecl_proprty_init_all(eclipse_runs):
    filepath = eclipse_runs["INIT"][0]
    init = load_ecl_property(filepath)
    assert isinstance(init, pd.DataFrame)
    # PORV missing from TUT1AN test ?
    assert init.shape == (75, 28) or init.shape == (75, 27)
    assert "PORO" in init.columns


def test_load_ecl_proprty_init_list(eclipse_runs):
    filepath = eclipse_runs["INIT"][0]
    init = load_ecl_property(filepath, keys=["PORO", "SATNUM"])
    assert isinstance(init, pd.DataFrame)
    assert init.shape == (75, 7)
    assert "PORO" in init.columns
    assert "SATNUM" in init.columns


def test_load_ecl_proprty_init_str(eclipse_runs):
    filepath = eclipse_runs["INIT"][0]
    init = load_ecl_property(filepath, keys="PORO")
    assert isinstance(init, pd.DataFrame)
    assert init.shape == (75, 6)
    assert "PORO" in init.columns


def test_load_ecl_proprty_init_specify_grid(eclipse_runs):
    filepath = eclipse_runs["INIT"][0]
    grid_filepath = eclipse_runs["GRID"][0]
    init = load_ecl_property(
        filepath, keys=["PORO", "SATNUM"], grid_filepath=grid_filepath
    )
    assert isinstance(init, pd.DataFrame)
    assert init.shape == (75, 7)
    assert "PORO" in init.columns
    assert "SATNUM" in init.columns


def test_load_ecl_proprty_rst_all(eclipse_runs):
    rst = load_ecl_property(eclipse_runs["RST"][0])
    assert isinstance(rst, pd.DataFrame)
    assert rst.shape == (75, 7)
    assert "SWAT_0" in rst.columns


def test_load_ecl_proprty_rst_list(eclipse_runs):
    rst = load_ecl_property(eclipse_runs["RST"][0], keys=["PRESSURE", "SWAT"])
    assert isinstance(rst, pd.DataFrame)
    assert rst.shape == (75, 7)
    assert "PRESSURE_0" in rst.columns
    assert "SWAT_0" in rst.columns


def test_load_ecl_proprty_rst_str(eclipse_runs):
    rst = load_ecl_property(eclipse_runs["RST"][0], keys="SWAT")
    assert isinstance(rst, pd.DataFrame)
    assert rst.shape == (75, 6)
    assert "SWAT_0" in rst.columns


def test_load_ecl_proprty_rst_specify_grid(eclipse_runs):
    grid_filepath = eclipse_runs["GRID"][0]
    rst = load_ecl_property(
        eclipse_runs["RST"][0], keys=["SWAT", "PRESSURE"], grid_filepath=grid_filepath
    )
    assert isinstance(rst, pd.DataFrame)
    assert rst.shape == (75, 7)
    assert "PRESSURE_0" in rst.columns
    assert "SWAT_0" in rst.columns


@pytest.mark.parametrize("rep", [0, 6, 10])
def test_load_ecl_proprty_rst_reportn(eclipse_runs_unified, rep):
    grid_filepath = eclipse_runs_unified["GRID"][0]
    rst = load_ecl_property(
        eclipse_runs_unified["RST"][0],
        keys=["SWAT", "PRESSURE"],
        grid_filepath=grid_filepath,
        report_index=rep,
    )
    assert isinstance(rst, pd.DataFrame)
    assert rst.shape == (75, 7)
    assert f"PRESSURE_{rep}" in rst.columns
    assert f"SWAT_{rep}" in rst.columns
