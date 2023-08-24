"""GetResponse tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_getresponse import streams


class TapGetResponse(Tap):
    """GetResponse tap class."""

    name = "tap-getresponse"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.GetResponseStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.CampaignsStream(self),
            streams.ContactsStream(self),
        ]


if __name__ == "__main__":
    TapGetResponse.cli()  # pylint: disable=E1120
