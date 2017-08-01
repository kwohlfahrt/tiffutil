from tiffutil.crop import *
import pytest
import numpy as np

from util import runner

def test_parse_roi():
    expected = [slice(10, 20), slice(14, 22)]
    assert parseROI("10,20,14,+8".split(',')) == expected

def test_crop(tmpdir, runner):
    data = np.arange(100, dtype='uint8').reshape(4, 5, 5)
    tifpath = str(tmpdir.join('input.tif'))
    imsave(tifpath, data)

    outpath = str(tmpdir.join('output1.tif'))
    result = runner.invoke(crop, [tifpath, outpath] + "2 +2 1 5".split())
    assert result.exit_code == 0
    np.testing.assert_equal(imread(outpath), data[:, 1:5, 2:4])
