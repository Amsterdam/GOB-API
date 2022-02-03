# -*- coding: utf-8 -*-
import datetime
from abc import abstractmethod

from graphql import DirectiveLocation, GraphQLDirective, GraphQLArgument, GraphQLNonNull, GraphQLString
from promise import Promise


class CustomDirectivesMiddleware:

    def resolve(self, next_mw, root, info, **kwargs):
        result = next_mw(root, info, **kwargs)
        return result.then(
            lambda resolved: self.__process_value(resolved, root, info),
            lambda error: Promise.rejected(error)
        )

    def __process_value(self, value, root, info):
        field = info.field_asts[0]
        if not field.directives:
            return value

        new_value = value
        for directive in field.directives:
            directive_class = CustomDirectiveMeta.REGISTRY[directive.name.value]
            new_value = directive_class.process(new_value, directive, root, info)

        return new_value


class CustomDirectiveMeta(type):
    REGISTRY = {}

    def __new__(mcs, name, bases, attrs):
        newclass = super(CustomDirectiveMeta, mcs).__new__(mcs, name, bases, attrs)
        if name != 'BaseCustomDirective':
            mcs.register(newclass)
        return newclass

    @classmethod
    def register(mcs, target):
        mcs.REGISTRY[target.get_name()] = target

    @classmethod
    def get_all_directives(mcs):
        return [directive() for directive in mcs.REGISTRY.values()]

    @abstractmethod
    def get_name(cls):
        pass


class BaseCustomDirective(GraphQLDirective, metaclass=CustomDirectiveMeta):

    def __init__(self):
        super().__init__(
            name=self.get_name(),
            description=self.__doc__,
            args=self.get_args(),
            locations=[DirectiveLocation.FIELD]
        )

    @classmethod
    def get_name(cls):
        return cls.__name__.replace('Directive', '').lower()

    @staticmethod
    def get_args():
        return {}

    @staticmethod
    def process(value, directive, root, info):
        return value


class FormatDate(BaseCustomDirective):
    """Formats a date or datetime as string to specified format."""

    @staticmethod
    def get_args():
        return {
            'format': GraphQLArgument(
                type_=GraphQLNonNull(GraphQLString),
                description='Format Date or DateTime value in this format.',
            )
        }

    @staticmethod
    def process(value, directive, root, info):
        if not isinstance(value, datetime.date):  # True for datetime and date
            return value

        fmt = [arg for arg in directive.arguments if arg.name.value == 'format'][0]
        return value.strftime(fmt.value.value)
