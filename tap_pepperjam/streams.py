"""Stream type classes for tap-pepperjam."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_pepperjam.client import PepperjamStream


class TransactionsStream(PepperjamStream):
    """Define custom stream."""

    name = "transactions"
    path = "/transaction-details"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("transaction_id", th.IntegerType),
        th.Property(
            "status",
            th.StringType,
        ),
        th.Property(
            "program_id",
            th.IntegerType,
        ),
        th.Property(
            "order_id",
            th.StringType,
        ),
        th.Property("commission", th.NumberType),
        th.Property(
            "creative_type",
            th.StringType,
        ),
        th.Property(
            "sale_amount",
            th.NumberType,
        ),
        th.Property(
            "type",
            th.StringType,
        ),
        th.Property(
            "date",
            th.DateTimeType,
        ),
        th.Property(
            "new_to_file",
            th.BooleanType,
        ),
        th.Property(
            "publisher_referral_url",
            th.StringType,
        ),
        th.Property(
            "sub_type",
            th.StringType,
        ),
        th.Property(
            "sid",
            th.StringType,
        ),
        th.Property(
            "program_name",
            th.StringType,
        ),
        th.Property(
            "website",
            th.StringType,
        ),
    ).to_dict()


class PaymentsStream(PepperjamStream):
    """Define custom stream."""

    name = "payments"
    path = "/payment-details"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("sid", th.StringType),
        th.Property(
            "program_id",
            th.IntegerType,
        ),
        th.Property(
            "program_name",
            th.StringType,
        ),
        th.Property(
            "order_id",
            th.StringType,
        ),
        th.Property(
            "sale_amount",
            th.NumberType,
        ),
        th.Property(
            "creative_type",
            th.StringType,
        ),
        th.Property(
            "payment_id",
            th.IntegerType,
        ),
        th.Property(
            "transaction_type",
            th.StringType,
        ),
        th.Property(
            "transaction_id",
            th.IntegerType,
        ),
        th.Property(
            "payment_date",
            th.DateTimeType,
        ),
        th.Property(
            "transaction_date",
            th.DateTimeType,
        ),
        th.Property("commission", th.NumberType),
    ).to_dict()


class SkusStream(PepperjamStream):
    """Define custom stream."""

    name = "skus"
    path = "/sku-details"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("sku", th.StringType),
        th.Property("quantity", th.IntegerType),
        th.Property(
            "status",
            th.StringType,
        ),
        th.Property(
            "program_id",
            th.IntegerType,
        ),
        th.Property(
            "order_id",
            th.StringType,
        ),
        th.Property("commission", th.NumberType),
        th.Property(
            "date",
            th.DateTimeType,
        ),
        th.Property(
            "sub_type",
            th.StringType,
        ),
        th.Property(
            "sale_amount",
            th.NumberType,
        ),
        th.Property(
            "creative_type",
            th.StringType,
        ),
        th.Property(
            "advertiser_id",
            th.IntegerType,
        ),
        th.Property(
            "item_category_name",
            th.StringType,
        ),
        th.Property(
            "item_name",
            th.StringType,
        ),
        th.Property(
            "advertiser_name",
            th.StringType,
        ),
        th.Property(
            "transaction_id",
            th.IntegerType,
        ),
        th.Property(
            "sid_name",
            th.StringType,
        ),
        th.Property(
            "transaction_type",
            th.StringType,
        ),
        th.Property(
            "creative_id",
            th.IntegerType,
        ),
    ).to_dict()
