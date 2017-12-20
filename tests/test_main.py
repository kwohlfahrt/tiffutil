from tiffutil.main import *


def test_help(runner):
    # Smoke test, mainly to make sure handling missing Matplotlib is OK
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
