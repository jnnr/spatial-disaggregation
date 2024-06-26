import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
import rioxarray as rxr

from spatial_disaggregation.disaggregate import disaggregate_polygon_to_raster


@pytest.fixture
def dummy_raster():
    return rxr.open_rasterio("test/_files/raster.tif").squeeze(drop=True)


@pytest.fixture
def square_segmentation_2x2():
    return gpd.read_file("test/_files/segmentation_2x2.geojson").set_index("id")


@pytest.fixture
def square_segmentation_3x3():
    return gpd.read_file("test/_files/segmentation_3x3.geojson").set_index("id")


def test_disaggregate_using_proxy_2x2(dummy_raster, square_segmentation_2x2):
    data = square_segmentation_2x2

    data["value"] = [2, 2, 2, 2]

    expected = [
        [0.72727273, 0., 0., 0.],
        [0.54545455, 0.72727273, 1., 1.],
        [2., 0., 0.25, 0.75],
        [0., 0., 0.25, 0.75],
    ]

    disaggregated = disaggregate_polygon_to_raster(data=data, crs=dummy_raster.rio.crs, proxy=dummy_raster)

    assert (disaggregated.coarsen(x=2, y=2).sum()["value"].values == [[2, 2], [2, 2]]).all()

    assert np.allclose(disaggregated['value'].values, expected)


def test_disaggregate_using_resolution_2x2():
    pass


def test_disaggregate_using_proxy_3x3():
    pass
