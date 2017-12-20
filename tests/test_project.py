from tiffutil.project import *
from tifffile import TiffWriter, TiffFile
from itertools import tee
import pytest

import numpy as np


def test_rollingmedian():
    data = iter(range(0, 10))
    expected = list(range(1, 9))
    assert list(rollingMedian(data, 3)) == expected


def test_multireduce():
    assert multiReduce([min, max], tee(range(20), 2)) == (0, 19)


def test_multireduce_np():
    import numpy as np
    from numpy.testing import assert_equal

    data = np.array([[1, 2, 3], [1, 4, -10], [5, 2, 0]])
    reduced = multiReduce([np.fmax, np.fmin], tee(data, 2))
    expected = map(np.asarray, ([5, 4, 3], [1, 2, -10]))
    for r, e in zip(reduced, expected):
        assert_equal(r, e)


@pytest.mark.parametrize("f, arg", [
    (np.amax, "max"), (np.amin, "min"), (np.mean, "mean")
])
def test_commandline(f, arg, tmpdir, runner):
    infile = tmpdir.join('in.tif')
    outfile = tmpdir.join('out.tif')
    rng = np.random.RandomState(4)
    data = rng.uniform(0, 256, size=(5, 10, 10)).astype('float32')
    with TiffWriter(str(infile)) as tif:
        tif.save(data)

    args = [str(infile), str(outfile), "--projection", arg, "--end", "2"]
    result = runner.invoke(project, args)
    assert result.exit_code == 0

    with TiffFile(str(outfile)) as tif:
        output = tif.asarray()

    np.testing.assert_array_equal(output, f(data[:2], axis=0))
