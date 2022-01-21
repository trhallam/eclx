import pathlib
import pytest


@pytest.fixture(params=[("t1a", "TUT1A"), ("t1e", "TUT1E")])
def eclipse_runs(request):
    """Return paths to eclipse test runs"""
    here = pathlib.Path(__file__).parent
    folder, deckname = request.param
    return here / "resources" / folder / deckname


@pytest.fixture(params=[("t1a", "TUT1A"), ("t1e", "TUT1E")])
def eclipse_runs_unified(request):
    """Return paths to eclipse test runs"""
    here = pathlib.Path(__file__).parent
    folder, deckname = request.param
    return here / "resources" / folder / deckname
