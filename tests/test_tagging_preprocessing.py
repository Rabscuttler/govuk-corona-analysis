from datetime import datetime
from pandas.testing import assert_frame_equal, assert_series_equal
from src.make_feedback_tagging.tagging_preprocessing import (
    convert_object_to_datetime,
    find_duplicated_rows,
    rank_rows,
    rank_tags,
    standardise_columns,
)
from typing import Callable, Union
import pandas as pd
import pytest

# Define arguments for to test `standardise_columns` in the `test_function_returns_correctly` test
args_function_returns_correctly_standardise_columns_returns_correctly = [
    ([pd.DataFrame(columns=["a", "b"])], pd.DataFrame(columns=["a", "b"])),
    ([pd.DataFrame(columns=["a*!&b£)C_d", "e_f"])], pd.DataFrame(columns=["a_b_c_d", "e_f"])),
    ([pd.DataFrame({"A": [0, 1], "b c%^d(e!F": [2, 3]})], pd.DataFrame({"a": [0, 1], "b_c_d_e_f": [2, 3]}))
]

# Define arguments for to test `convert_object_datetime_formats_to_datetime` in the `test_function_returns_correctly`
# test
args_function_returns_correctly_convert_object_to_datetime = [
    ([pd.DataFrame({"col_a": ["2020-01-01 01:13:48 foo", "2020-04-23 19:49:23+00"], "col_b": [0, 1]}), "col_a"],
     pd.DataFrame({"col_a": [datetime(2020, 1, 1, 1, 13, 48), datetime(2020, 4, 23, 19, 49, 23)], "col_b": [0, 1]})),
    ([pd.DataFrame({"text_date": ["2020-12-29 18:28:43", "2020-02-17 12:07:04UTC"], "data": [2, 3]}), "text_date"],
     pd.DataFrame({"text_date": [datetime(2020, 12, 29, 18, 28, 43), datetime(2020, 2, 17, 12, 7, 4)], "data": [2, 3]}))
]

# Define arguments for to test `find_duplicated_rows` in the `test_function_returns_correctly` test
args_function_returns_correctly_find_duplicated_rows = [
    ([pd.DataFrame({"id": [0, 1, 2], "col_a": [3, 4, 5], "col_b": [6, 7, 8]}), ["col_a", "col_b"]],
     pd.DataFrame(index=pd.Int64Index([]), columns=["id", "col_a", "col_b"], dtype="int64")),
    ([pd.DataFrame({"id": [0, 1, 2], "col_a": [3, 4, 4], "col_b": [6, 7, 7]}), ["col_a", "col_b"]],
     pd.DataFrame({"id": [1, 2], "col_a": [4, 4], "col_b": [7, 7]}, index=pd.Int64Index([1, 2])))
]

# Define arguments for to test `rank_rows` in the `test_function_returns_correctly` test
args_function_returns_correctly_rank_rows = [
    ([pd.DataFrame({"id": [0, 1, 2, 3], "col_rank": [8, 9, 6, 7]}), "col_rank"],
     pd.Series([2, 1, 4, 3], dtype="float64", name="col_rank")),
    ([pd.DataFrame({"id": [0, 1, 2, 3], "col_rank": [8, 9, 6, 7]}), "col_rank", "first"],
     pd.Series([2, 1, 4, 3], dtype="float64", name="col_rank")),
    ([pd.DataFrame({"id": [0, 1, 2, 3], "col_rank": [8, 8, 6, 7]}), "col_rank", "first"],
     pd.Series([1, 2, 4, 3], dtype="float64", name="col_rank")),
    ([pd.DataFrame({"id": [0, 1, 2, 3], "col_rank": [8, 8, 6, 7]}), "col_rank", "average"],
     pd.Series([1.5, 1.5, 4, 3], dtype="float64", name="col_rank")),
    ([pd.DataFrame({"id": [0, 1, 2, 3], "col_rank": [8, 8, 6, 7]}), "col_rank", "min"],
     pd.Series([1, 1, 4, 3], dtype="float64", name="col_rank")),
    ([pd.DataFrame({"id": [0, 1, 2, 3], "col_rank": [8, 8, 6, 7]}), "col_rank", "max"],
     pd.Series([2, 2, 4, 3], dtype="float64", name="col_rank")),
    ([pd.DataFrame({"id": [0, 1, 2, 3], "col_rank": [8, 8, 6, 7]}), "col_rank", "dense"],
     pd.Series([1, 1, 3, 2], dtype="float64", name="col_rank")),
    ([pd.DataFrame({"id": [0, 1, 2, 3], "col_rank": [8, 9, 6, 7]}), "col_rank", "first", False],
     pd.Series([2, 1, 4, 3], dtype="float64", name="col_rank")),
    ([pd.DataFrame({"id": [0, 1, 2, 3], "col_rank": [8, 9, 6, 7]}), "col_rank", "first", True],
     pd.Series([3, 4, 1, 2], dtype="float64", name="col_rank")),
]

# Define arguments for to test `rank_tags` in the `test_function_returns_correctly` test
args_function_returns_correctly_rank_tags = [
    ([pd.DataFrame({"col_tag": ["a", "b", "c", "d"], "data": [0, 1, 2, 3]}), "col_tag", pd.Series([4, 3, 2, 1]),
      {"b": -1, "d": -2}],
     pd.Series([7, 2, 5, 1])),
    ([pd.DataFrame({"col_tag": ["a", "b", "c", "d"], "data": [0, 1, 2, 3]}), "col_tag", pd.Series([4, 3, 2, 1]),
      {"a": -6, "b": -1, "d": -2}],
     pd.Series([1, 6, 9, 5]))
]

# Create the test cases for the `test_function_returns_correctly` test
args_function_returns_correctly = [
    *[(standardise_columns, *a) for a in args_function_returns_correctly_standardise_columns_returns_correctly],
    *[(convert_object_to_datetime, *a) for a in args_function_returns_correctly_convert_object_to_datetime],
    *[(find_duplicated_rows, *a) for a in args_function_returns_correctly_find_duplicated_rows],
    *[(rank_rows, *a) for a in args_function_returns_correctly_rank_rows],
    *[(rank_tags, *a) for a in args_function_returns_correctly_rank_tags],
]


@pytest.mark.parametrize("test_func, test_input, test_expected", args_function_returns_correctly)
def test_function_returns_correctly(test_func: Callable[..., Union[pd.DataFrame, pd.Series]], test_input,
                                    test_expected):
    """Test the a function, test_func, returns correctly, as long as test_func outputs a pandas DataFrame or Series."""
    if isinstance(test_expected, pd.DataFrame):
        assert_frame_equal(test_func(*test_input), test_expected)
    else:
        assert_series_equal(test_func(*test_input), test_expected)


def test_convert_object_to_datetime_raises_error_for_nat():
    """Test that the convert_object_to_datetime function returns an AssertionError if not all times could be parsed."""
    with pytest.raises(AssertionError):
        _ = convert_object_to_datetime(pd.DataFrame({"text_date": ["2020-12-29 18:28:43", None], "data": [2, 3]}),
                                       "text_date")


# Define some test cases for the `test_rank_tags_raises_assertion_error` test
args_rank_tags_raises_assertion_error = [a for args in args_function_returns_correctly_rank_tags for a in args[:-1]]


@pytest.mark.parametrize("test_input_df, test_input_col_tag, test_input_s_ranked, test_input_set_tag_ranks",
                         args_rank_tags_raises_assertion_error)
def test_rank_tags_raises_assertion_error(test_input_df, test_input_col_tag, test_input_s_ranked,
                                          test_input_set_tag_ranks):
    """Test rank_tags raises an assertion error if the lengths of df and s_ranked do not match."""

    # Iterate over the length of `test_input_s_ranked`, and execute `rank_tags` with a filtered `test_input_s_ranked`
    # less than its original length - should always raise an `AssertionError` with a specific message
    for ii in range(len(test_input_s_ranked) - 1):
        with pytest.raises(AssertionError, match=f"'s_ranked', and 'df' must be the same length!: {ii:,} != "
                                                 f"{len(test_input_df):,}"):
            rank_tags(test_input_df, test_input_col_tag, test_input_s_ranked.iloc[:ii], test_input_set_tag_ranks)
