import pytest

from eclx._utils import test_open_eclfile as t_open_eclfile

from ecl.summary import EclSum
from ecl.eclfile import EclFile
from ecl.grid import EclGrid

# def test_scan_ecl_kw(eclipse_props):
#     scan_ecl_kw(eclipse_props)
#     assert False


@pytest.mark.parametrize(
    "fext,hand",
    [("SUM", EclSum), ("RST", EclFile), ("INIT", EclFile), ("GRID", EclGrid)],
)
def test_test_open_eclfile(eclipse_runs, fext, hand):
    filepath = eclipse_runs[fext][0]
    proc = t_open_eclfile(hand, filepath)
    assert proc.exitcode == 0
