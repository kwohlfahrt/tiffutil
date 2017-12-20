from tiffutil.project import *
from tiffutil.main import main
from tifffile import TiffWriter, TiffFile

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


def test_commandline(tmpdir, runner):
    infile = tmpdir.join('in.tif')
    outfile = tmpdir.join('out.tif')
    data = np.random.uniform(0, 256, size=(5, 10, 10)).astype('float32')
    with TiffWriter(str(infile)) as tif:
        tif.save(data)

    args = [str(infile), str(outfile), "--projection", "max", "--end", "2"]
    result = runner.invoke(main, ["project"] + args)
    assert result.exit_code == 0

    with TiffFile(str(outfile)) as tif:
        output = tif.asarray()

    np.testing.assert_array_equal(output, data[:2].max(axis=0))
