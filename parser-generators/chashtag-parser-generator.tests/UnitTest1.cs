namespace chashtag_parser_generator.tests;

using Xunit;
using Antlr4.Runtime;
using chashtag_parser_generator;

public class ParserTests
{
    [Fact]
    public void ParseSimpleInput_ProducesExpectedTree()
    {
        string input = "3 + 4";
        ICharStream stream = new AntlrInputStream(input);
        testLexer lexer = new(stream);
        CommonTokenStream tokens = new(lexer);
        testParser parser = new(tokens);

        var tree = parser.r(); // Replace "expr" with your start rule
        string actualTree = tree.ToStringTree(parser);

        Assert.NotNull(tree); // Or compare to expected output
    }
}
