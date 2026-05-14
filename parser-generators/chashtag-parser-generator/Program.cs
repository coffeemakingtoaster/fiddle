using Antlr4.Runtime;
using Antlr4.Runtime.Tree;

class Program
{
    static void Main()
    {
        string input = "hello world";
        ICharStream stream = new AntlrInputStream(input);
        testLexer lexer = new(stream);
        CommonTokenStream tokens = new(lexer);
        testParser parser = new(tokens);

        IParseTree tree = parser.r();
        Console.WriteLine(tree.ToStringTree(parser));
    }
}
