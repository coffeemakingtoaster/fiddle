grammar test;

// Parser rules
r : 'hello' ID ;         // Match the keyword 'hello' followed by an identifier

// Lexer rules
ID : [a-zA-Z]+ ;         // Match one or more letters
WS : [ \t\r\n]+ -> skip ; // Skip whitespace
