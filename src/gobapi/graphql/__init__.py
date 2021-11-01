"""GraphQL

"""
import graphene

from gobcore.model.metadata import PRIVATE_META_FIELDS, FIXED_FIELDS
from gobapi.graphql.scalars import Date, DateTime, GeoJSON, Scalar
from graphql.language.ast import IntValue


class BigInt(Scalar):
    """
    The `BigInt` scalar type represents non-fractional whole numeric values.
    `BigInt` is not constrained to 32-bit like the `Int` type and thus is a less
    compatible type.
    """

    @staticmethod
    def coerce_int(value):
        try:
            num = int(value)
        except ValueError:
            try:
                num = int(float(value))
            except ValueError:
                return None
        return num

    serialize = coerce_int
    parse_value = coerce_int

    @staticmethod
    def parse_literal(ast):
        if isinstance(ast, IntValue):
            return int(ast.value)


def graphene_type(gob_typename, description=""):
    """Get the corresponding Graphene type for any GOB type

    :param gob_typename: The typename within GOB
    :param description: The description to add to the Graphene type
    :return: The Graphene type if a corresponding type can be found, else None
    """
    conversion = {
        "GOB.Character": graphene.String,
        "GOB.String": graphene.String,
        "GOB.Integer": graphene.Int,
        "GOB.BigInteger": BigInt,
        "GOB.Decimal": graphene.Float,
        "GOB.Boolean": graphene.Boolean,
        "GOB.Date": Date,
        "GOB.DateTime": DateTime,
        "GOB.Geo.Geometry": GeoJSON,
        "GOB.JSON": graphene.JSONString,
        "GOB.IncompleteDate": graphene.JSONString,
        # Secure types match their 'base type', datetimes are converted to strings
        "GOB.SecureString": graphene.String,
        "GOB.SecureDecimal": graphene.Float,
        "GOB.SecureDateTime": graphene.String,
        "GOB.SecureIncompleteDate": graphene.JSONString,
    }
    if conversion.get(gob_typename):
        return conversion.get(gob_typename)(description=description)


# Not all GOB fields are exposed in the GraphQL interface
exclude_fields = tuple(name for name in {**PRIVATE_META_FIELDS, **FIXED_FIELDS}.keys())
