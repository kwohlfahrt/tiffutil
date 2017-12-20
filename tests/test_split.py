from tiffutil.split import *
from tifffile import imsave, imread
import numpy as np


def test_chunk():
    data = np.arange(100).reshape(20, 5)
    all_chunks = []
    for i, c in enumerate(map(np.stack, chunk(data, 6))):
        np.testing.assert_equal(c, data[i*6:(i+1)*6])
        all_chunks.append(c)
    np.testing.assert_equal(np.concatenate(all_chunks), data)


def test_crop(tmpdir, runner):
    data = np.arange(100, dtype='uint8').reshape(5, 4, 5)
    tifpath = str(tmpdir.join('input.tif'))
    imsave(tifpath, data)

    outpath = str(tmpdir.join('output{}.tif'))
    result = runner.invoke(split, [tifpath, outpath, "-n", "3"])
    assert result.exit_code == 0
    for i in range(2):
        np.testing.assert_equal(imread(outpath.format(i)), data[i*3:(i+1)*3])
