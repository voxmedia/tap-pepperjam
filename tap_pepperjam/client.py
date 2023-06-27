"""REST client handling, including pepperjamStream base class."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Iterable

import requests
from requests import Response
from singer_sdk.pagination import BaseAPIPaginator
from singer_sdk.streams import RESTStream

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class DayChunkAndTokenPaginator(BaseAPIPaginator):
    """custom paginator class."""

    def __init__(
        self,
        start_date: str,
        increment: int = 1,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(start_date)
        self._value = {"date": datetime.strptime(start_date, "%Y-%m-%d"), "page": 1}
        self._end = datetime.today()
        self._increment = increment

    @property
    def end_date(self):
        """Get the end pagination value.

        Returns:
            End date.
        """
        return self._end

    @property
    def increment(self):
        """Get the paginator increment.

        Returns:
            Increment.
        """
        return self._increment

    def get_next(self, response: Response):
        if self.has_more:
            if "next" in response.json()["meta"]["pagination"]:
                return {
                    "date": self.current_value["date"],
                    "page": self.current_value["page"] + 1,
                }
            return {
                "date": self.current_value["date"]
                + timedelta(
                    days=self.increment,
                ),
                "page": 1,
            }
        return None

    def has_more(self, response: Response) -> bool:
        """Checks if there are more days to process.

        Args:
            response: API response object.

        Returns:
            Boolean flag used to indicate if the endpoint has more pages.
        """
        return (
            "next" in response.json()["meta"]["pagination"]
            or self.current_value["date"]
            + timedelta(
                days=self.increment,
            )
            < self.end_date
        )


def set_none_or_cast(value, expected_type):
    if value == "" or value is None:
        return None
    elif not isinstance(value, expected_type):
        return expected_type(value)
    else:
        return value


class PepperjamStream(RESTStream):
    """pepperjam stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return (
            "https://api.pepperjamnetwork.com/"
            + self.config["api_version"]
            + "/publisher/report"
        )

    # Set this value or override `get_new_paginator`.
    next_page_token_jsonpath = "$.meta.next"  # noqa: S105

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
        return headers

    def get_new_paginator(self) -> DayChunkAndTokenPaginator:
        return DayChunkAndTokenPaginator(
            start_date=self.config.get("start_date"),
            increment=28,
        )

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {
            "format": "json",
            "apiKey": self.config.get("auth_token"),
            "website": "all",
        }
        date_format_str = "%Y-%m-%d"
        next_page_date = datetime.strftime(
            next_page_token["date"],
            date_format_str,
        )
        if next_page_date:
            params["startDate"] = next_page_date
            end_datetime = (
                datetime.strptime(
                    next_page_date,
                    date_format_str,
                )
                + timedelta(days=28)
                if datetime.strptime(
                    next_page_date,
                    date_format_str,
                )
                + timedelta(days=28)
                < datetime.now()
                else datetime.now()
            )
            params["endDate"] = datetime.strftime(end_datetime, date_format_str)
            params["page"] = next_page_token["page"]
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        records = response.json()["data"]
        yield from records

    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        for field_tuple in [
            ("transaction_id", int),
            ("program_id", int),
            ("commission", float),
            ("sale_amount", float),
            ("payment_id", int),
            ("advertiser_id", int),
            ("creative_id", int),
        ]:
            field_name = field_tuple[0]
            field_type = field_tuple[1]
            if field_name in row:
                row[field_name] = set_none_or_cast(row[field_name], field_type)
        return row
