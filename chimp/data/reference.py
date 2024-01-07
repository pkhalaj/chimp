"""
chimp.data.reference
===================

This module provides functions for loading CHIMP reference data.
"""
from dataclasses import dataclass
from typing import Union, List, Optional

import xarray as xr

from chimp.data.source import DataSource


def find_random_scene(
    reference_data,
    path,
    rng,
    multiple=4,
    window_size=256,
    qi_thresh=0.8,
    valid_fraction=0.2,
):
    """
    Finds a random scene in the reference data that has given minimum
    fraction of values of values exceeding a given RQI threshold.

    Args:
        reference_data: Reference data object describing the reference
            data.
        path: The path of the reference data file.
        rng: A numpy random generator instance to randomize the scene search.
        multiple: Limits the scene position to coordinates that a multiples
            of the given value.
        qi_thresh: Threshold for the minimum RQI of a reference pixel to
            be considered valid.
        valid_fraction: The minimum amount of valid samples in the
            region.

    Return:
        A tuple ``(i_start, i_end, j_start, j_end)`` defining the position
        of the random crop.
    """
    with xr.open_dataset(path) as data:
        qi = data[reference_data.quality_index].data

        found = False
        count = 0
        while not found:
            count += 1
            n_rows, n_cols = qi.shape
            i_start = rng.integers(0, (n_rows - window_size) // multiple)
            i_end = i_start + window_size // multiple
            j_start = rng.integers(0, (n_cols - window_size) // multiple)
            j_end = j_start + window_size // multiple

            i_start = i_start * multiple
            i_end = i_end * multiple
            j_start = j_start * multiple
            j_end = j_end * multiple

            row_slice = slice(i_start, i_end)
            col_slice = slice(j_start, j_end)

            if (qi[row_slice, col_slice] > qi_thresh).mean() > valid_fraction:
                found = True

    return (i_start, i_end, j_start, j_end)


@dataclass
class RetrievalTarget:
    """
    This dataclass holds properties of retrieval targets provided
    by a reference dataset.
    """

    name: str
    lower_limit: Optional[float] = None


ALL_REFERENCE_DATA = {}


@dataclass
class ReferenceData(DataSource):
    """
    This dataclass holds properties of reference datasets.
    """

    name: str
    scale: int
    targets: List[RetrievalTarget]
    quality_index: str

    def __init__(
        self, name: str, scale: int, targets: list[RetrievalTarget], quality_index: str
    ):
        super().__init__(name)
        ALL_REFERENCE_DATA[name] = self
        self.name = name
        self.scale = scale
        self.targets = targets
        self.quality_index = quality_index


def get_reference_data(name: Union[str, ReferenceData]) -> ReferenceData:
    """
    Retrieve reference dataset by name.

    Args:
        name: The name of a dataset.

    Return:
        A ReferenceData object that can be used to load reference data
        from the requested dataset.
    """
    from . import baltrad
    from . import mrms

    if isinstance(name, DataSource):
        return name
    if name in ALL_REFERENCE_DATA:
        return ALL_REFERENCE_DATA[name]

    raise ValueError(
        f"The reference data '{name}' is currently not available. Available "
        f" reference datasets are {list(ALL_REFERENCE_DATA.keys())}."
    )