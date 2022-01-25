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

# %%
resources = pathlib.Path("../tests/resources")
deck = "t1an/TUT1AN"

# %%
rst = eclx.get_ecl_deck((resources/deck))["RST"]

# %%
eclx._ecl_file.load_ecl_property("../tests/resources/t1a/TUT1A.UNRST")

# %%
eclx.load_summary_df("../tests/resources/t1a/TUT1A.UNSMRY")

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

# %%
