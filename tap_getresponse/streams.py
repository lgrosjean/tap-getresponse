"""Stream type classes for tap-getresponse."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_getresponse.client import GetResponseStream


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
