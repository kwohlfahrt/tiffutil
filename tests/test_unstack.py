import pytest
import numpy as np

from tifffile import TiffWriter, TiffFile

from tiffutil.unstack import *
from util import runner

def test_unstack(tmpdir, runner):
    data = np.random.randint(0, 200, size=(10, 32, 32)).astype('uint8')
    tifpath = tmpdir.join("test.tif")
    with TiffWriter(str(tifpath)) as f:
        f.save(data)

    outputs = list(map(str, map(tmpdir.join, map("out{}.tif".format, range(2)))))
    result = runner.invoke(unstack, [str(tifpath)] + outputs)
    assert result.exit_code == 0

    expecteds = np.rollaxis(data.reshape(5, 2, 32, 32), 1)
    for output, expected in zip(map(TiffFile, outputs), expecteds):
        with output as f:
            np.testing.assert_equal(f.asarray(), expected)

def test_unstack_axis(tmpdir, runner):
    data = np.random.randint(0, 200, size=(4, 10, 32, 32)).astype('uint8')
    tifpath = tmpdir.join("test.tif")
    with TiffWriter(str(tifpath)) as f:
        f.save(data)

    outputs = list(map(str, map(tmpdir.join, map("out{}.tif".format, range(2)))))
    result = runner.invoke(unstack, ["--axis", "1", str(tifpath)] + outputs)
    assert result.exit_code == 0

    expecteds = np.rollaxis(data.reshape(20, 2, 32, 32), 1)
    for output, expected in zip(map(TiffFile, map(str, outputs)), expecteds):
        with output as f:
            np.testing.assert_equal(f.asarray(), expected)
