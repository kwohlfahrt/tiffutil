from tiffutil.project import *
import numpy as np

def test_rollingmedian():
    data = iter(range(0, 10))
    expected = list(range(1, 9))
    assert list(rollingMedian(data, 3)) == expected

def test_multireduce():
    assert multiReduce([min, max], range(20)) == (0, 19)

def test_multireduce_np():
    import numpy as np
    from numpy.testing import assert_equal

    data = np.array([[1, 2, 3], [1, 4, -10], [5, 2, 0]])
    reduced = multiReduce([np.fmax, np.fmin], data)
    expected = map(np.asarray, ([5, 4, 3], [1, 2, -10]))
    for r, e in zip(reduced, expected):
        assert_equal(r, e)

def test_tiffchain(tmpdir):
    from tifffile import TiffWriter, TiffFile

    offsets = np.arange(3)
    files = list(map(tmpdir.join, map("{}.tif".format, offsets)))
    writers = map(TiffWriter, map(str, files))

    data = np.arange(10) + (offsets * 10)[:, None]
    for writer, a in zip(writers, data):
        with writer:
            writer.save(a)

    series = chain.from_iterable(TiffFile(str(f)).series for f in files)
    np.testing.assert_equal(list(tiffChain(series)), np.concatenate(data))

    series = chain.from_iterable(TiffFile(str(f)).series for f in files)
    np.testing.assert_equal(list(tiffChain(series, start=12, end=22)),
                            np.concatenate(data)[12:22])
