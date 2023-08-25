"""Stream type classes for tap-getresponse."""

from __future__ import annotations

import typing as t
from pathlib import Path

import requests
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_getresponse.client import GetResponseStream, extract_jsonpath

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class CampaignsStream(GetResponseStream):
    """Get a list of campaigns"""

    name = "campaigns"
    path = "/campaigns"
    primary_keys: t.ClassVar[list[str]] = ["campaignId"]
    schema = th.PropertiesList(
        th.Property(
            "description",
            th.StringType,
            description="same as the campaign name, kept for compatibility reasons",
        ),
        th.Property(
            "campaignId",
            th.StringType,
            description="Campaign ID",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The campaign (list) name.",
        ),
        th.Property(
            "techName",
            th.StringType,
            description="Unique internal ID of a list used for FTP imports",
        ),
        th.Property(
            "languageCode",
            th.StringType,
            description="The campaign language code according to ISO 639-1",
        ),
        th.Property(
            "isDefault",
            th.BooleanType,
            description="Is the campaign default",
        ),
        th.Property(
            "createdOn",
            th.DateTimeType,
            description="The date of creation",
        ),
        th.Property(
            "href",
            th.URIType,
            description="Direct hyperlink to a resource",
        ),
    ).to_dict()  # type: ignore

    # Source: https://sdk.meltano.com/en/v0.25.0/parent_streams.html
    def get_child_context(self, record: dict, context: t.Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "campaignId": record["campaignId"],
        }


# Source: https://sdk.meltano.com/en/v0.25.0/parent_streams.html
class CampaignDetailsStream(GetResponseStream):
    """Get a single campaign by the campaign ID"""

    name = "campaign_details"
    path = "/campaigns/{campaignId}"

    parent_stream_type = CampaignsStream

    primary_keys: t.ClassVar[list[str]] = ["campaignId"]

    schema = th.PropertiesList(
        th.Property(
            "campaignId",
            th.StringType,
            description="Campaign ID",
        ),
        th.Property(
            "name",
            th.StringType,
            required=True,
            description="The campaign (list) name.",
        ),
        th.Property(
            "confirmation",
            th.ObjectType(
                th.Property(
                    "fromField",
                    th.ObjectType(
                        th.Property(
                            "fromFieldId",
                            th.StringType,
                            required=True,
                            description="The 'From' address ID",
                        ),
                        th.Property(
                            "href",
                            th.URIType,
                            description="Direct hyperlink to a resource",
                        ),
                    ),
                ),
                th.Property(
                    "mimeType",
                    th.StringType,
                    description="The MIME type for the confirmation message",
                ),
                th.Property(
                    "redirectUrl",
                    th.URIType,
                    description="The URL a subscriber will be redirected to if the redirectType is set to customUrl",
                ),
            ),
        ),
    ).to_dict()  # type: ignore


class ContactsStream(GetResponseStream):
    """Get a list of contacts"""

    name = "contacts"
    path = "/contacts"
    primary_keys: t.ClassVar[list[str]] = ["contactId"]
    schema = th.PropertiesList(
        th.Property(
            "contactId",
            th.StringType,
            required=True,
        ),
        th.Property(
            "name",
            th.StringType,
            description="Contact's name",
        ),
        th.Property(
            "origin",
            th.StringType,
            # TODO: add enum Enum:"import" "email" "www" "panel" "leads" "sale" "api" "forward" "survey" "iphone" "copy" "landing_page" "website_builder_elegant"
        ),
        th.Property(
            "timeZone",
            th.StringType,
            description="The time zone of a contact, uses the time zone database format (https://www.iana.org/time-zones)",
        ),
        th.Property(
            "activities",
            th.URIType,
            description="Contact's activities",
        ),
        th.Property(
            "changedOn",
            th.DateTimeType,
        ),
        th.Property(
            "createdOn",
            th.DateTimeType,
        ),
        th.Property(
            "campaign",
            th.ObjectType(
                th.Property("campaignId", th.StringType, required=True),
                th.Property("href", th.StringType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "email",
            th.StringType,
            required=True,
        ),
        th.Property(
            "scoring",
            th.NumberType,
            description="Contact scoring, pass null to remove the score from a contact",
        ),
        th.Property(
            "engagementScore",
            th.IntegerType,
            # allowed_values=Enum ...,
            description="Engagement Score is a feature that presents a visual estimate of a contact's engagement with mailings. The score is based on the contact's interactions with your e-mails. Via API, it's returned in the form of numbers ranging from 1 (Not Engaged) to 5 (Highly Engaged).",
        ),
        th.Property(
            "href",
            th.StringType,
            required=True,
        ),
        # th.Property(
        #     "ipAddress",
        #     th.IPv4Type,
        #     description="The contact's IP address. IPv4 and IPv6 formats are accepted.",
        # ),
    ).to_dict()  # type: ignore


class NewslettersStream(GetResponseStream):
    """Get the list of newsletters"""

    name = "newsletters"
    path = "/newsletters"
    primary_keys: t.ClassVar[list[str]] = ["newsletterId"]

    schema = th.PropertiesList(
        th.Property(
            "newsletterId",
            th.StringType,
            required=True,
            description="The newsletter ID",
        ),
        th.Property(
            "href",
            th.URIType,
            required=True,
            description="Direct hyperlink to a resource",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The newsletter name",
        ),
        th.Property(
            "type",
            th.StringType,
            # TODO: add  Enum:"broadcast" "draft"
            description="The newsletter type",
        ),
        th.Property(
            "status",
            th.StringType,
            # TODO: add  Enum:"enabled" "disabled"
            description="The newsletter status",
        ),
        th.Property(
            "editor",
            th.StringType,
            # TODO: Enum:"custom" "text" "getresponse" "legacy" "html2"
            description="This describes how the content of the message was created",
        ),
        th.Property(
            "subject",
            th.StringType,
            description="The message subject",
        ),
        th.Property(
            "campaign",
            th.ObjectType(
                th.Property(
                    "campaignId",
                    th.StringType,
                    required=True,
                    description="Campaign ID",
                ),
                th.Property(
                    "href",
                    th.URIType,
                    description="Direct hyperlink to a resource",
                ),
                th.Property(
                    "name",
                    th.StringType,
                    description="The campaign name",
                ),
            ),
            description="The newsletter must be assigned to a campaign",
        ),
        th.Property(
            "sendOn",
            th.DateTimeType,
            description="The scheduled send date and time for the newsletter in the ISO 8601 format",
        ),
        th.Property(
            "createdOn",
            th.DateTimeType,
            description="The creation date",
        ),
        th.Property(
            "sendMetrics",
            th.ObjectType(
                # TODO: Enum:"scheduled" "in_progress" "finished"
                th.Property(
                    "status",
                    th.StringType,
                ),
                th.Property(
                    "sent",
                    th.StringType,
                    description="Messages already sent",
                ),
                th.Property(
                    "total",
                    th.StringType,
                    description="The total amount of messages to send",
                ),
            ),
            description="The sending metrics",
        ),
        th.Property(
            "flags",
            th.StringType,
            description="Comma-separated list of message flags. The possible values are: openrate, clicktrack, and google_analytics.",
        ),
    ).to_dict()  # type: ignore

    # Source: https://sdk.meltano.com/en/v0.25.0/parent_streams.html
    def get_child_context(self, record: dict, context: t.Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "newsletterId": record["newsletterId"],
        }


class NewsletterDetailsStream(GetResponseStream):
    """Get a single newsletter by its ID"""

    name = "newsletter_details"
    path = "/newsletters/{newsletterId}"

    parent_stream_type = NewslettersStream

    primary_keys: t.ClassVar[list[str]] = ["newsletterId"]

    schema_filepath = SCHEMAS_DIR / "newsletter_details.json"  # type: ignore


class NewsletterActivitiesStream(GetResponseStream):
    """
    Get newsletter activities.

    By default, activities from the last 14 days are listed only.
    """

    name = "newsletter_activities"
    path = "/newsletters/{newsletterId}/activities"

    parent_stream_type = NewslettersStream

    schema_filepath = SCHEMAS_DIR / "newsletter_activities.json"  # type: ignore

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """The response must be parsed to convert to raw result which is a list to a dict"""

        data = response.json()
        input_ = {"activities": data}

        yield from extract_jsonpath(self.records_jsonpath, input=input_)
