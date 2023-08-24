"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_getresponse.tap import TapGetResponse

SAMPLE_CONFIG = {
    "auth_token": "auth_token",
}


# Run standard built-in tap tests from the SDK:
TestTapGetResponse = get_tap_test_class(
    tap_class=TapGetResponse,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
