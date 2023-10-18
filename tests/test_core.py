"""Tests standard tap features using the built-in SDK tests library

Source: https://github.com/meltano/sdk/blob/main/singer_sdk/testing/tap_tests.py
"""

import os

from tap_getresponse.tap import TapGetResponse

SAMPLE_CONFIG = {
    "auth_token": os.getenv("TAP_GETRESPONSE_AUTH_TOKEN"),
}

tap = TapGetResponse(config=SAMPLE_CONFIG)


def test_tap_cli_prints() -> None:
    """Test that the tap is able to print standard metadata."""
    tap.print_version()
    tap.print_about()
    tap.print_about(output_format="json")


def test_tap_stream_connection() -> None:
    """
    Test that the tap can connect to each stream.
    Run connection test, aborting each stream after 1 record.
    """
    tap.run_connection_test()
