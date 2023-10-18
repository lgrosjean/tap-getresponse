import typing as t

from singer_sdk import typing as th

from tap_getresponse.client import GetResponseStream


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

    # Source: https://sdk.meltano.com/en/v0.25.0/parent_streams.html
    def get_child_context(self, record: dict, context: t.Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "contactId": record["contactId"],
        }


class ContactDetailsStream(GetResponseStream):
    """Get contact details by contact ID"""

    name = "contact_details"
    path = "/contacts/{contactId}"

    parent_stream_type = ContactsStream

    primary_keys: t.ClassVar[list[str]] = ["contactId"]

    schema = th.PropertiesList(
        th.Property("contactId", th.StringType, required=True),
        th.Property("name", th.StringType),
        th.Property("origin", th.StringType),
        th.Property(
            "timeZone",
            th.StringType,
            description="The time zone of a contact, uses the time zone database format",
        ),
        th.Property("activities", th.URIType),
        th.Property("changedOn", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
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
        ),
        th.Property("email", th.EmailType),
        # th.Property("dayOfCycle", th.StringType),
        th.Property(
            "scoring",
            th.NumberType,
            description="Contact scoring, pass null to remove the score from a contact",
        ),
        th.Property(
            "engagementScore",
            th.IntegerType,
            allowed_values=[None, 1, 2, 3, 4, 5],
            description="""
            Engagement Score is a feature that presents a visual estimate of a contact's 
            engagement with mailings. The score is based on the contact's interactions 
            with your e-mails. Via API, it's returned in the form of numbers ranging 
            from 1 (Not Engaged) to 5 (Highly Engaged).
            """,
        ),
        th.Property(
            "href",
            th.URIType,
            required=True,
            description="Direct hyperlink to a resource",
        ),
        th.Property("note", th.StringType),
        th.Property(
            "ipAddress",
            th.StringType,
            description="The contact's IP address. IPv4 and IPv6 formats are accepted.",
        ),
        th.Property(
            "geolocation",
            th.ObjectType(
                th.Property("latitude", th.StringType),
                th.Property("longitude", th.StringType),
                th.Property(
                    "continentCode",
                    th.StringType,
                    allowed_values=["", "OC", "AN", "SA", "NA", "AS", "EU", "AF"],
                ),
                th.Property(
                    "countryCode",
                    th.StringType,
                    description="The country code, compliant with ISO 3166-1 alpha-2",
                ),
                th.Property("region", th.StringType),
                th.Property("postalCode", th.StringType),
                # th.Property("dmaCode", th.StringType),
                th.Property("city", th.StringType),
            ),
        ),
        th.Property(
            "customFieldValues",
            th.ArrayType(
                th.ObjectType(
                    th.Property("customFieldId", th.StringType, required=True),
                    th.Property("name", th.StringType, required=True),
                    th.Property("type", th.StringType),
                    th.Property("value", th.ArrayType(th.StringType)),
                    th.Property("values", th.ArrayType(th.StringType)),
                )
            ),
            description="The list of tracked links",
        ),
    ).to_dict()  # type: ignore


class ContactActivitiesStream(GetResponseStream):
    """
    Get a list of contact activities

    By default, only activities from the last 14 days are returned.
    TODO: To get earlier data, use `query[createdOn]` parameter from config file.

    Source: https://apireference.getresponse.com/#operation/getActivities
    """

    name = "contact_activities"
    path = "/contacts/{contactId}/activities"

    parent_stream_type = ContactsStream

    primary_keys: t.ClassVar[list[str]] = ["contactId"]

    schema = th.PropertiesList(
        th.Property("contactId", th.StringType, required=True),
        th.Property(
            "activity",
            th.StringType,
            description="The type of activity",
            allowed_values=["send", "open", "click"],
        ),
        th.Property("subject", th.StringType),
        th.Property("createdOn", th.DateTimeType, description="The activity date"),
        th.Property(
            "previewUrl",
            th.URIType,
            description="""This is only available for the send activity.
            It includes a link to the message preview""",
        ),
        th.Property(
            "resource",
            th.ObjectType(
                th.Property("resourceId", th.StringType),
                th.Property(
                    "resourceType",
                    th.StringType,
                    allowed_values=[
                        None,
                        "newsletters",
                        "splittests",
                        "autoresponders",
                        "rss-newsletters",
                        "sms",
                    ],
                ),
                th.Property(
                    "href", th.URIType, description="Direct hyperlink to a resource"
                ),
            ),
        ),
        th.Property(
            "clickTrack",
            th.ObjectType(
                th.Property("id", th.StringType, description="The click tracking ID"),
                th.Property(
                    "name", th.StringType, description="The name of the clicked link"
                ),
                th.Property(
                    "url", th.URIType, description="The URL of the clicked link"
                ),
            ),
        ),
    ).to_dict()  # type: ignore

    def post_process(
        self,
        row: dict,
        context: t.Optional[dict] = None,  # noqa: ARG002
    ) -> t.Union[dict, None]:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        row["contactId"] = context["contactId"]
        return row
