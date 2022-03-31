# eclx - [![latest-version](https://img.shields.io/pypi/v/eclx?color=006dad&label=pypi_version&logo=Python&logoColor=white)](https://pypi.org/project/eclx)

<p align="left">
    <a href="https://github.com/trhallam/eclx/actions" 
       alt="Python Tests">
        <img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/trhallam/0da415ee1bf30b0fc37a2fc4ddafbdee/raw/eclx_test.json" />
    </a>
    <a href="https://github.com/psf/black" 
       alt="black">
        <img src="https://img.shields.io/badge/code_style-black-000000.svg" />
    </a>
    </a>
        <a href="https://github.com/trhallam/digirock/blob/main/LICENSE" 
       alt="License">
        <img src="https://img.shields.io/badge/license-MIT-brightgreen" />
    </a>
</p>

Functions and CLI for extracting data from Eclipse run decks and results.

This library builds upon [ecl](github.com/equinor/ecl) and add safer/easier methods using context managers to extract data.

Currenly `ecl` is only available via pip on Linux and MacOS but windows installable artifacts can be found [here](github.com/trhallam/ecl).

## Installation

`eclx` is available via `pip`.

```
pip install eclx
```

## Functions and Classes

`eclx` provides the following functions and classes.

```
from eclx import (
  EclDeck, # class for handling ecl decks
  open_EclFile, # context manager for Ecl files e.g. INIT, UNRST
  open_EclGrid, # context manager for Ecl grid files e.g. EGRID
  open_EclSum, # context manager for Ecl summary files e.g. SUM
  get_filetype, # method to discover the type of Eclipse file
  get_ecl_deck,  # method to get all related files in an Eclipse deck, requires the files are named the same
  load_ecl_property, # load a 3d grid property (requires the grid file) as a dataframe
  load_ecl_grid_index,  # load the 3d cell index as a dataframe
  get_ecl_property_keys, # get a list of all the 3d property keys in a file
  load_ecl_grid, # load an ecl grid (corner points) as a dataframe
  load_init_intehead, # load INIT intehead keyword
  load_ecl_rst, # load restart 3d grid properties for a given report into a dataframe
  get_restart_reports,  # get all of the reports available for a deck
  get_summary_keys, # get the curve keys from the Eclipse summary file (well curves)
  load_summary_df, # load the summary curves into a dataframe
)
```

## CLI

The command-line interface has three sub-commands `report`, `summary` and `simx`. 

Help menus for each sub-command are available using the `--help` flag.
