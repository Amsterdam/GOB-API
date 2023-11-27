# Generated from gobapi/graphql_streaming/graphql2sql/grammar/GraphQL.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\31")
        buf.write("\u00d0\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\3\2")
        buf.write("\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3")
        buf.write("\6\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n")
        buf.write("\3\n\3\n\3\n\3\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3")
        buf.write("\f\3\f\3\f\3\r\3\r\3\16\3\16\3\17\3\17\3\20\3\20\3\21")
        buf.write("\3\21\3\22\3\22\3\23\3\23\3\23\7\23v\n\23\f\23\16\23y")
        buf.write("\13\23\3\23\3\23\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3")
        buf.write("\24\3\24\5\24\u0086\n\24\3\25\3\25\3\25\3\25\3\25\3\26")
        buf.write("\3\26\7\26\u008f\n\26\f\26\16\26\u0092\13\26\3\27\3\27")
        buf.write("\3\27\5\27\u0097\n\27\3\30\3\30\3\30\3\30\3\30\3\30\3")
        buf.write("\31\3\31\3\32\5\32\u00a2\n\32\3\32\3\32\3\32\6\32\u00a7")
        buf.write("\n\32\r\32\16\32\u00a8\3\32\5\32\u00ac\n\32\3\32\5\32")
        buf.write("\u00af\n\32\3\32\3\32\3\32\3\32\5\32\u00b5\n\32\3\32\5")
        buf.write("\32\u00b8\n\32\3\33\3\33\3\33\7\33\u00bd\n\33\f\33\16")
        buf.write("\33\u00c0\13\33\5\33\u00c2\n\33\3\34\3\34\5\34\u00c6\n")
        buf.write("\34\3\34\3\34\3\35\6\35\u00cb\n\35\r\35\16\35\u00cc\3")
        buf.write("\35\3\35\2\2\36\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23")
        buf.write("\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25")
        buf.write(")\26+\27-\2/\2\61\2\63\30\65\2\67\29\31\3\2\f\4\2$$^^")
        buf.write("\5\2C\\aac|\6\2\62;C\\aac|\n\2$$\61\61^^ddhhppttvv\5\2")
        buf.write("\62;CHch\3\2\62;\3\2\63;\4\2GGgg\4\2--//\5\2\13\f\17\17")
        buf.write("\"\"\2\u00da\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3")
        buf.write("\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2")
        buf.write("\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2")
        buf.write("\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2")
        buf.write("#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2")
        buf.write("\2\63\3\2\2\2\29\3\2\2\2\3;\3\2\2\2\5=\3\2\2\2\7?\3\2")
        buf.write("\2\2\tA\3\2\2\2\13G\3\2\2\2\rP\3\2\2\2\17R\3\2\2\2\21")
        buf.write("T\3\2\2\2\23V\3\2\2\2\25Z\3\2\2\2\27]\3\2\2\2\31f\3\2")
        buf.write("\2\2\33h\3\2\2\2\35j\3\2\2\2\37l\3\2\2\2!n\3\2\2\2#p\3")
        buf.write("\2\2\2%r\3\2\2\2\'\u0085\3\2\2\2)\u0087\3\2\2\2+\u008c")
        buf.write("\3\2\2\2-\u0093\3\2\2\2/\u0098\3\2\2\2\61\u009e\3\2\2")
        buf.write("\2\63\u00b7\3\2\2\2\65\u00c1\3\2\2\2\67\u00c3\3\2\2\2")
        buf.write("9\u00ca\3\2\2\2;<\7}\2\2<\4\3\2\2\2=>\7.\2\2>\6\3\2\2")
        buf.write("\2?@\7\177\2\2@\b\3\2\2\2AB\7s\2\2BC\7w\2\2CD\7g\2\2D")
        buf.write("E\7t\2\2EF\7{\2\2F\n\3\2\2\2GH\7o\2\2HI\7w\2\2IJ\7v\2")
        buf.write("\2JK\7c\2\2KL\7v\2\2LM\7k\2\2MN\7q\2\2NO\7p\2\2O\f\3\2")
        buf.write("\2\2PQ\7<\2\2Q\16\3\2\2\2RS\7*\2\2S\20\3\2\2\2TU\7+\2")
        buf.write("\2U\22\3\2\2\2VW\7\60\2\2WX\7\60\2\2XY\7\60\2\2Y\24\3")
        buf.write("\2\2\2Z[\7q\2\2[\\\7p\2\2\\\26\3\2\2\2]^\7h\2\2^_\7t\2")
        buf.write("\2_`\7c\2\2`a\7i\2\2ab\7o\2\2bc\7g\2\2cd\7p\2\2de\7v\2")
        buf.write("\2e\30\3\2\2\2fg\7B\2\2g\32\3\2\2\2hi\7&\2\2i\34\3\2\2")
        buf.write("\2jk\7?\2\2k\36\3\2\2\2lm\7]\2\2m \3\2\2\2no\7_\2\2o\"")
        buf.write("\3\2\2\2pq\7#\2\2q$\3\2\2\2rw\7$\2\2sv\5-\27\2tv\n\2\2")
        buf.write("\2us\3\2\2\2ut\3\2\2\2vy\3\2\2\2wu\3\2\2\2wx\3\2\2\2x")
        buf.write("z\3\2\2\2yw\3\2\2\2z{\7$\2\2{&\3\2\2\2|}\7v\2\2}~\7t\2")
        buf.write("\2~\177\7w\2\2\177\u0086\7g\2\2\u0080\u0081\7h\2\2\u0081")
        buf.write("\u0082\7c\2\2\u0082\u0083\7n\2\2\u0083\u0084\7u\2\2\u0084")
        buf.write("\u0086\7g\2\2\u0085|\3\2\2\2\u0085\u0080\3\2\2\2\u0086")
        buf.write("(\3\2\2\2\u0087\u0088\7u\2\2\u0088\u0089\7q\2\2\u0089")
        buf.write("\u008a\7t\2\2\u008a\u008b\7v\2\2\u008b*\3\2\2\2\u008c")
        buf.write("\u0090\t\3\2\2\u008d\u008f\t\4\2\2\u008e\u008d\3\2\2\2")
        buf.write("\u008f\u0092\3\2\2\2\u0090\u008e\3\2\2\2\u0090\u0091\3")
        buf.write("\2\2\2\u0091,\3\2\2\2\u0092\u0090\3\2\2\2\u0093\u0096")
        buf.write("\7^\2\2\u0094\u0097\t\5\2\2\u0095\u0097\5/\30\2\u0096")
        buf.write("\u0094\3\2\2\2\u0096\u0095\3\2\2\2\u0097.\3\2\2\2\u0098")
        buf.write("\u0099\7w\2\2\u0099\u009a\5\61\31\2\u009a\u009b\5\61\31")
        buf.write("\2\u009b\u009c\5\61\31\2\u009c\u009d\5\61\31\2\u009d\60")
        buf.write("\3\2\2\2\u009e\u009f\t\6\2\2\u009f\62\3\2\2\2\u00a0\u00a2")
        buf.write("\7/\2\2\u00a1\u00a0\3\2\2\2\u00a1\u00a2\3\2\2\2\u00a2")
        buf.write("\u00a3\3\2\2\2\u00a3\u00a4\5\65\33\2\u00a4\u00a6\7\60")
        buf.write("\2\2\u00a5\u00a7\t\7\2\2\u00a6\u00a5\3\2\2\2\u00a7\u00a8")
        buf.write("\3\2\2\2\u00a8\u00a6\3\2\2\2\u00a8\u00a9\3\2\2\2\u00a9")
        buf.write("\u00ab\3\2\2\2\u00aa\u00ac\5\67\34\2\u00ab\u00aa\3\2\2")
        buf.write("\2\u00ab\u00ac\3\2\2\2\u00ac\u00b8\3\2\2\2\u00ad\u00af")
        buf.write("\7/\2\2\u00ae\u00ad\3\2\2\2\u00ae\u00af\3\2\2\2\u00af")
        buf.write("\u00b0\3\2\2\2\u00b0\u00b1\5\65\33\2\u00b1\u00b2\5\67")
        buf.write("\34\2\u00b2\u00b8\3\2\2\2\u00b3\u00b5\7/\2\2\u00b4\u00b3")
        buf.write("\3\2\2\2\u00b4\u00b5\3\2\2\2\u00b5\u00b6\3\2\2\2\u00b6")
        buf.write("\u00b8\5\65\33\2\u00b7\u00a1\3\2\2\2\u00b7\u00ae\3\2\2")
        buf.write("\2\u00b7\u00b4\3\2\2\2\u00b8\64\3\2\2\2\u00b9\u00c2\7")
        buf.write("\62\2\2\u00ba\u00be\t\b\2\2\u00bb\u00bd\t\7\2\2\u00bc")
        buf.write("\u00bb\3\2\2\2\u00bd\u00c0\3\2\2\2\u00be\u00bc\3\2\2\2")
        buf.write("\u00be\u00bf\3\2\2\2\u00bf\u00c2\3\2\2\2\u00c0\u00be\3")
        buf.write("\2\2\2\u00c1\u00b9\3\2\2\2\u00c1\u00ba\3\2\2\2\u00c2\66")
        buf.write("\3\2\2\2\u00c3\u00c5\t\t\2\2\u00c4\u00c6\t\n\2\2\u00c5")
        buf.write("\u00c4\3\2\2\2\u00c5\u00c6\3\2\2\2\u00c6\u00c7\3\2\2\2")
        buf.write("\u00c7\u00c8\5\65\33\2\u00c88\3\2\2\2\u00c9\u00cb\t\13")
        buf.write("\2\2\u00ca\u00c9\3\2\2\2\u00cb\u00cc\3\2\2\2\u00cc\u00ca")
        buf.write("\3\2\2\2\u00cc\u00cd\3\2\2\2\u00cd\u00ce\3\2\2\2\u00ce")
        buf.write("\u00cf\b\35\2\2\u00cf:\3\2\2\2\22\2uw\u0085\u0090\u0096")
        buf.write("\u00a1\u00a8\u00ab\u00ae\u00b4\u00b7\u00be\u00c1\u00c5")
        buf.write("\u00cc\3\b\2\2")
        return buf.getvalue()


class GraphQLLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    T__14 = 15
    T__15 = 16
    T__16 = 17
    STRING = 18
    BOOLEAN = 19
    SORT = 20
    NAME = 21
    NUMBER = 22
    WS = 23

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'{'", "','", "'}'", "'query'", "'mutation'", "':'", "'('", 
            "')'", "'...'", "'on'", "'fragment'", "'@'", "'$'", "'='", "'['", 
            "']'", "'!'", "'sort'" ]

    symbolicNames = [ "<INVALID>",
            "STRING", "BOOLEAN", "SORT", "NAME", "NUMBER", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "STRING", "BOOLEAN", "SORT", 
                  "NAME", "ESC", "UNICODE", "HEX", "NUMBER", "INT", "EXP", 
                  "WS" ]

    grammarFileName = "GraphQL.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


