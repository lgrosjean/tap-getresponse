import typing as t

from singer_sdk import typing as th

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

    # Source: https://sdk.meltano.com/en/v0.25.0/parent_streams.html
    def get_child_context(self, record: dict, context: t.Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "campaignId": record["campaignId"],
        }


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
