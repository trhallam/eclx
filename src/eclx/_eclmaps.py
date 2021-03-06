"""Mappings for key ecl properties.
"""
from enum import Enum, unique

# pylint: disable=missing-docstring


class InitIntheadMap(Enum):
    UNITS = 2
    PVTM = 3
    NI = 8
    NJ = 9
    NK = 10
    NACTIV = 11
    GRID_TYPE = 13
    PHASE = 14
    IPROG = 94


@unique
class EclUnitMap(Enum):
    METRIC = 1
    FIELD = 2
    LAB = 3
    PVTM = 4


class EclUnitScaler(Enum):
    METRIC = dict(
        length=1,
        time=1,
        area=1,
        density=1e-3,
        density_kg=1.0,
        pressure=1e-1,
        ipressure=1 / 1e-1,
        temp_abs=1,
        temp_rel=lambda x: x,
        compress=1e2,
        viscosity=1,
        perm=1,
        volume=1,
        unitless=1,
    )
    FIELD = dict(
        length=0.3048,
        time=1,
        area=10.7639,
        density=0.0160184634,
        density_kg=16.0185,
        pressure=0.00689476,
        ipressure=1 / 0.00689476,
        temp_abs=5 / 9,
        temp_rel=lambda x: x - 32 * 5 / 9,
        compress=1 / 0.00689476,
        viscosity=1,
        perm=1,
        volume=0.158987,
        unitless=1,
    )
    LAB = dict(
        length=1e-2,
        time=1 / 24,
        area=1e-4,
        density=1,
        density_kg=1000.0,
        pressure=0.101325,
        ipressure=1 / 0.101325,
        temp_abs=1,
        temp_rel=lambda x: x,
        compress=1 / 0.101325,
        viscosity=1,
        perm=1,
        volume=1e-6,
        unitless=1,
    )
    PVTM = dict(
        length=1,
        time=1,
        area=1,
        density=1e-3,
        density_kg=1.0,
        pressure=0.101325,
        ipressure=1 / 0.101325,
        temp_abs=1,
        temp_rel=lambda x: x,
        compress=1 / 0.101325,
        viscosity=1,
        perm=1,
        volume=1,
        unitless=1,
    )


class EclipseAsciiTypeMap(Enum):
    INTE = int
    REAL = float
    CHAR = str
    LOGI = bool
    DOUB = float
