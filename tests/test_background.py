from tiffutil.background import *
import numpy as np
from tifffile import TiffWriter, TiffFile


def test_smooth():
    data = np.array([0.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 0.0])
    expected = np.array([0.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0])
    tolerance = np.array([1e-100, 1e-1, 1e-100, 1e-100, 1e-100, 1e-100, 1e-1, 1e-100])
    np.testing.assert_array_less(abs(smooth(data, 3.0) - expected), tolerance)


def test_smooth_inverted():
    data = np.array([0.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 0.0])
    expected = np.array([1.4, 1.4, 2.0, 2.0, 2.0, 1.4, 1.0, 0.4])
    tolerance = np.array([1e-1, 1e-1, 1e-100, 1e-100, 1e-100, 1e-1, 1e-100, 1e-1])
    np.testing.assert_array_less(abs(smooth(data, 3.0, invert=True) - expected), tolerance)


def test_commandline(tmpdir, runner):
    infile = tmpdir.join('in.tif')
    outfile = tmpdir.join('out.tif')
    data = np.random.uniform(0, 256, size=(100, 100)).astype('float32')
    with TiffWriter(str(infile)) as tif:
        tif.save(data)

    args = [str(infile), str(outfile), "--radius", "2.0"]
    result = runner.invoke(background, args)
    assert result.exit_code == 0

    with TiffFile(str(outfile)) as tif:
        output = tif.asarray()

    np.testing.assert_array_equal(output <= data, True)


def test_commandline_correct(tmpdir, runner):
    infile = tmpdir.join('in.tif')
    outfile = tmpdir.join('out.tif')
    data = np.random.randint(0, 256, size=(100, 100)).astype('float32')
    with TiffWriter(str(infile)) as tif:
        tif.save(data)

    args = [str(infile), str(outfile), "--radius", "2.0", "--correct"]
    result = runner.invoke(background, args)
    assert result.exit_code == 0

    with TiffFile(str(outfile)) as tif:
        output = tif.asarray()

    np.testing.assert_array_equal(output <= data, True)
    assert output.shape == data.shape


def test_video(tmpdir, runner):
    infile = tmpdir.join('in.tif')
    outfile = tmpdir.join('out.tif')
    data = np.random.uniform(0, 256, size=(10, 100, 100)).astype('float32')
    with TiffWriter(str(infile)) as tif:
        tif.save(data)

    args = [str(infile), str(outfile), "--radius", "2.0"]
    result = runner.invoke(background, args)
    assert result.exit_code == 0

    with TiffFile(str(outfile)) as tif:
        output = tif.asarray()

    np.testing.assert_array_equal(output <= data, True)
