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
#     display_name: Python (etlp)
#     language: python
#     name: etlp
# ---

# %% [markdown]
# # Import Keywords from text files
#
# `eclx` uses the [`lark`](https://github.com/lark-parser/lark) to implement a grammar parser for ECL keyword files. This is currently experimental and may change.
#
# Data is loaded a string tables and users must interpret the tables to a useable form, this includes the expansion of Eclipse x*y repeater values and -1 default values.

# %%
from eclx import EclAsciiParser

# create an instance of the parser
p = EclAsciiParser()
# parse the file you want to load
p.parse("../tests/resources/COMPLEX_PVT.inc")

# %% [markdown]
# Eclipse keywords can be printed

# %%
q = EclAsciiParser()
q.parse("../tests/resources/t1a/TUT1A.DATA")

# %%
print(p.get_keywords())

# %% [markdown]
# Indexing of Keyword is possible

# %%
p["DENSITY"]

# %% [markdown]
# Access all the data

# %%
p.data

# %% [markdown]
# ## Another Example

# %%
q = EclAsciiParser()
q.parse("../tests/resources/t1a/TUT1A.DATA")

# %%
