"""
Dump GOB

Dumps of catalog collections in csv format
"""
import re

from gobapi.dump.config import DELIMITER_CHAR, QUOTATION_CHAR
from gobapi.dump.config import REFERENCE_TYPES, get_reference_fields
from gobapi.dump.config import JSON_TYPES

from gobapi.dump.config import get_unique_reference, add_unique_reference, is_unique_id
from gobapi.dump.config import get_field_specifications, get_field_order, get_field_value, joined_names

regex_crlf = re.compile(r"\r?\n")


def _csv_line(values: list) -> str:
    """
    Returns a CSV line for the given values

    :param values:
    :return:
    """
    return DELIMITER_CHAR.join(values) + "\n"


def _csv_value(value) -> str:
    """
    Return the CSV value for a given value

    :param value:
    :return:
    """
    if value is None:
        return ""
    elif isinstance(value, (int, float)):
        # Do not surround numeric values with quotes
        return str(value)
    else:
        value = str(value)
        value = regex_crlf.sub(" ", value)
        value = value.replace(QUOTATION_CHAR, 2 * QUOTATION_CHAR)
        return f"{QUOTATION_CHAR}{value}{QUOTATION_CHAR}"


def _csv_reference_values(value, spec) -> list:
    """
    Returns the CSV values for the given reference and type specification
    Note that the result is an array, as a reference value results in multiple CSV values

    :param value:
    :return:
    """
    values = []

    if spec['type'] == "GOB.Reference":
        dst = value or {}
        add_unique_reference(dst)

        for field in get_reference_fields(spec):
            sub_value = dst.get(field, None)
            values.append(_csv_value(sub_value))

    else:  # GOB.ManyReference
        dsts = value or []

        for dst in dsts:
            add_unique_reference(dst)

        for field in get_reference_fields(spec):
            sub_values = []

            for dst in dsts:
                sub_value = dst.get(field, None)
                sub_values.append(_csv_value(sub_value))

            values.append("[" + ",".join(sub_values) + "]")
    return values


def _csv_values(value, spec) -> list:
    """
    Returns the CSV values for the given value and type specification
    Note that the result is an array, as reference value result in multiple CSV values

    :param value:
    :return:
    """
    if spec['type'] in REFERENCE_TYPES:
        return _csv_reference_values(value, spec)

    elif spec['type'] in JSON_TYPES:
        if isinstance(value, list):
            values = []

            for field in spec['attributes'].keys():
                sub_values = []

                for row in value:
                    sub_value = row.get(field, '')
                    sub_values.append(_csv_value(sub_value))

                values.append("[" + ",".join(sub_values) + "]")

            return values
        else:
            value = value or {}
            return [_csv_value(value.get(field)) for field in spec['attributes'].keys()]
    else:
        return [_csv_value(value)]


class CsvDumper:

    def __init__(self, entities, model=None, ignore_fields=None, header=True):
        if model:
            self.field_specs = get_field_specifications(model)
            self.field_order = [f for f in get_field_order(model) if f not in (ignore_fields or [])]
        else:
            self.field_specs, self.field_order = {}, []

        self.field_names = self._get_field_names()
        self.include_header = header
        self.entities = entities

    def _get_field_names(self) -> list:
        """
        Returns the fieldnames for field specifications, based on the field order

        :return:
        """
        fields = []

        for field_name in self.field_order:
            field_spec = self.field_specs[field_name]

            if field_spec['type'] in REFERENCE_TYPES:
                for reference_field in get_reference_fields(field_spec):
                    fields.append(joined_names(field_name, reference_field))

            elif field_spec['type'] in JSON_TYPES:
                for field in field_spec['attributes'].keys():
                    fields.append(joined_names(field_name, field))

            else:
                fields.append(field_name)

        return fields

    def _csv_header(self) -> str:
        return _csv_line([_csv_value(field) for field in self.field_names])

    def _csv_record(self, entity) -> str:
        """
        Returns the CSV record fields for the given entity and corresponding type specifications
        :param entity:
        :return:
        """
        fields = []
        specs = self.field_specs

        for field_name in self.field_order:
            field_spec = specs[field_name]

            if is_unique_id(field_name):
                value = get_unique_reference(entity, field_name, specs)
            else:
                value = get_field_value(entity, field_name, field_spec)

            fields.extend(_csv_values(value, field_spec))

        return _csv_line(fields)

    def __iter__(self) -> str:
        """
        Yield the given entities as a list, starting with a header.

        :return:
        """
        _header_yielded = False

        for entity in self.entities:
            if not _header_yielded and self.include_header:
                yield self._csv_header()
                _header_yielded = True

            yield self._csv_record(entity)
