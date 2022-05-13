import pytest

from eclx import open_EclSum, get_summary_keys, load_summary_df

from ecl.summary import EclSum


def test_open_EclSum(eclipse_runs):
    sum_file = eclipse_runs["SUM"][0]

    with open_EclSum(sum_file) as sf:
        assert isinstance(sf, EclSum)


# reproducing these segmentation faults doesn't seem to be predictable
# def test_open_Eclsum_err(eclipse_runs):
#     with pytest.raises(FileNotFoundError):
#         with open_EclSum("not-a-file") as sf:
#             pass

#     not_a_sum_file = eclipse_runs["DATA"][0]
#     with pytest.raises(ValueError):
#         with open_EclSum(not_a_sum_file) as sf:
#             pass
