import pytest

from eclx._grid import (
    load_ecl_grid,
    load_ecl_grid_index,
    _corner_names,
    get_ecl_grid_dims,
    open_EclGrid,
)

from ecl.grid import EclGrid


def test_open_EclGrid_ok(eclipse_runs):
    filepath = eclipse_runs["GRID"][0]
    with open_EclGrid(filepath) as egrid:
        assert isinstance(egrid, EclGrid)


def test_open_EclGrid_missing_file(eclipse_runs):
    filepath = eclipse_runs["GRID"][0].with_suffix(".EGRIS")
    with pytest.raises(FileNotFoundError):
        with open_EclGrid(filepath) as egrid:
            pass


def test_open_EclGrid_bad_file(eclipse_runs):
    filepath = eclipse_runs["DATA"][0]
    with pytest.raises(ValueError):
        with open_EclGrid(filepath) as egrid:
            pass


def test_ecl_grid_dims(eclipse_runs):
    filepath = eclipse_runs["GRID"][0]
    assert get_ecl_grid_dims(filepath) == (5, 5, 3)


def test_corner_names():
    cn = _corner_names()
    assert cn[:3] == ["x0", "y0", "z0"]
    assert cn[-3:] == ["x7", "y7", "z7"]
    assert len(cn) == 8 * 3


def test_load_ecl_grid_index(eclipse_runs):
    result = load_ecl_grid_index(eclipse_runs["GRID"][0])
    assert result.shape == (75, 5)


def test_load_ecl_grid(eclipse_runs):
    result = load_ecl_grid(eclipse_runs["GRID"][0])
    assert result.shape == (75, 28)
