#ifndef SYNTAXANALYZER_H
#define SYNTAXANALYZER_H

#define TOKEN_IDENTIFIER    1
#define TOKEN_INTEGER       2
#define TOKEN_IF            3
#define TOKEN_ELSE          4
#define TOKEN_END_IF        5
#define TOKEN_WHILE         6
#define TOKEN_END_WHILE     7
#define TOKEN_ASSIGN        8
#define TOKEN_PLUS          9
#define TOKEN_MULTIPLY      10
#define TOKEN_POWER         11
#define TOKEN_SEMICOLON     12
#define TOKEN_LPAREN        13
#define TOKEN_RPAREN        14
#define TOKEN_LESS          15
#define TOKEN_GREATER       16
#define TOKEN_EQUAL         17
#define TOKEN_EOF           18
#define TOKEN_UNKNOWN       0

#define STACK_SIZE          500
#define MAX_RULE_LENGTH     10

struct Token {
    int type;
    char value[256];
    int line;
    int position;
};

struct ParseStep {
    int stepNumber;
    int stack[STACK_SIZE];
    int stackTop;
    int currentToken;
    char action[256];
    bool isError;
};

class SyntaxAnalyzer {
private:
    Token* tokens;
    int tokenCount;
    int currentPos;

    int stack[STACK_SIZE];
    int stackTop;

    ParseStep* parseHistory;
    int historyCount;
    int historyCapacity;

    bool errorFlag;
    char errorMessage[256];

    void push(int symbol);
    int pop();
    int top();

    void addHistoryStep(const char* action, bool isError = false);
    void expandHistory();

    bool isTerminal(int symbol);
    bool isNonTerminal(int symbol);


public:
	SyntaxAnalyzer();
	~SyntaxAnalyzer();
    const char* getSymbolName(int symbol);
    void setTokens(Token* tokenList, int count);
    bool parse();

    int getHistoryCount() { return historyCount; }
    ParseStep* getHistoryStep(int index) {
        if (index >= 0 && index < historyCount)
            return &parseHistory[index];
        return 0;
    }

    bool hasError() { return errorFlag; }
    const char* getErrorMessage() { return errorMessage; }

    void clear();
};

#endif
