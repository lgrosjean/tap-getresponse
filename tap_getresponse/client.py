"""REST client handling, including GetResponseStream base class."""

from __future__ import annotations

import typing as t

import requests
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BasePageNumberPaginator
from singer_sdk.streams import RESTStream


class GetResponsePaginator(BasePageNumberPaginator):
    """
    Source: https://sdk.meltano.com/en/latest/classes/singer_sdk.pagination.BasePageNumberPaginator.html
    """

    start_value = 1

    def __init__(self):
        super().__init__(start_value=self.start_value)

    def get_next(self, response) -> int | None:
        if "currentPage" in response.headers:
            current_page = response.headers["CurrentPage"]
            return int(current_page) + 1
        return None

    def has_more(self, response) -> bool:
        if "currentPage" in response.headers:
            current_page = int(response.headers["CurrentPage"])
            total_pages = int(response.headers["TotalPages"])
            return current_page < total_pages
        return False


class GetResponseStream(RESTStream):
    """GetResponse stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        # TODO: retrieve it from self.config for custom base url or use it by default
        return "https://api3.getresponse360.pl/v3"

    records_jsonpath = "$[*]"  # Or override `parse_response`.

    # Set this value or override `get_new_paginator`.
    # next_page_token_jsonpath = "$.next_page"  # noqa: S105

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="X-Auth-Token",
            value=f"api-key {self.config.get('auth_token', '')}",
            location="header",
        )

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
        return headers

    def get_new_paginator(self) -> GetResponsePaginator:
        """Create a new pagination helper instance.

        https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html#how-to-migrate

        Returns:
            A pagination helper instance.
        """
        return GetResponsePaginator()

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        params["perPage"] = self.config.get("per_page", 1000)
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    def prepare_request_payload(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ARG002, ANN401
    ) -> dict | None:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary with the JSON body for a POST requests.
        """
        # TODO: Delete this method if no payload is required. (Most REST APIs.)
        return None

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

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
        # TODO: Delete this method if not needed.
        return row
