import pathlib
import pytest

from eclx import get_ecl_deck


@pytest.fixture(
    params=[("t1a", "TUT1A"), ("t1e", "TUT1E"), ("t1an", "TUT1AN"), ("t1uu", "TUT1UU")]
)
def eclipse_runs(request):
    """Return paths to eclipse test runs"""
    here = pathlib.Path(__file__).parent
    folder, deckname = request.param
    deck = get_ecl_deck(here / "resources" / folder / deckname)
    return deck


@pytest.fixture(params=[("t1a", "TUT1A"), ("t1e", "TUT1E")])
def eclipse_runs_unified(request):
    """Return paths to eclipse test runs"""
    here = pathlib.Path(__file__).parent
    folder, deckname = request.param
    deck = get_ecl_deck(here / "resources" / folder / deckname)
    return deck


@pytest.fixture(params=[("t1an", "TUT1AN"), ("t1uu", "TUT1UU")])
def eclipse_runs_notunified(request):
    """Return paths to eclipse test runs"""
    here = pathlib.Path(__file__).parent
    folder, deckname = request.param
    deck = get_ecl_deck(here / "resources" / folder / deckname)
    return deck


@pytest.fixture()
def eclipse_props():
    """Return a link to the complex PROPS test"""
    here = pathlib.Path(__file__).parent
    return here / "resources" / "COMPLEX_PVT.inc"
