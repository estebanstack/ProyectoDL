grammar DLang;

program
    : statement* EOF
    ;

statement
    : simpleStatement
    | compoundStatement
    ;

simpleStatement
    : assignment
    | printStatement
    | returnStatement
    | funcCall
    ;

compoundStatement
    : ifStatement
    | whileStatement
    | funcDef
    ;

// Sentencias basicas 

assignment
    : ID '=' expr                #AssignStmt
    ;

printStatement
    : 'print' '(' expr ')'       #PrintStmt
    ;

returnStatement
    : 'return' expr?             #ReturnStmt
    ;

// Control de flujo

ifStatement
    : 'if' '(' expr ')' block ('else' block)?   #IfStmt
    ;

whileStatement
    : 'while' '(' expr ')' block               #WhileStmt
    ;

block
    : '{' statement* '}'                       #BlockStmt
    ;

// Funciones

funcDef
    : 'def' ID '(' paramList? ')' block        #FuncDefStmt
    ;

paramList
    : ID (',' ID)*
    ;

funcCall
    : ID '(' argList? ')'                      #FuncCallExpr
    ;

argList
    : expr (',' expr)*
    ;

// Expresiones

expr
    : expr 'or' andExpr                        #OrOp
    | andExpr                                  #AndExprRoot
    ;

andExpr
    : andExpr 'and' relExpr                    #AndOp
    | relExpr                                  #RelExprRoot
    ;

relExpr
    : addExpr (relOp addExpr)?                 #RelOpExpr
    ;

relOp
    : '==' | '!=' | '<' | '<=' | '>' | '>='
    ;

addExpr
    : addExpr ('+' | '-') mulExpr              #AddSubExpr
    | mulExpr                                  #MulRoot
    ;

mulExpr
    : mulExpr ('*' | '/' | '%') powExpr        #MulDivExpr
    | powExpr                                  #PowRoot
    ;

powExpr
    : unaryExpr ('^' unaryExpr)*               #PowerOp
    ;

unaryExpr
    : '-' unaryExpr                            #UnaryMinusExpr
    | '+' unaryExpr                            #UnaryPlusExpr
    | 'not' unaryExpr                          #UnaryNotExpr
    | primary                                  #PrimaryExpr
    ;

primary
    : NUMBER                                   #NumberLiteralExpr
    | STRING                                   #StringLiteralExpr
    | 'true'                                   #TrueLiteralExpr
    | 'false'                                  #FalseLiteralExpr
    | ID                                       #IdentifierExpr
    | funcCall                                 #FuncCallPrimary
    | listLiteral                              #ListLiteralExpr
    | '(' expr ')'                             #ParenExpr
    ;

// listas y matrices

listLiteral
    : '[' (expr (',' expr)*)? ']'              #ListLiteralNode
    ;

// lexico

ID
    : [a-zA-Z_][a-zA-Z_0-9]*
    ;

NUMBER
    : DIGIT+ ('.' DIGIT+)?                     // enteros y reales
    ;

STRING
    : '"' (~["\r\n])* '"'
    | '\'' (~['\r\n])* '\''
    ;

WS
    : [ \t\r\n]+ -> skip
    ;

COMMENT
    : '#' ~[\r\n]* -> skip
    ;

fragment DIGIT : [0-9];
