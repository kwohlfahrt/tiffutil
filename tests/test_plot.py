import numpy as np
from tifffile import imsave
import pytest

pytest.importorskip("matplotlib")

from tiffutil.plot import *  # noqa: E402


def test_commandline(tmpdir, runner):
    data = [np.random.randint(0, 255, size=(20, 20), dtype='uint8'),
            np.random.randint(0, 255, size=(20, 20), dtype='uint8')]
    inputs = list(map(tmpdir.join, map("{}.tif".format, range(len(data)))))
    for img, tifpath in zip(data, inputs):
        imsave(str(tifpath), img)

    outpath = str(tmpdir.join('output.pdf'))
    args = [
        "--channel", "0", "0", "1", str(inputs[0]),
        "--channel", "1", "1", "0", str(inputs[1]),
        "--output", str(outpath), "--scalebar", "100", "μm", "1000"
    ]
    result = runner.invoke(plot, args)
    assert result.exit_code == 0
