# Generated from gobapi/graphql_streaming/graphql2sql/grammar/GraphQL.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GraphQLParser import GraphQLParser
else:
    from GraphQLParser import GraphQLParser

# This class defines a complete generic visitor for a parse tree produced by GraphQLParser.

class GraphQLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GraphQLParser#document.
    def visitDocument(self, ctx:GraphQLParser.DocumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#definition.
    def visitDefinition(self, ctx:GraphQLParser.DefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#operationDefinition.
    def visitOperationDefinition(self, ctx:GraphQLParser.OperationDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#selectionSet.
    def visitSelectionSet(self, ctx:GraphQLParser.SelectionSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#operationType.
    def visitOperationType(self, ctx:GraphQLParser.OperationTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#selection.
    def visitSelection(self, ctx:GraphQLParser.SelectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#field.
    def visitField(self, ctx:GraphQLParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#fieldName.
    def visitFieldName(self, ctx:GraphQLParser.FieldNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#alias.
    def visitAlias(self, ctx:GraphQLParser.AliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#arguments.
    def visitArguments(self, ctx:GraphQLParser.ArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#argument.
    def visitArgument(self, ctx:GraphQLParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#fragmentSpread.
    def visitFragmentSpread(self, ctx:GraphQLParser.FragmentSpreadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#inlineFragment.
    def visitInlineFragment(self, ctx:GraphQLParser.InlineFragmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#fragmentDefinition.
    def visitFragmentDefinition(self, ctx:GraphQLParser.FragmentDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#fragmentName.
    def visitFragmentName(self, ctx:GraphQLParser.FragmentNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#directives.
    def visitDirectives(self, ctx:GraphQLParser.DirectivesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#directive.
    def visitDirective(self, ctx:GraphQLParser.DirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#typeCondition.
    def visitTypeCondition(self, ctx:GraphQLParser.TypeConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#variableDefinitions.
    def visitVariableDefinitions(self, ctx:GraphQLParser.VariableDefinitionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#variableDefinition.
    def visitVariableDefinition(self, ctx:GraphQLParser.VariableDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#variable.
    def visitVariable(self, ctx:GraphQLParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#defaultValue.
    def visitDefaultValue(self, ctx:GraphQLParser.DefaultValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#valueOrVariable.
    def visitValueOrVariable(self, ctx:GraphQLParser.ValueOrVariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#stringValue.
    def visitStringValue(self, ctx:GraphQLParser.StringValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#numberValue.
    def visitNumberValue(self, ctx:GraphQLParser.NumberValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#booleanValue.
    def visitBooleanValue(self, ctx:GraphQLParser.BooleanValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#arrayValue.
    def visitArrayValue(self, ctx:GraphQLParser.ArrayValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#ttype.
    def visitTtype(self, ctx:GraphQLParser.TtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#typeName.
    def visitTypeName(self, ctx:GraphQLParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#listType.
    def visitListType(self, ctx:GraphQLParser.ListTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#nonNullType.
    def visitNonNullType(self, ctx:GraphQLParser.NonNullTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#nameArray.
    def visitNameArray(self, ctx:GraphQLParser.NameArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQLParser#array.
    def visitArray(self, ctx:GraphQLParser.ArrayContext):
        return self.visitChildren(ctx)



del GraphQLParser