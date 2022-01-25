"""Interface for users to ecl by Statoil/Equinor

This interface builds entirely upon the ecl project.
https://github.com/Equinor/ecl

ecl is a library designed to interface directly with
Eclipse simulation files.

"""
# pylint: disable=invalid-name

import pathlib

import numpy as np
import pandas as pd

# from ecl import EclFileEnum
# from ecl.grid.ecl_grid import EclGrid
# from ecl.eclfile import EclFile
# from ecl.eclfile.ecl_restart_file import EclRestartHead

# from etlpy.core.exceptions import WorkflowError

from ._ecl_file import load_ecl_property
from ._grid import (
    load_ecl_grid_index,
    load_ecl_grid,
    get_ecl_grid_dims,
    _xcorn_names,
    _ycorn_names,
    _zcorn_names,
)
from ._init import load_init_intehead
from ._rst import is_restart_file, get_restart_reports, load_ecl_rst
from ._utils import import_tqdm

tqdm = import_tqdm()


class EclResult:
    """A class to encapsulate Eclipse Simulator Output Methods and Properties"""

    def __init__(self, silent=False):
        """Constructor

        Args:
            silent (bool, optional): Defaults to False, disable progress bars,
                log output
        """
        self.data = pd.DataFrame()
        self.units_updated = False
        self.egrid_file = None
        self.einit_file = None
        self.erst_file = None
        self.silent = silent
        self.loaded_reports = None
        self.nx = None
        self.ny = None
        self.nz = None
        self.mapaxes = None
        self.active = None
        self.coord = None
        self.xyzcorn = None
        self.zcorn_names = None
        self._xcorn_names = None
        self._ycorn_names = None
        self._zcorn_names = None
        self.keys_init = None
        self.init_intehead = dict()
        self.reports = None
        self.reports_dict = dict()
        self.dates = None
        self._unified_rst = None
        self._rst_file_map = None

    def set_grid(self, filepath):
        """Set the simulation grid file and initialise ecl link

        Arguments:
            filename {string}: Full file name and path
        """
        filepath = pathlib.Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Cannot find input file {filepath}")
        self.egrid_file = filepath

    def load_grid(self, filename=None):
        """Load the simulation grid file

        Arguments:
            filename (string): Defaults to None; Full file name and path
        """
        if filename is not None:
            self.set_grid(filename)
        elif self.egrid_file is None:
            raise ValueError("grid file has not been specified")

        self.nx, self.ny, self.nz = get_ecl_grid_dims(self.egrid_file)
        self.data = load_ecl_grid_index(self.egrid_file, silent=self.silent)
        self.xyzcorn = load_ecl_grid(self.egrid_file, silent=self.silent)

        self.data["centerx"] = self.xyzcorn[_xcorn_names()].mean(axis=1)
        self.data["centery"] = self.xyzcorn[_ycorn_names()].mean(axis=1)
        self.data["centerz"] = self.xyzcorn[_zcorn_names()].mean(axis=1)

    def _get_cornmin(self, full_grid, corn_names):
        """Calculate the min values for each cell, if full_grid is True get the overall grid
        minimum value from corn_names

        Args:
            full_grid (bool): Return minimum value for each cell or full grid
            corn_names (list): List of strings corresponding to corner names in self.zcorn
                e.g. self._xcorn_names

        Returns:
            minimum values from the grid of corn_names
        """
        if not full_grid:
            return self.xyzcorn[corn_names].min(axis=1)
        else:
            return self.xyzcorn[corn_names].min().min()

    def _get_cornmax(self, full_grid, corn_names):
        """Calculate the max values for each cell, if full_grid is True get the overall grid
        maximum value from corn_names

        Args:
            full_grid (bool): Return maximum value for each cell or full grid
            corn_names (list): List of strings corresponding to corner names in self.zcorn
                e.g. self._xcorn_names

        Returns:
            maximum values from the grid of corn_names
        """
        if not full_grid:
            return self.xyzcorn[corn_names].max(axis=1)
        else:
            return self.xyzcorn[corn_names].max().max()

    def get_cornxmin(self, full_grid=False):
        """Calculate the xmin for each corner, if full_grid is True get the overall
        grid minimum x value.
        """
        return self._get_cornmin(full_grid, self._xcorn_names)

    def get_cornxmax(self, full_grid=False):
        """Calculate the xmax for each corner, if full_grid is True get the overall
        grid maximum x value.
        """
        return self._get_cornmax(full_grid, self._xcorn_names)

    def get_cornymin(self, full_grid=False):
        """Calculate the ymin for each corner, if full_grid is True get the overall
        grid minimum y value.
        """
        return self._get_cornmin(full_grid, self._ycorn_names)

    def get_cornymax(self, full_grid=False):
        """Calculate the ymax for each corner, if full_grid is True get the overall
        grid maximum y value.
        """
        return self._get_cornmax(full_grid, self._ycorn_names)

    def get_cornzmin(self, full_grid=False):
        """Calculate the zmin for each corner, if all is True get the overall
        grid minimum z value.
        """
        return self._get_cornmin(full_grid, self._zcorn_names)

    def get_cornzmax(self, full_grid=False):
        """Calculate the zmin for each corner, if all is True get the overall
        grid maximum z value.
        """
        return self._get_cornmax(full_grid, self._zcorn_names)

    def get_cellside(self, gi, side, normal=False):
        """Get the corner points of a specified cell side number 1-6

            Side 1: Top -    corners 0, 2, 3, 1
            Side 2: Front -  corners 0, 1, 5, 4
            Side 3: Right -  corners 1, 3, 7, 5
            Side 4: Left -   corners 0, 4, 6, 2
            Side 5: Back -   corners 3, 2, 6, 7
            Side 6: Bottom - corners 4, 5, 7, 6

        Args:
            gi (int): The global index of the cell
            side (int): The side required value 1-6
            normal (bool, optional): Defaults to False. Return the normal of the cell
                The normal will always face inwards.
        """
        # By the right hand rule the normal for each face should point towards
        # the centre of the cell. This is important for log extraction when determing
        # whether a ray enters or exits a cell.
        cell = self.xyzcorn.iloc[gi]  # pandas data series
        if side < 7 and side > 0:  # return size by integer value
            f = [
                [0, 2, 3, 1],
                [0, 1, 5, 4],
                [1, 3, 7, 5],
                [0, 4, 6, 2],
                [3, 2, 6, 7],
                [4, 5, 7, 6],
            ][side - 1]
        else:
            raise ValueError("side must be in range 1 to 6")

        x = cell.filter([f"x{i}" for i in f]).values
        y = cell.filter([f"y{i}" for i in f]).values
        z = cell.filter([f"z{i}" for i in f]).values

        if normal:  # calculate normal by cross-product and reduction
            v0 = np.array([x[0], y[0], z[0]])
            v1 = np.array([x[1], y[1], z[1]])
            v2 = np.array([x[3], y[3], z[3]])
            n = np.cross(v1 - v0, v2 - v0)
            n = n / np.linalg.norm(n)
            return [x, y, z], n
        else:
            return [x, y, z]

    def get_grid_summary(self):
        """Print a summary of grid statistics"""
        print(f"Dual Porosity: {self.egrid.dual_grid()}")
        print(f"IJK Dimensions: {self.egrid.nx} {self.egrid.ny} {self.egrid.nz}")
        print(f"Map Axes: YX YY {self.mapaxes[0]} {self.mapaxes[1]}")
        print(f"          0X 0Y {self.mapaxes[2]} {self.mapaxes[3]}")
        print(f"          XX XY {self.mapaxes[4]} {self.mapaxes[5]}")

    def set_init(self, filepath):
        """Set the init simulation file

        Args:
            filepath (string): Full file name and path
        """
        filepath = pathlib.Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Cannot find input file {filepath}.")
        self.einit_file = filepath

    def load_init(self, filepath=None, keys=None):
        """Load the init simulation file

        keys are loaded into `pandas.DataFrame` `self.data`.

        Args:
            filepath (string) -- Full file name and path
            keys (list/str, optional): Key or list of keys to load.
                Defaults to None - loads all keys.
        """

        if filepath is not None:
            self.set_init(filepath)
        elif self.einit_file is None:
            raise ValueError("init file has not been specified")

        self.init_intehead = load_init_intehead(self.einit_file)

        # sanity checks
        if (
            self.init_intehead["NI"] != self.nx
            or self.init_intehead["NJ"] != self.ny
            or self.init_intehead["NK"] != self.nz
        ):
            raise ValueError("INIT file grid dimensions do not match grid dimensions.")

        data = load_ecl_property(
            self.einit_file,
            grid_filepath=self.egrid_file,
            keys=keys,
            silent=self.silent,
            report_index=0,
        )

        if self.data.empty:
            self.data = data
        else:
            self.data = self.data.join(data.iloc[:, 5:])

    def set_rst(self, filepath):
        """Load the report list and create report list dictionary

        Arguments:
            filepath (pathlike) -- The full path to the restart file.

        """
        filepath = pathlib.Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Cannot find input file {filepath}.")
        self.erst_file = str(filepath)

        if not is_restart_file(filepath):
            raise ValueError(
                f"The input filename {filepath} does not correspond to a restart file.  Please follow the Eclipse naming conventions"
            )

        self.dates = get_restart_reports(filepath)
        self.reports = self.dates["report"].to_list()


    def load_rst(self, reports=None, keys=None):
        """Load the restart file

        Arguments:
            reports ('all'/list) -- A list of report numbers else
                                     loads 'all' reports
        """
        if reports is None:
            reports = self.dates["report"].to_list()
        elif isinstance(reports, int):
            reports = [reports]
        elif not isinstance(reports, list):
            raise ValueError("Report should be one of None, int or list[int]")

        data_rst = load_ecl_rst(
            self.erst_file,
            grid_filepath=self.egrid_file,
            reports=reports,
            keys=keys,
            silent=self.silent,
        )

        if self.data.empty:
            self.data = data_rst
        else:
            self.data = self.data.join(data_rst.iloc[:, 5:])

        # # error reporting
        # if len(failed_keys) > 0:
        #     msg = "Invalid 3D KWs:" + ", ".join(failed_keys)
        #     print(msg)
        # if len(missing_keys) > 0:
        #     msg = "Missing requested 3D KWs:" + ", ".join(missing_keys)
        #     print(msg)

    def get_celldz_mean(self, df):
        """Calculates the minimum height of all active cells.

        This method is simple and relies on the diference between vertical corners
        that may also have an X, Y offset.
        """
        dz = np.zeros_like(df.x1)
        for i in range(0, 4):
            a = self._zcorn_names[i]
            b = self._zcorn_names[i + 4]
            dz += df[b] - df[a].values
            return dz / 4

    def get_zcorn_reduc(
        self, xmin=None, xmax=None, ymin=None, ymax=None, active=False, dzmin=None
    ):
        """Filter the xyzcorn DataFrame by setting cartesian boundary points.

        Args:
            xmin (float, optional): Defaults to None.
                Minimun x value to accept in output DataFrame.
            xmax (float, optional): Defaults to None.
                Maximum x value to accept in output DataFrame.
            ymin (float, optional): Defaults to None.
                Minimum y value to accept in output DataFrame.
            ymax (float, optional): Defaults to None.
                Maximum y value to accept in output DataFrame.
            active (bool): Defaults to False, if True return active cells only.

        Returns:
            [pandas.DataFrame]: self.xyzcorn filtered to boundary conditions.
        """
        zcorn_reduc = self.xyzcorn.copy(deep=True)
        zcorn_reduc.loc[:, "xmin"] = self.get_cornxmin()
        zcorn_reduc.loc[:, "xmax"] = self.get_cornxmax()
        zcorn_reduc.loc[:, "ymin"] = self.get_cornymin()
        zcorn_reduc.loc[:, "ymax"] = self.get_cornymax()
        query_mask = ""
        if active:
            query_mask += f"active >= 0 &"

        if xmin is not None:
            query_mask += f"xmin <= {xmax} &"
        if xmax is not None:
            query_mask += f"xmax >= {xmin} &"
        if ymin is not None:
            query_mask += f"ymin <= {ymax} &"
        if ymax is not None:
            query_mask += f"ymax >= {ymin} &"
        if dzmin is not None:
            zcorn_reduc["cell_dz"] = self.get_celldz_mean(zcorn_reduc)
            query_mask += f"cell_dz > {dzmin} &"
        if query_mask[-2:] == " &":
            query_mask = query_mask[:-2]
        if query_mask != "":
            zcorn_reduc.query(query_mask, inplace=True)
        return zcorn_reduc
