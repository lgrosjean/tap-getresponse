import typing as t

from singer_sdk import typing as th

from tap_getresponse.client import GetResponseStream


class SmsStream(GetResponseStream):
    """Get the list of SMS messages.

    See: https://apireference.getresponse.com/#operation/getSMSList
    """

    name = "sms"
    path = "/sms"
    primary_keys: t.ClassVar[list[str]] = ["smsId"]
    schema = th.PropertiesList(
        th.Property(
            "smsId", th.StringType, required=True, description="The SMS message ID"
        ),
        th.Property("href", th.URIType, required=True),
        th.Property("name", th.StringType, description="The SMS message name"),
        th.Property(
            "campaign",
            th.ObjectType(
                th.Property(
                    "campaignId",
                    th.StringType,
                    required=True,
                    description="Campaign ID",
                ),
                th.Property("name", th.StringType, description="The campaign name"),
            ),
        ),
        th.Property(
            "modifiedOn",
            th.DateTimeType,
            description="""The date the SMS message was last modified on,
            shown in ISO 8601 date and time format""",
        ),
        th.Property(
            "type",
            th.StringType,
            allowed_values=["sms", "draft"],
            description="The SMS message type",
        ),
        th.Property(
            "sendOn",
            th.ObjectType(
                th.Property(
                    "date",
                    th.DateTimeType,
                    description="""Send date. Shown in format ISO 8601 
                    without timezone offset""",
                ),
                # th.Property(
                #     "timeZone", th.ObjectType(), description="Time zone details"
                # ),
            ),
        ),
        th.Property(
            "recipientsType",
            th.StringType,
            allowed_values=["contacts", "importedNumbers"],
            description="Type of SMS message recipients",
        ),
        th.Property(
            "senderName",
            th.StringType,
            description="The SMS message sender name",
        ),
        th.Property(
            "content",
            th.StringType,
            description="The SMS message content",
        ),
        th.Property(
            "sendMetrics",
            th.ObjectType(
                th.Property("progress", th.StringType, description="Sending progress"),
                th.Property(
                    "status",
                    th.StringType,
                    allowed_values=["scheduled", "sending", "sent"],
                    description="Sending status",
                ),
            ),
            description="Information about sending process",
        ),
        th.Property(
            "statistics",
            th.ObjectType(
                th.Property(
                    "sent", th.IntegerType, description="Number of sent messages"
                ),
                th.Property(
                    "delivered",
                    th.IntegerType,
                    description="Number of delivered messages",
                ),
                th.Property(
                    "clicks",
                    th.IntegerType,
                    description="Number of clicked messages",
                ),
            ),
            description="Message statistics",
        ),
    ).to_dict()  # type: ignore

    # Source: https://sdk.meltano.com/en/v0.25.0/parent_streams.html
    def get_child_context(self, record: dict, context: t.Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "smsId": record["smsId"],
        }
