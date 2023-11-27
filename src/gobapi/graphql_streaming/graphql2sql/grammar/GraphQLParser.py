# Generated from gobapi/graphql_streaming/graphql2sql/grammar/GraphQL.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\31")
        buf.write("\u010b\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31")
        buf.write("\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36")
        buf.write("\4\37\t\37\3\2\6\2@\n\2\r\2\16\2A\3\3\3\3\5\3F\n\3\3\4")
        buf.write("\3\4\3\4\3\4\5\4L\n\4\3\4\5\4O\n\4\3\4\3\4\5\4S\n\4\3")
        buf.write("\5\3\5\3\5\5\5X\n\5\3\5\7\5[\n\5\f\5\16\5^\13\5\3\5\3")
        buf.write("\5\3\6\3\6\3\7\3\7\3\7\5\7g\n\7\3\b\3\b\5\bk\n\b\3\b\5")
        buf.write("\bn\n\b\3\b\5\bq\n\b\3\t\3\t\5\tu\n\t\3\n\3\n\3\n\3\n")
        buf.write("\3\13\3\13\3\13\3\13\7\13\177\n\13\f\13\16\13\u0082\13")
        buf.write("\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\f")
        buf.write("\u008f\n\f\3\r\3\r\3\r\5\r\u0094\n\r\3\16\3\16\3\16\3")
        buf.write("\16\5\16\u009a\n\16\3\16\3\16\3\17\3\17\3\17\3\17\3\17")
        buf.write("\5\17\u00a3\n\17\3\17\3\17\3\20\3\20\3\21\6\21\u00aa\n")
        buf.write("\21\r\21\16\21\u00ab\3\22\3\22\3\22\3\22\3\22\3\22\3\22")
        buf.write("\3\22\3\22\3\22\3\22\3\22\5\22\u00ba\n\22\3\23\3\23\3")
        buf.write("\24\3\24\3\24\3\24\7\24\u00c2\n\24\f\24\16\24\u00c5\13")
        buf.write("\24\3\24\3\24\3\25\3\25\3\25\3\25\5\25\u00cd\n\25\3\26")
        buf.write("\3\26\3\26\3\27\3\27\3\27\3\30\3\30\5\30\u00d7\n\30\3")
        buf.write("\31\3\31\3\31\3\31\5\31\u00dd\n\31\3\32\3\32\5\32\u00e1")
        buf.write("\n\32\3\32\3\32\5\32\u00e5\n\32\5\32\u00e7\n\32\3\33\3")
        buf.write("\33\3\34\3\34\3\34\3\34\3\35\3\35\3\36\3\36\3\36\3\36")
        buf.write("\7\36\u00f5\n\36\f\36\16\36\u00f8\13\36\3\36\3\36\3\37")
        buf.write("\3\37\3\37\3\37\7\37\u0100\n\37\f\37\16\37\u0103\13\37")
        buf.write("\3\37\3\37\3\37\3\37\5\37\u0109\n\37\3\37\2\2 \2\4\6\b")
        buf.write("\n\f\16\20\22\24\26\30\32\34\36 \"$&(*,.\60\62\64\668")
        buf.write(":<\2\3\3\2\6\7\2\u010e\2?\3\2\2\2\4E\3\2\2\2\6R\3\2\2")
        buf.write("\2\bT\3\2\2\2\na\3\2\2\2\ff\3\2\2\2\16h\3\2\2\2\20t\3")
        buf.write("\2\2\2\22v\3\2\2\2\24z\3\2\2\2\26\u008e\3\2\2\2\30\u0090")
        buf.write("\3\2\2\2\32\u0095\3\2\2\2\34\u009d\3\2\2\2\36\u00a6\3")
        buf.write("\2\2\2 \u00a9\3\2\2\2\"\u00b9\3\2\2\2$\u00bb\3\2\2\2&")
        buf.write("\u00bd\3\2\2\2(\u00c8\3\2\2\2*\u00ce\3\2\2\2,\u00d1\3")
        buf.write("\2\2\2.\u00d6\3\2\2\2\60\u00dc\3\2\2\2\62\u00e6\3\2\2")
        buf.write("\2\64\u00e8\3\2\2\2\66\u00ea\3\2\2\28\u00ee\3\2\2\2:\u00f0")
        buf.write("\3\2\2\2<\u0108\3\2\2\2>@\5\4\3\2?>\3\2\2\2@A\3\2\2\2")
        buf.write("A?\3\2\2\2AB\3\2\2\2B\3\3\2\2\2CF\5\6\4\2DF\5\34\17\2")
        buf.write("EC\3\2\2\2ED\3\2\2\2F\5\3\2\2\2GS\5\b\5\2HI\5\n\6\2IK")
        buf.write("\7\27\2\2JL\5&\24\2KJ\3\2\2\2KL\3\2\2\2LN\3\2\2\2MO\5")
        buf.write(" \21\2NM\3\2\2\2NO\3\2\2\2OP\3\2\2\2PQ\5\b\5\2QS\3\2\2")
        buf.write("\2RG\3\2\2\2RH\3\2\2\2S\7\3\2\2\2TU\7\3\2\2U\\\5\f\7\2")
        buf.write("VX\7\4\2\2WV\3\2\2\2WX\3\2\2\2XY\3\2\2\2Y[\5\f\7\2ZW\3")
        buf.write("\2\2\2[^\3\2\2\2\\Z\3\2\2\2\\]\3\2\2\2]_\3\2\2\2^\\\3")
        buf.write("\2\2\2_`\7\5\2\2`\t\3\2\2\2ab\t\2\2\2b\13\3\2\2\2cg\5")
        buf.write("\16\b\2dg\5\30\r\2eg\5\32\16\2fc\3\2\2\2fd\3\2\2\2fe\3")
        buf.write("\2\2\2g\r\3\2\2\2hj\5\20\t\2ik\5\24\13\2ji\3\2\2\2jk\3")
        buf.write("\2\2\2km\3\2\2\2ln\5 \21\2ml\3\2\2\2mn\3\2\2\2np\3\2\2")
        buf.write("\2oq\5\b\5\2po\3\2\2\2pq\3\2\2\2q\17\3\2\2\2ru\5\22\n")
        buf.write("\2su\7\27\2\2tr\3\2\2\2ts\3\2\2\2u\21\3\2\2\2vw\7\27\2")
        buf.write("\2wx\7\b\2\2xy\7\27\2\2y\23\3\2\2\2z{\7\t\2\2{\u0080\5")
        buf.write("\26\f\2|}\7\4\2\2}\177\5\26\f\2~|\3\2\2\2\177\u0082\3")
        buf.write("\2\2\2\u0080~\3\2\2\2\u0080\u0081\3\2\2\2\u0081\u0083")
        buf.write("\3\2\2\2\u0082\u0080\3\2\2\2\u0083\u0084\7\n\2\2\u0084")
        buf.write("\25\3\2\2\2\u0085\u0086\7\26\2\2\u0086\u0087\7\b\2\2\u0087")
        buf.write("\u008f\7\27\2\2\u0088\u0089\7\26\2\2\u0089\u008a\7\b\2")
        buf.write("\2\u008a\u008f\5:\36\2\u008b\u008c\7\27\2\2\u008c\u008d")
        buf.write("\7\b\2\2\u008d\u008f\5.\30\2\u008e\u0085\3\2\2\2\u008e")
        buf.write("\u0088\3\2\2\2\u008e\u008b\3\2\2\2\u008f\27\3\2\2\2\u0090")
        buf.write("\u0091\7\13\2\2\u0091\u0093\5\36\20\2\u0092\u0094\5 \21")
        buf.write("\2\u0093\u0092\3\2\2\2\u0093\u0094\3\2\2\2\u0094\31\3")
        buf.write("\2\2\2\u0095\u0096\7\13\2\2\u0096\u0097\7\f\2\2\u0097")
        buf.write("\u0099\5$\23\2\u0098\u009a\5 \21\2\u0099\u0098\3\2\2\2")
        buf.write("\u0099\u009a\3\2\2\2\u009a\u009b\3\2\2\2\u009b\u009c\5")
        buf.write("\b\5\2\u009c\33\3\2\2\2\u009d\u009e\7\r\2\2\u009e\u009f")
        buf.write("\5\36\20\2\u009f\u00a0\7\f\2\2\u00a0\u00a2\5$\23\2\u00a1")
        buf.write("\u00a3\5 \21\2\u00a2\u00a1\3\2\2\2\u00a2\u00a3\3\2\2\2")
        buf.write("\u00a3\u00a4\3\2\2\2\u00a4\u00a5\5\b\5\2\u00a5\35\3\2")
        buf.write("\2\2\u00a6\u00a7\7\27\2\2\u00a7\37\3\2\2\2\u00a8\u00aa")
        buf.write("\5\"\22\2\u00a9\u00a8\3\2\2\2\u00aa\u00ab\3\2\2\2\u00ab")
        buf.write("\u00a9\3\2\2\2\u00ab\u00ac\3\2\2\2\u00ac!\3\2\2\2\u00ad")
        buf.write("\u00ae\7\16\2\2\u00ae\u00af\7\27\2\2\u00af\u00b0\7\b\2")
        buf.write("\2\u00b0\u00ba\5.\30\2\u00b1\u00b2\7\16\2\2\u00b2\u00ba")
        buf.write("\7\27\2\2\u00b3\u00b4\7\16\2\2\u00b4\u00b5\7\27\2\2\u00b5")
        buf.write("\u00b6\7\t\2\2\u00b6\u00b7\5\26\f\2\u00b7\u00b8\7\n\2")
        buf.write("\2\u00b8\u00ba\3\2\2\2\u00b9\u00ad\3\2\2\2\u00b9\u00b1")
        buf.write("\3\2\2\2\u00b9\u00b3\3\2\2\2\u00ba#\3\2\2\2\u00bb\u00bc")
        buf.write("\5\64\33\2\u00bc%\3\2\2\2\u00bd\u00be\7\t\2\2\u00be\u00c3")
        buf.write("\5(\25\2\u00bf\u00c0\7\4\2\2\u00c0\u00c2\5(\25\2\u00c1")
        buf.write("\u00bf\3\2\2\2\u00c2\u00c5\3\2\2\2\u00c3\u00c1\3\2\2\2")
        buf.write("\u00c3\u00c4\3\2\2\2\u00c4\u00c6\3\2\2\2\u00c5\u00c3\3")
        buf.write("\2\2\2\u00c6\u00c7\7\n\2\2\u00c7\'\3\2\2\2\u00c8\u00c9")
        buf.write("\5*\26\2\u00c9\u00ca\7\b\2\2\u00ca\u00cc\5\62\32\2\u00cb")
        buf.write("\u00cd\5,\27\2\u00cc\u00cb\3\2\2\2\u00cc\u00cd\3\2\2\2")
        buf.write("\u00cd)\3\2\2\2\u00ce\u00cf\7\17\2\2\u00cf\u00d0\7\27")
        buf.write("\2\2\u00d0+\3\2\2\2\u00d1\u00d2\7\20\2\2\u00d2\u00d3\5")
        buf.write("\60\31\2\u00d3-\3\2\2\2\u00d4\u00d7\5\60\31\2\u00d5\u00d7")
        buf.write("\5*\26\2\u00d6\u00d4\3\2\2\2\u00d6\u00d5\3\2\2\2\u00d7")
        buf.write("/\3\2\2\2\u00d8\u00dd\7\24\2\2\u00d9\u00dd\7\30\2\2\u00da")
        buf.write("\u00dd\7\25\2\2\u00db\u00dd\5<\37\2\u00dc\u00d8\3\2\2")
        buf.write("\2\u00dc\u00d9\3\2\2\2\u00dc\u00da\3\2\2\2\u00dc\u00db")
        buf.write("\3\2\2\2\u00dd\61\3\2\2\2\u00de\u00e0\5\64\33\2\u00df")
        buf.write("\u00e1\58\35\2\u00e0\u00df\3\2\2\2\u00e0\u00e1\3\2\2\2")
        buf.write("\u00e1\u00e7\3\2\2\2\u00e2\u00e4\5\66\34\2\u00e3\u00e5")
        buf.write("\58\35\2\u00e4\u00e3\3\2\2\2\u00e4\u00e5\3\2\2\2\u00e5")
        buf.write("\u00e7\3\2\2\2\u00e6\u00de\3\2\2\2\u00e6\u00e2\3\2\2\2")
        buf.write("\u00e7\63\3\2\2\2\u00e8\u00e9\7\27\2\2\u00e9\65\3\2\2")
        buf.write("\2\u00ea\u00eb\7\21\2\2\u00eb\u00ec\5\62\32\2\u00ec\u00ed")
        buf.write("\7\22\2\2\u00ed\67\3\2\2\2\u00ee\u00ef\7\23\2\2\u00ef")
        buf.write("9\3\2\2\2\u00f0\u00f1\7\21\2\2\u00f1\u00f6\7\27\2\2\u00f2")
        buf.write("\u00f3\7\4\2\2\u00f3\u00f5\7\27\2\2\u00f4\u00f2\3\2\2")
        buf.write("\2\u00f5\u00f8\3\2\2\2\u00f6\u00f4\3\2\2\2\u00f6\u00f7")
        buf.write("\3\2\2\2\u00f7\u00f9\3\2\2\2\u00f8\u00f6\3\2\2\2\u00f9")
        buf.write("\u00fa\7\22\2\2\u00fa;\3\2\2\2\u00fb\u00fc\7\21\2\2\u00fc")
        buf.write("\u0101\5\60\31\2\u00fd\u00fe\7\4\2\2\u00fe\u0100\5\60")
        buf.write("\31\2\u00ff\u00fd\3\2\2\2\u0100\u0103\3\2\2\2\u0101\u00ff")
        buf.write("\3\2\2\2\u0101\u0102\3\2\2\2\u0102\u0104\3\2\2\2\u0103")
        buf.write("\u0101\3\2\2\2\u0104\u0105\7\22\2\2\u0105\u0109\3\2\2")
        buf.write("\2\u0106\u0107\7\21\2\2\u0107\u0109\7\22\2\2\u0108\u00fb")
        buf.write("\3\2\2\2\u0108\u0106\3\2\2\2\u0109=\3\2\2\2\37AEKNRW\\")
        buf.write("fjmpt\u0080\u008e\u0093\u0099\u00a2\u00ab\u00b9\u00c3")
        buf.write("\u00cc\u00d6\u00dc\u00e0\u00e4\u00e6\u00f6\u0101\u0108")
        return buf.getvalue()


class GraphQLParser ( Parser ):

    grammarFileName = "GraphQL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "','", "'}'", "'query'", "'mutation'", 
                     "':'", "'('", "')'", "'...'", "'on'", "'fragment'", 
                     "'@'", "'$'", "'='", "'['", "']'", "'!'", "<INVALID>", 
                     "<INVALID>", "'sort'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "STRING", "BOOLEAN", "SORT", 
                      "NAME", "NUMBER", "WS" ]

    RULE_document = 0
    RULE_definition = 1
    RULE_operationDefinition = 2
    RULE_selectionSet = 3
    RULE_operationType = 4
    RULE_selection = 5
    RULE_field = 6
    RULE_fieldName = 7
    RULE_alias = 8
    RULE_arguments = 9
    RULE_argument = 10
    RULE_fragmentSpread = 11
    RULE_inlineFragment = 12
    RULE_fragmentDefinition = 13
    RULE_fragmentName = 14
    RULE_directives = 15
    RULE_directive = 16
    RULE_typeCondition = 17
    RULE_variableDefinitions = 18
    RULE_variableDefinition = 19
    RULE_variable = 20
    RULE_defaultValue = 21
    RULE_valueOrVariable = 22
    RULE_value = 23
    RULE_ttype = 24
    RULE_typeName = 25
    RULE_listType = 26
    RULE_nonNullType = 27
    RULE_nameArray = 28
    RULE_array = 29

    ruleNames =  [ "document", "definition", "operationDefinition", "selectionSet", 
                   "operationType", "selection", "field", "fieldName", "alias", 
                   "arguments", "argument", "fragmentSpread", "inlineFragment", 
                   "fragmentDefinition", "fragmentName", "directives", "directive", 
                   "typeCondition", "variableDefinitions", "variableDefinition", 
                   "variable", "defaultValue", "valueOrVariable", "value", 
                   "ttype", "typeName", "listType", "nonNullType", "nameArray", 
                   "array" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    STRING=18
    BOOLEAN=19
    SORT=20
    NAME=21
    NUMBER=22
    WS=23

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class DocumentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def definition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GraphQLParser.DefinitionContext)
            else:
                return self.getTypedRuleContext(GraphQLParser.DefinitionContext,i)


        def getRuleIndex(self):
            return GraphQLParser.RULE_document

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDocument" ):
                return visitor.visitDocument(self)
            else:
                return visitor.visitChildren(self)




    def document(self):

        localctx = GraphQLParser.DocumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_document)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 60
                self.definition()
                self.state = 63 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GraphQLParser.T__0) | (1 << GraphQLParser.T__3) | (1 << GraphQLParser.T__4) | (1 << GraphQLParser.T__10))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefinitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def operationDefinition(self):
            return self.getTypedRuleContext(GraphQLParser.OperationDefinitionContext,0)


        def fragmentDefinition(self):
            return self.getTypedRuleContext(GraphQLParser.FragmentDefinitionContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_definition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefinition" ):
                return visitor.visitDefinition(self)
            else:
                return visitor.visitChildren(self)




    def definition(self):

        localctx = GraphQLParser.DefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_definition)
        try:
            self.state = 67
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GraphQLParser.T__0, GraphQLParser.T__3, GraphQLParser.T__4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 65
                self.operationDefinition()
                pass
            elif token in [GraphQLParser.T__10]:
                self.enterOuterAlt(localctx, 2)
                self.state = 66
                self.fragmentDefinition()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperationDefinitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def selectionSet(self):
            return self.getTypedRuleContext(GraphQLParser.SelectionSetContext,0)


        def operationType(self):
            return self.getTypedRuleContext(GraphQLParser.OperationTypeContext,0)


        def NAME(self):
            return self.getToken(GraphQLParser.NAME, 0)

        def variableDefinitions(self):
            return self.getTypedRuleContext(GraphQLParser.VariableDefinitionsContext,0)


        def directives(self):
            return self.getTypedRuleContext(GraphQLParser.DirectivesContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_operationDefinition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOperationDefinition" ):
                return visitor.visitOperationDefinition(self)
            else:
                return visitor.visitChildren(self)




    def operationDefinition(self):

        localctx = GraphQLParser.OperationDefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_operationDefinition)
        self._la = 0 # Token type
        try:
            self.state = 80
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GraphQLParser.T__0]:
                self.enterOuterAlt(localctx, 1)
                self.state = 69
                self.selectionSet()
                pass
            elif token in [GraphQLParser.T__3, GraphQLParser.T__4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 70
                self.operationType()
                self.state = 71
                self.match(GraphQLParser.NAME)
                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==GraphQLParser.T__6:
                    self.state = 72
                    self.variableDefinitions()


                self.state = 76
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==GraphQLParser.T__11:
                    self.state = 75
                    self.directives()


                self.state = 78
                self.selectionSet()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectionSetContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def selection(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GraphQLParser.SelectionContext)
            else:
                return self.getTypedRuleContext(GraphQLParser.SelectionContext,i)


        def getRuleIndex(self):
            return GraphQLParser.RULE_selectionSet

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectionSet" ):
                return visitor.visitSelectionSet(self)
            else:
                return visitor.visitChildren(self)




    def selectionSet(self):

        localctx = GraphQLParser.SelectionSetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_selectionSet)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(GraphQLParser.T__0)
            self.state = 83
            self.selection()
            self.state = 90
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GraphQLParser.T__1) | (1 << GraphQLParser.T__8) | (1 << GraphQLParser.NAME))) != 0):
                self.state = 85
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==GraphQLParser.T__1:
                    self.state = 84
                    self.match(GraphQLParser.T__1)


                self.state = 87
                self.selection()
                self.state = 92
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 93
            self.match(GraphQLParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperationTypeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GraphQLParser.RULE_operationType

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOperationType" ):
                return visitor.visitOperationType(self)
            else:
                return visitor.visitChildren(self)




    def operationType(self):

        localctx = GraphQLParser.OperationTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_operationType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            _la = self._input.LA(1)
            if not(_la==GraphQLParser.T__3 or _la==GraphQLParser.T__4):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field(self):
            return self.getTypedRuleContext(GraphQLParser.FieldContext,0)


        def fragmentSpread(self):
            return self.getTypedRuleContext(GraphQLParser.FragmentSpreadContext,0)


        def inlineFragment(self):
            return self.getTypedRuleContext(GraphQLParser.InlineFragmentContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_selection

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelection" ):
                return visitor.visitSelection(self)
            else:
                return visitor.visitChildren(self)




    def selection(self):

        localctx = GraphQLParser.SelectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_selection)
        try:
            self.state = 100
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 97
                self.field()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 98
                self.fragmentSpread()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 99
                self.inlineFragment()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FieldContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fieldName(self):
            return self.getTypedRuleContext(GraphQLParser.FieldNameContext,0)


        def arguments(self):
            return self.getTypedRuleContext(GraphQLParser.ArgumentsContext,0)


        def directives(self):
            return self.getTypedRuleContext(GraphQLParser.DirectivesContext,0)


        def selectionSet(self):
            return self.getTypedRuleContext(GraphQLParser.SelectionSetContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_field

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitField" ):
                return visitor.visitField(self)
            else:
                return visitor.visitChildren(self)




    def field(self):

        localctx = GraphQLParser.FieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_field)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.fieldName()
            self.state = 104
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==GraphQLParser.T__6:
                self.state = 103
                self.arguments()


            self.state = 107
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==GraphQLParser.T__11:
                self.state = 106
                self.directives()


            self.state = 110
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==GraphQLParser.T__0:
                self.state = 109
                self.selectionSet()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FieldNameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def alias(self):
            return self.getTypedRuleContext(GraphQLParser.AliasContext,0)


        def NAME(self):
            return self.getToken(GraphQLParser.NAME, 0)

        def getRuleIndex(self):
            return GraphQLParser.RULE_fieldName

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFieldName" ):
                return visitor.visitFieldName(self)
            else:
                return visitor.visitChildren(self)




    def fieldName(self):

        localctx = GraphQLParser.FieldNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_fieldName)
        try:
            self.state = 114
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 112
                self.alias()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 113
                self.match(GraphQLParser.NAME)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AliasContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(GraphQLParser.NAME)
            else:
                return self.getToken(GraphQLParser.NAME, i)

        def getRuleIndex(self):
            return GraphQLParser.RULE_alias

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAlias" ):
                return visitor.visitAlias(self)
            else:
                return visitor.visitChildren(self)




    def alias(self):

        localctx = GraphQLParser.AliasContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_alias)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            self.match(GraphQLParser.NAME)
            self.state = 117
            self.match(GraphQLParser.T__5)
            self.state = 118
            self.match(GraphQLParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GraphQLParser.ArgumentContext)
            else:
                return self.getTypedRuleContext(GraphQLParser.ArgumentContext,i)


        def getRuleIndex(self):
            return GraphQLParser.RULE_arguments

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArguments" ):
                return visitor.visitArguments(self)
            else:
                return visitor.visitChildren(self)




    def arguments(self):

        localctx = GraphQLParser.ArgumentsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_arguments)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 120
            self.match(GraphQLParser.T__6)
            self.state = 121
            self.argument()
            self.state = 126
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==GraphQLParser.T__1:
                self.state = 122
                self.match(GraphQLParser.T__1)
                self.state = 123
                self.argument()
                self.state = 128
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 129
            self.match(GraphQLParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SORT(self):
            return self.getToken(GraphQLParser.SORT, 0)

        def NAME(self):
            return self.getToken(GraphQLParser.NAME, 0)

        def nameArray(self):
            return self.getTypedRuleContext(GraphQLParser.NameArrayContext,0)


        def valueOrVariable(self):
            return self.getTypedRuleContext(GraphQLParser.ValueOrVariableContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_argument

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgument" ):
                return visitor.visitArgument(self)
            else:
                return visitor.visitChildren(self)




    def argument(self):

        localctx = GraphQLParser.ArgumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_argument)
        try:
            self.state = 140
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 131
                self.match(GraphQLParser.SORT)
                self.state = 132
                self.match(GraphQLParser.T__5)
                self.state = 133
                self.match(GraphQLParser.NAME)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 134
                self.match(GraphQLParser.SORT)
                self.state = 135
                self.match(GraphQLParser.T__5)
                self.state = 136
                self.nameArray()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 137
                self.match(GraphQLParser.NAME)
                self.state = 138
                self.match(GraphQLParser.T__5)
                self.state = 139
                self.valueOrVariable()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FragmentSpreadContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fragmentName(self):
            return self.getTypedRuleContext(GraphQLParser.FragmentNameContext,0)


        def directives(self):
            return self.getTypedRuleContext(GraphQLParser.DirectivesContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_fragmentSpread

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFragmentSpread" ):
                return visitor.visitFragmentSpread(self)
            else:
                return visitor.visitChildren(self)




    def fragmentSpread(self):

        localctx = GraphQLParser.FragmentSpreadContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_fragmentSpread)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 142
            self.match(GraphQLParser.T__8)
            self.state = 143
            self.fragmentName()
            self.state = 145
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==GraphQLParser.T__11:
                self.state = 144
                self.directives()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InlineFragmentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeCondition(self):
            return self.getTypedRuleContext(GraphQLParser.TypeConditionContext,0)


        def selectionSet(self):
            return self.getTypedRuleContext(GraphQLParser.SelectionSetContext,0)


        def directives(self):
            return self.getTypedRuleContext(GraphQLParser.DirectivesContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_inlineFragment

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInlineFragment" ):
                return visitor.visitInlineFragment(self)
            else:
                return visitor.visitChildren(self)




    def inlineFragment(self):

        localctx = GraphQLParser.InlineFragmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_inlineFragment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            self.match(GraphQLParser.T__8)
            self.state = 148
            self.match(GraphQLParser.T__9)
            self.state = 149
            self.typeCondition()
            self.state = 151
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==GraphQLParser.T__11:
                self.state = 150
                self.directives()


            self.state = 153
            self.selectionSet()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FragmentDefinitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fragmentName(self):
            return self.getTypedRuleContext(GraphQLParser.FragmentNameContext,0)


        def typeCondition(self):
            return self.getTypedRuleContext(GraphQLParser.TypeConditionContext,0)


        def selectionSet(self):
            return self.getTypedRuleContext(GraphQLParser.SelectionSetContext,0)


        def directives(self):
            return self.getTypedRuleContext(GraphQLParser.DirectivesContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_fragmentDefinition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFragmentDefinition" ):
                return visitor.visitFragmentDefinition(self)
            else:
                return visitor.visitChildren(self)




    def fragmentDefinition(self):

        localctx = GraphQLParser.FragmentDefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_fragmentDefinition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 155
            self.match(GraphQLParser.T__10)
            self.state = 156
            self.fragmentName()
            self.state = 157
            self.match(GraphQLParser.T__9)
            self.state = 158
            self.typeCondition()
            self.state = 160
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==GraphQLParser.T__11:
                self.state = 159
                self.directives()


            self.state = 162
            self.selectionSet()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FragmentNameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(GraphQLParser.NAME, 0)

        def getRuleIndex(self):
            return GraphQLParser.RULE_fragmentName

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFragmentName" ):
                return visitor.visitFragmentName(self)
            else:
                return visitor.visitChildren(self)




    def fragmentName(self):

        localctx = GraphQLParser.FragmentNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_fragmentName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 164
            self.match(GraphQLParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirectivesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def directive(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GraphQLParser.DirectiveContext)
            else:
                return self.getTypedRuleContext(GraphQLParser.DirectiveContext,i)


        def getRuleIndex(self):
            return GraphQLParser.RULE_directives

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirectives" ):
                return visitor.visitDirectives(self)
            else:
                return visitor.visitChildren(self)




    def directives(self):

        localctx = GraphQLParser.DirectivesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_directives)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 167 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 166
                self.directive()
                self.state = 169 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==GraphQLParser.T__11):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirectiveContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(GraphQLParser.NAME, 0)

        def valueOrVariable(self):
            return self.getTypedRuleContext(GraphQLParser.ValueOrVariableContext,0)


        def argument(self):
            return self.getTypedRuleContext(GraphQLParser.ArgumentContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_directive

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirective" ):
                return visitor.visitDirective(self)
            else:
                return visitor.visitChildren(self)




    def directive(self):

        localctx = GraphQLParser.DirectiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_directive)
        try:
            self.state = 183
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 171
                self.match(GraphQLParser.T__11)
                self.state = 172
                self.match(GraphQLParser.NAME)
                self.state = 173
                self.match(GraphQLParser.T__5)
                self.state = 174
                self.valueOrVariable()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 175
                self.match(GraphQLParser.T__11)
                self.state = 176
                self.match(GraphQLParser.NAME)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 177
                self.match(GraphQLParser.T__11)
                self.state = 178
                self.match(GraphQLParser.NAME)
                self.state = 179
                self.match(GraphQLParser.T__6)
                self.state = 180
                self.argument()
                self.state = 181
                self.match(GraphQLParser.T__7)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeConditionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeName(self):
            return self.getTypedRuleContext(GraphQLParser.TypeNameContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_typeCondition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeCondition" ):
                return visitor.visitTypeCondition(self)
            else:
                return visitor.visitChildren(self)




    def typeCondition(self):

        localctx = GraphQLParser.TypeConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_typeCondition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 185
            self.typeName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableDefinitionsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variableDefinition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GraphQLParser.VariableDefinitionContext)
            else:
                return self.getTypedRuleContext(GraphQLParser.VariableDefinitionContext,i)


        def getRuleIndex(self):
            return GraphQLParser.RULE_variableDefinitions

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableDefinitions" ):
                return visitor.visitVariableDefinitions(self)
            else:
                return visitor.visitChildren(self)




    def variableDefinitions(self):

        localctx = GraphQLParser.VariableDefinitionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_variableDefinitions)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 187
            self.match(GraphQLParser.T__6)
            self.state = 188
            self.variableDefinition()
            self.state = 193
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==GraphQLParser.T__1:
                self.state = 189
                self.match(GraphQLParser.T__1)
                self.state = 190
                self.variableDefinition()
                self.state = 195
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 196
            self.match(GraphQLParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableDefinitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variable(self):
            return self.getTypedRuleContext(GraphQLParser.VariableContext,0)


        def ttype(self):
            return self.getTypedRuleContext(GraphQLParser.TtypeContext,0)


        def defaultValue(self):
            return self.getTypedRuleContext(GraphQLParser.DefaultValueContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_variableDefinition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableDefinition" ):
                return visitor.visitVariableDefinition(self)
            else:
                return visitor.visitChildren(self)




    def variableDefinition(self):

        localctx = GraphQLParser.VariableDefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_variableDefinition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 198
            self.variable()
            self.state = 199
            self.match(GraphQLParser.T__5)
            self.state = 200
            self.ttype()
            self.state = 202
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==GraphQLParser.T__13:
                self.state = 201
                self.defaultValue()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(GraphQLParser.NAME, 0)

        def getRuleIndex(self):
            return GraphQLParser.RULE_variable

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariable" ):
                return visitor.visitVariable(self)
            else:
                return visitor.visitChildren(self)




    def variable(self):

        localctx = GraphQLParser.VariableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_variable)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 204
            self.match(GraphQLParser.T__12)
            self.state = 205
            self.match(GraphQLParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefaultValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self):
            return self.getTypedRuleContext(GraphQLParser.ValueContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_defaultValue

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefaultValue" ):
                return visitor.visitDefaultValue(self)
            else:
                return visitor.visitChildren(self)




    def defaultValue(self):

        localctx = GraphQLParser.DefaultValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_defaultValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 207
            self.match(GraphQLParser.T__13)
            self.state = 208
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueOrVariableContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self):
            return self.getTypedRuleContext(GraphQLParser.ValueContext,0)


        def variable(self):
            return self.getTypedRuleContext(GraphQLParser.VariableContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_valueOrVariable

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValueOrVariable" ):
                return visitor.visitValueOrVariable(self)
            else:
                return visitor.visitChildren(self)




    def valueOrVariable(self):

        localctx = GraphQLParser.ValueOrVariableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_valueOrVariable)
        try:
            self.state = 212
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GraphQLParser.T__14, GraphQLParser.STRING, GraphQLParser.BOOLEAN, GraphQLParser.NUMBER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 210
                self.value()
                pass
            elif token in [GraphQLParser.T__12]:
                self.enterOuterAlt(localctx, 2)
                self.state = 211
                self.variable()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GraphQLParser.RULE_value

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class StringValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GraphQLParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(GraphQLParser.STRING, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringValue" ):
                return visitor.visitStringValue(self)
            else:
                return visitor.visitChildren(self)


    class BooleanValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GraphQLParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BOOLEAN(self):
            return self.getToken(GraphQLParser.BOOLEAN, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBooleanValue" ):
                return visitor.visitBooleanValue(self)
            else:
                return visitor.visitChildren(self)


    class NumberValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GraphQLParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(GraphQLParser.NUMBER, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumberValue" ):
                return visitor.visitNumberValue(self)
            else:
                return visitor.visitChildren(self)


    class ArrayValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GraphQLParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def array(self):
            return self.getTypedRuleContext(GraphQLParser.ArrayContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayValue" ):
                return visitor.visitArrayValue(self)
            else:
                return visitor.visitChildren(self)



    def value(self):

        localctx = GraphQLParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_value)
        try:
            self.state = 218
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GraphQLParser.STRING]:
                localctx = GraphQLParser.StringValueContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 214
                self.match(GraphQLParser.STRING)
                pass
            elif token in [GraphQLParser.NUMBER]:
                localctx = GraphQLParser.NumberValueContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 215
                self.match(GraphQLParser.NUMBER)
                pass
            elif token in [GraphQLParser.BOOLEAN]:
                localctx = GraphQLParser.BooleanValueContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 216
                self.match(GraphQLParser.BOOLEAN)
                pass
            elif token in [GraphQLParser.T__14]:
                localctx = GraphQLParser.ArrayValueContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 217
                self.array()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TtypeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeName(self):
            return self.getTypedRuleContext(GraphQLParser.TypeNameContext,0)


        def nonNullType(self):
            return self.getTypedRuleContext(GraphQLParser.NonNullTypeContext,0)


        def listType(self):
            return self.getTypedRuleContext(GraphQLParser.ListTypeContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_ttype

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTtype" ):
                return visitor.visitTtype(self)
            else:
                return visitor.visitChildren(self)




    def ttype(self):

        localctx = GraphQLParser.TtypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_ttype)
        self._la = 0 # Token type
        try:
            self.state = 228
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GraphQLParser.NAME]:
                self.enterOuterAlt(localctx, 1)
                self.state = 220
                self.typeName()
                self.state = 222
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==GraphQLParser.T__16:
                    self.state = 221
                    self.nonNullType()


                pass
            elif token in [GraphQLParser.T__14]:
                self.enterOuterAlt(localctx, 2)
                self.state = 224
                self.listType()
                self.state = 226
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==GraphQLParser.T__16:
                    self.state = 225
                    self.nonNullType()


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeNameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(GraphQLParser.NAME, 0)

        def getRuleIndex(self):
            return GraphQLParser.RULE_typeName

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeName" ):
                return visitor.visitTypeName(self)
            else:
                return visitor.visitChildren(self)




    def typeName(self):

        localctx = GraphQLParser.TypeNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_typeName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 230
            self.match(GraphQLParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ListTypeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ttype(self):
            return self.getTypedRuleContext(GraphQLParser.TtypeContext,0)


        def getRuleIndex(self):
            return GraphQLParser.RULE_listType

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitListType" ):
                return visitor.visitListType(self)
            else:
                return visitor.visitChildren(self)




    def listType(self):

        localctx = GraphQLParser.ListTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_listType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 232
            self.match(GraphQLParser.T__14)
            self.state = 233
            self.ttype()
            self.state = 234
            self.match(GraphQLParser.T__15)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NonNullTypeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GraphQLParser.RULE_nonNullType

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNonNullType" ):
                return visitor.visitNonNullType(self)
            else:
                return visitor.visitChildren(self)




    def nonNullType(self):

        localctx = GraphQLParser.NonNullTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_nonNullType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 236
            self.match(GraphQLParser.T__16)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NameArrayContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(GraphQLParser.NAME)
            else:
                return self.getToken(GraphQLParser.NAME, i)

        def getRuleIndex(self):
            return GraphQLParser.RULE_nameArray

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNameArray" ):
                return visitor.visitNameArray(self)
            else:
                return visitor.visitChildren(self)




    def nameArray(self):

        localctx = GraphQLParser.NameArrayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_nameArray)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 238
            self.match(GraphQLParser.T__14)
            self.state = 239
            self.match(GraphQLParser.NAME)
            self.state = 244
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==GraphQLParser.T__1:
                self.state = 240
                self.match(GraphQLParser.T__1)
                self.state = 241
                self.match(GraphQLParser.NAME)
                self.state = 246
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 247
            self.match(GraphQLParser.T__15)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GraphQLParser.ValueContext)
            else:
                return self.getTypedRuleContext(GraphQLParser.ValueContext,i)


        def getRuleIndex(self):
            return GraphQLParser.RULE_array

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArray" ):
                return visitor.visitArray(self)
            else:
                return visitor.visitChildren(self)




    def array(self):

        localctx = GraphQLParser.ArrayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_array)
        self._la = 0 # Token type
        try:
            self.state = 262
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 249
                self.match(GraphQLParser.T__14)
                self.state = 250
                self.value()
                self.state = 255
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==GraphQLParser.T__1:
                    self.state = 251
                    self.match(GraphQLParser.T__1)
                    self.state = 252
                    self.value()
                    self.state = 257
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 258
                self.match(GraphQLParser.T__15)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 260
                self.match(GraphQLParser.T__14)
                self.state = 261
                self.match(GraphQLParser.T__15)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





