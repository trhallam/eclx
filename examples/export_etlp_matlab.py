# Example of how to use eclx to export files for ELTPs Matlab Sim2seis

import pathlib
from eclx import EclDeck
from eclx._eclmaps import EclUnitMap, EclUnitScaler
from eclx._utils import _check_ijk_dim


def write_space_delim_file(
    df,
    filename,
    props=None,
    comments="%",
    fliphand=False,
    units=None,
    order=("i", "j", "k"),
):
    """"""
    ecl_index = ["i", "j", "k"]
    if props is None:
        props = df.columns
    else:
        props = ecl_index + [prop for prop in props if prop not in ecl_index]

    ni, nj, nk = _check_ijk_dim(df)
    units = units if units else -1

    # write zeros for missing props
    for prop in props:
        if prop not in df.columns:
            df[prop] = 0

    data = df[list(props)]

    # sort for ijk output
    if fliphand:
        data["j"] = nj - data["j"]

    data = data.sort_values(list(order))
    for v in ecl_index:
        data[v] = data[v] + 1

    with open(filename, "w") as out:
        out.write(comments + str(filename) + "\n")
        out.write("% Fixed Width export from eclx for ETLP" + "\n")
        out.write(
            "% Grid dimensions nx,ny,nz and mapunit (0=feet, 1=metres, -1=unknown)"
            + "\n"
        )
        out.write(f" {ni:4d} {nj:4d} {nk:4d} {units:4d}" + "\n")
        out.write(comments + " " + " ,".join(data.columns) + "\n")

    data.to_csv(
        filename,
        mode="a",
        sep=" ",
        header=False,
        line_terminator="",
        index=False,
        float_format="%.4f",
    )


def vsh_from_ntg(df):
    return 1 - df["NTG"].clip(0, 1)


if __name__ == "__main__":
    reports_to_load = [0, 2]
    path_to_deck = pathlib.Path("../tests/resources/t1a/TUT1A.DATA")
    output_filename = path_to_deck.stem

    deck = EclDeck()
    deck.set_grid(path_to_deck.with_suffix(".EGRID"))
    deck.set_init(path_to_deck.with_suffix(".INIT"))
    deck.set_rst(path_to_deck.with_suffix(".UNRST"))

    deck.load_grid()
    deck.load_init()
    deck.load_rst(reports=reports_to_load)

    # calculate a VSH property somehow
    deck.data["VSH"] = vsh_from_ntg(deck.data)

    # transform units to metric if necessary
    sim_units = EclUnitMap(deck.init_intehead["UNITS"]).name
    unit_scalar = EclUnitScaler[sim_units].value

    print("deck in units:", sim_units)
    # scale pressure to etlp metric units
    for col in deck.data.columns:
        if "PRESSURE" in col:
            deck.data[col] = deck.data[col] * unit_scalar["pressure"]

    # transform coordinates as well (say from ft to meters)
    for col in deck.corner_names:
        deck.xyzcorn[col] = deck.xyzcorn[col] * unit_scalar["length"]

    # write etlpgrid file
    print(f"Writing grid file")
    write_space_delim_file(
        deck.xyzcorn.drop(["active"], axis=1), output_filename + ".etlpgrid", units=1
    )

    # write etlpstat file
    print(f"Writing stat file")
    write_space_delim_file(
        deck.data,
        output_filename + ".etlpstat",
        props=["actnum", "VSH", "PORO", "PORV", "SATNUM"],
        units=1,
    )

    # write etlpdyn files
    for rep in reports_to_load:
        print(f"Writing dyn file {rep}")
        try:
            deck.data[f"SOIL_{rep}"] = (
                1 - deck.data[f"SWAT_{rep}"] - deck.data[f"SGAS_{rep}"]
            )
        except KeyError:
            # NO GAS SATURATION
            deck.data[f"SOIL_{rep}"] = 1 - deck.data[f"SWAT_{rep}"]

        write_space_delim_file(
            deck.data,
            output_filename + f"_{rep}.etlpdyn",
            units=1,
            props=[
                f"SGAS_{rep}",
                f"SOIL_{rep}",
                f"SWAT_{rep}",
                f"GAS_PRES_{rep}",
                f"PRESSURE_{rep}",
                f"WAT_PRES_{rep}",
                f"RS_{rep}",
                f"ES_{rep}",
            ],
        )
