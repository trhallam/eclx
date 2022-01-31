# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.6
#   kernelspec:
#     display_name: Python [conda env:ecl_test38]
#     language: python
#     name: conda-env-ecl_test38-py
# ---

# %% [markdown]
# # Loading ecl results with `eclx`

# %%
# %load_ext autoreload
# %autoreload 2

import pathlib
import eclx
import pandas as pd
import numpy as np

# %%
resources = pathlib.Path("../tests/resources")
deck = "t1an/TUT1AN"

# %%
rst = eclx.get_ecl_deck((resources/deck))["RST"]

# %%
eclx._ecl_file.load_ecl_property("../tests/resources/t1a/TUT1A.UNRST")

# %%
with eclx.open_EclGrid("../tests/resources/t1ma_gc/TUT1MA_GC.EGRID") as f:
    mp = f.export_mapaxes()
    if mp:
        mp = mp.numpy_copy()
    c = f.export_coord().numpy_copy()
        
print(mp)
print(c)

# %%
with eclx.open_EclGrid("../tests/resources/t1a/TUT1A.EGRID") as f:
    mp = f.export_mapaxes()
    if mp:
        mp = mp.numpy_copy()
    c = f.export_coord().numpy_copy()
        
print(mp)
print(c)

# %%
with eclx.open_EclGrid("../tests/resources/t1ma_lc/TUT1MA_LC.EGRID") as f:
    mp = f.export_mapaxes()
    if mp:
        mp = mp.numpy_copy()
    c = f.export_coord().numpy_copy()
print(mp)
print(c)

# %%
with eclx.open_EclGrid("../tests/resources/t1ma_lcfh/TUT1MA_LCFH.EGRID") as f:
    mp = f.export_mapaxes()
    if mp:
        mp = mp.numpy_copy()
    c = f.export_coord().numpy_copy()   
print(mp)
print(c)

# %%
1000*np.sin(np.deg2rad(45))

# %%
mp

# %%
eclx.load_summary_df("../tests/resources/t1uu/TUT1UU.S0002")

# %%
eclx._rst.load_ecl_rst((resources/deck).with_suffix(".X0000"))

# %%
eclx._rst._get_restart_reports_unified("../tests/resources/t1a/TUT1A.UNRST")

# %%

from ecl.summary import EclSum

# %%
eclx.load_ecl_rst(rst[0], 0)

# %%
pathlib.di

# %%
ecl.ecl_util.EclUtil.get_file_type(str((resources/deck).with_suffix(".EGRID")))

# %%
dir(ecl.EclFileEnum)

# %%
dir(ecl)

# %% [markdown]
# ## Loading PROPS Keywords and Tables

# %%
from eclx.props import get_type, scan_eclipsekw, read_eclipsekw_3dtable, _read_eclipsekw_section

_read_eclipsekw_section("../tests/resources/COMPLEX_PVT.inc", "PVTO")

# %%
dir(eclx)

# %%
