"""pepperjam tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_pepperjam import streams


class TapPepperjam(Tap):
    """pepperjam tap class."""

    name = "tap-pepperjam"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "api_version",
            th.StringType,
            required=True,
            description="API Version",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.mysample.com",
            description="The url for the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.pepperjamStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.TransactionsStream(self),
            streams.PaymentsStream(self),
            streams.SkusStream(self),
        ]


if __name__ == "__main__":
    TapPepperjam.cli()
