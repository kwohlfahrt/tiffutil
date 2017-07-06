from tiffutil.bin import *
from tiffutil.main import main
import numpy as np
from tifffile import TiffWriter, TiffFile

import pytest

@pytest.fixture()
def runner():
    from click.testing import CliRunner
    return CliRunner()

def test_commandline(tmpdir, runner):
    infile = tmpdir.join('in.tif')
    outfile = tmpdir.join('out.tif')
    data = np.random.uniform(0, 256, size=(100, 100)).astype('uint32')
    nbins = 4
    expected = np.sum((data[i::nbins] for i in range(nbins)))
    with TiffWriter(str(infile)) as tif:
        tif.save(data)

    args = [str(infile), str(outfile), "-n", str(nbins)]
    result = runner.invoke(main, ["bin"] + args)
    assert result.exit_code == 0

    with TiffFile(str(outfile)) as tif:
        output = tif.asarray()

    np.testing.assert_array_equal(output, expected)
