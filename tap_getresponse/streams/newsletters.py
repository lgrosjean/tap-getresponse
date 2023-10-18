import typing as t

from singer_sdk import typing as th

from tap_getresponse.client import GetResponseStream


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
            description="The newsletter type",
            default="broadcast",
            allowed_values=["broadcast", "draft"],
        ),
        th.Property(
            "status",
            th.StringType,
            description="The newsletter status",
            allowed_values=["enabled", "disabled"],
        ),
        th.Property(
            "editor",
            th.StringType,
            description="This describes how the content of the message was created",
            # allowed_values=["custom", "text", "getresponse", "legacy", "html2"],
        ),
        th.Property(
            "subject",
            th.StringType,
            description="The message subject",
        ),
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
            description="The 'From' email address used for the message",
        ),
        th.Property(
            "replyTo",
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
            description="The email that will be used as the reply-to address",
        ),
        th.Property(
            "campaign",
            th.ObjectType(
                th.Property(
                    "Campaign ID",
                    th.StringType,
                    description="The 'From' address ID",
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
            "createdOn",
            th.DateTimeType,
            description="The creation date",
        ),
        th.Property(
            "sendOn",
            th.DateTimeType,
            description="The scheduled send date and time for the newsletter in the ISO 8601 format.",
        ),
        th.Property(
            "content",
            th.ObjectType(
                th.Property(
                    "html",
                    th.StringType,
                    description="The message content in HTML",
                ),
                th.Property(
                    "plain",
                    th.StringType,
                    description="The plain text equivalent of the message content",
                ),
            ),
            description="The message content.",
        ),
        th.Property(
            "attachments",
            th.ArrayType(
                th.ObjectType(
                    th.Property("fileName", th.StringType, description="The file name"),
                    th.Property(
                        "content",
                        th.StringType,
                        description="The base64 encoded file content",
                    ),
                    th.Property(
                        "mimeType", th.StringType, description="The file mime type"
                    ),
                )
            ),
            description="The newsletter attachments. The size of all attachments combined can't exceed 400KB",
        ),
        th.Property(
            "clickTracks",
            th.ArrayType(
                th.ObjectType(
                    th.Property("clickTrackId", th.StringType),
                    th.Property("url", th.URIType, description="The tracked link"),
                    th.Property(
                        "name", th.StringType, description="The tracked link name"
                    ),
                    # TODO: normally string regarding documentation but got some O value (int)
                    # th.Property(
                    #     "amount",
                    #     th.StringType,
                    #     description="The number of clicks on a link in a message",
                    # ),
                )
            ),
            description="The list of tracked links",
        ),
        th.Property(
            "sendMetrics",
            th.ObjectType(
                th.Property(
                    "status",
                    th.StringType,
                    allowed_values=["scheduled", "in_progress", "finished"],
                    default="finished",
                ),
                th.Property("sent", th.StringType, description="Messages already sent"),
                th.Property(
                    "total",
                    th.StringType,
                    description="The total amount of messages to send",
                ),
            ),
            description="The sending metrics",
        ),
        # th.property("sendSettings")
    ).to_dict()  # type: ignore


class NewsletterActivitiesStream(GetResponseStream):
    """
    Get newsletter activities.

    By default, activities from the last 14 days are listed only.
    """

    name = "newsletter_activities"
    path = "/newsletters/{newsletterId}/activities"

    parent_stream_type = NewslettersStream

    schema = th.PropertiesList(
        th.Property(
            "activity",
            th.StringType,
            description="The type of activity",
            allowed_values=["send", "open", "click"],
        ),
        th.Property(
            "createdOn",
            th.DateTimeType,
            description="The date when activity occurred",
        ),
        th.Property(
            "contact",
            th.ObjectType(
                th.Property("contactId", th.StringType, description="The contact ID"),
                th.Property(
                    "href", th.URIType, description="Direct hyperlink to a resource"
                ),
            ),
        ),
    ).to_dict()  # type: ignore
