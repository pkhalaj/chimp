"""
cimr.areas
==========

Contains area definitions for the regions used by CIMR.
"""
from pathlib import Path

import numpy as np
import pyresample

from pansat.roi import ROI, PolygonROI

###############################################################################
# Nordics
###############################################################################

NORDICS_1 = pyresample.load_area(Path(__file__).parent / "cimr_nordic_1.yml")
NORDICS_2 = pyresample.load_area(Path(__file__).parent / "cimr_nordic_2.yml")
NORDICS_4 = pyresample.load_area(Path(__file__).parent / "cimr_nordic_4.yml")
NORDICS_8 = pyresample.load_area(Path(__file__).parent / "cimr_nordic_8.yml")
ROI_NORDICS = ROI(
    -9.05380216185029,
    51.77251844681491,
    45.24074941367874,
    73.3321989854415
)
_lons, _lats = NORDICS_8.get_lonlats()
ROI_POLY_NORDICS =  PolygonROI(np.array([
    [_lons[0, 0], _lats[0, 0]],
    [_lons[0, -1], _lats[0, -1]],
    [_lons[-1, -1], _lats[-1, -1]],
    [_lons[-1, 0], _lats[-1, 0]],
]))

NORDICS = {
    1: NORDICS_1,
    2: NORDICS_2,
    4: NORDICS_4,
    8: NORDICS_8,
    "roi": ROI_NORDICS,
    "roi_poly": ROI_POLY_NORDICS
}

###############################################################################
# CONUS
###############################################################################

CONUS_4 = pyresample.load_area(Path(__file__).parent / "cimr_conus_4.yml")
CONUS_8 = pyresample.load_area(Path(__file__).parent / "cimr_conus_8.yml")
CONUS_16 = pyresample.load_area(Path(__file__).parent / "cimr_conus_16.yml")
ROI_CONUS = ROI(
    -129.995,
    20.005,
    -60.005,
    54.995
)
_lons, _lats = CONUS_8.get_lonlats()
ROI_POLY_CONUS =  PolygonROI(np.array([
    [_lons[0, 0], _lats[0, 0]],
    [_lons[0, -1], _lats[0, -1]],
    [_lons[-1, -1], _lats[-1, -1]],
    [_lons[-1, 0], _lats[-1, 0]],
]))

CONUS = {
    4: CONUS_4,
    8: CONUS_8,
    16: CONUS_16,
    "roi": ROI_CONUS,
    "roi_poly": ROI_POLY_CONUS
}

MRMS = pyresample.load_area(Path(__file__).parent / "mrms.yml")
