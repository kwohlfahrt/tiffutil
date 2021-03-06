from tiffutil.bin import *  # noqa: F401
import numpy as np
from tifffile import TiffWriter, TiffFile


def test_commandline(tmpdir, runner):
    infile = tmpdir.join('in.tif')
    outfile = tmpdir.join('out.tif')
    data = np.random.randint(0, 256, size=(20, 10, 10)).astype('uint32')
    nbins = 4
    expected = np.sum((data[i::nbins] for i in range(nbins)))
    with TiffWriter(str(infile)) as tif:
        tif.save(data)

    args = [str(infile), str(outfile), "-n", str(nbins)]
    result = runner.invoke(bin, args)
    assert result.exit_code == 0

    with TiffFile(str(outfile)) as tif:
        output = tif.asarray()

    np.testing.assert_array_equal(output, expected)
