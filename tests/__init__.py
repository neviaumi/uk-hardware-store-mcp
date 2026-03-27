import os

import pytest

IS_CI = os.getenv("CI", "false") == "true"

skip_if_ci = pytest.mark.skipif(IS_CI, reason="tests only run locally")
