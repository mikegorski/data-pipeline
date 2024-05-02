import re

from data_pipeline import __version__


def test_version_should_be_of_proper_format():
    pattern = r"\b\d+\.\d+\.\d+\b"
    match = re.match(pattern, __version__)
    assert match
