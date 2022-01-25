# eclx

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
  EclResult, # class for handling ecl decks
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
