import typing as t

from singer_sdk import typing as th

from tap_getresponse.client import GetResponseStream


class WebinarsStream(GetResponseStream):
    """Get a list of webinars"""

    name = "webinars"
    path = "/webinars"
    primary_keys: t.ClassVar[list[str]] = ["webinarId"]
    schema = th.PropertiesList(
        th.Property(
            "webinarId",
            th.StringType,
        ),
        th.Property(
            "name",
            th.StringType,
        ),
        th.Property(
            "href",
            th.URIType,
            description="Direct hyperlink to a resource",
        ),
        th.Property(
            "createdOn",
            th.DateTimeType,
        ),
        th.Property(
            "startsOn",
            th.DateTimeType,
        ),
        th.Property(
            "webinarUrl",
            th.URIType,
            description="The URL to the webinar room",
        ),
        th.Property(
            "status",
            th.StringType,
            description="Enum:`upcoming` `finished` `published` `unpublished`",
            allowed_values=["upcoming", "finished", "published", "unpublished"],
        ),
        th.Property(
            "type",
            th.URIType,
            description="The webinar type",
            allowed_values=["all", "live", "on_demand"],
        ),
        th.Property(
            "campaigns",
            th.ArrayType(
                th.ObjectType(
                    th.Property("campaignId", th.StringType, required=True),
                    th.Property("href", th.StringType),
                    th.Property("name", th.StringType),
                ),
            ),
        ),
        th.Property(
            "newsletters",
            th.ArrayType(
                th.ObjectType(
                    th.Property("newsletterId", th.StringType, required=True),
                    th.Property("href", th.StringType, required=True),
                ),
            ),
            description="The list of invitation messages",
        ),
        th.Property(
            "statistics",
            th.ObjectType(
                th.Property("registrants", th.IntegerType, required=True),
                th.Property("visitors", th.IntegerType, required=True),
                th.Property("attendees", th.IntegerType, required=True),
            ),
        ),
    ).to_dict()  # type: ignore
