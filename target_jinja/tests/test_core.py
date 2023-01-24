"""Tests standard target features using the built-in SDK tests library."""

import datetime

from typing import Dict, Any

from singer_sdk.testing import get_standard_target_tests

from target_jinja.target import TargetJinja2

SAMPLE_CONFIG: Dict[str, Any] = {
    # TODO: Initialize minimal target config
}


# Run standard built-in target tests from the SDK:
def test_standard_target_tests():
    """Run standard target tests from the SDK."""
    tests = get_standard_target_tests(
        TargetJinja2,
        config=SAMPLE_CONFIG,
    )
    for test in tests:
        test()


# TODO: Create additional tests as appropriate for your target.
