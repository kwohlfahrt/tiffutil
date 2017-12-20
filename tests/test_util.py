from tiffutil.util import *
from tifffile import imsave
import numpy as np
import pytest


def test_tifchain(tmpdir):
    shape = (5, 10, 10)
    tifpaths = list(map(str, map(tmpdir.join, map("test{}.tif".format, range(2)))))
    data = np.random.randint(0, 2**8, size=(len(tifpaths),) + shape).astype('uint8')
    for path, d in zip(tifpaths, data):
        imsave(path, d)

    tifs = list(map(TiffFile, tifpaths))
    chained = list(tiffChain(chain.from_iterable(tif.series for tif in tifs)))
    assert len(chained) == 10
    assert all(c.shape == shape[1:] for c in chained)


def test_atleast3D():
    shape = (5, 5, 5, 5)
    assert(atleast3D(np.ones(shape)).shape == shape)

    shape = (5, 5, 5)
    assert(atleast3D(np.ones(shape)).shape == shape)

    shape = (5, 5)
    assert(atleast3D(np.ones(shape)).shape == (1,) + shape)


def test_tifchain2d(tmpdir):
    shape = (10, 10)
    tifpaths = list(map(str, map(tmpdir.join, map("test{}.tif".format, range(2)))))
    data = np.random.randint(0, 2**8, size=(len(tifpaths),) + shape).astype('uint8')
    for path, d in zip(tifpaths, data):
        imsave(path, d)

    tifs = list(map(TiffFile, tifpaths))
    chained = list(tiffChain(chain.from_iterable(tif.series for tif in tifs)))
    assert len(chained) == 2
    assert all(c.shape == shape for c in chained)


def test_limits(tmpdir):
    shape = (5, 10, 10)
    tifpaths = list(map(str, map(tmpdir.join, map("test{}.tif".format, range(2)))))
    data = np.random.randint(0, 2**8, size=(len(tifpaths),) + shape).astype('uint8')
    for path, d in zip(tifpaths, data):
        imsave(path, d)

    tifs = list(map(TiffFile, tifpaths))
    chained = list(tiffChain(chain.from_iterable(tif.series for tif in tifs), 2, 6))
    assert len(chained) == 4
    assert all(c.shape == shape[1:] for c in chained)


@pytest.mark.parametrize("x, expected", [
    (np.dtype('uint8'), np.dtype('int16')),
    (np.dtype('int8'), np.dtype('int8')),
    (np.dtype('float32'), np.dtype('float32')),
])
def test_signed(x, expected):
    assert signed(x) == expected


@pytest.mark.parametrize("x", [
    np.dtype(('int32', 3)), np.dtype([('foo', 'int32')])
])
def test_signed_error(x):
    with pytest.raises(ValueError):
        signed(x)
