#include <vcl.h>
#pragma hdrstop

#include "Main.h"
#include "../LexicalBlock/LexicalBlock.h"
#include "../LexicalBlock/LexicalBlock.cpp"
#include "../SyntaxAnalyzer/SyntaxAnalyzer.h"
#include "../SyntaxAnalyzer/SyntaxAnalyzer.cpp"

#pragma package(smart_init)
#pragma resource "*.dfm"

TMainForm* MainForm;

bool strEqual(const char* a, const char* b)
{
    if (a == b)
        return true;
    if (!a || !b)
        return false;
    while (*a && *b) {
        if (*a != *b)
            return false;
        a++;
        b++;
    }
    return *a == *b;
}

void strCopy(char* dest, const char* src)
{
    if (!dest || !src)
        return;
    while (*src) {
        *dest = *src;
        dest++;
        src++;
    }
    *dest = '\0';
}

int strLen(const char* str)
{
    int len = 0;
    while (str && str[len])
        len++;
    return len;
}

char* strDup(const char* src)
{
    if (!src)
        return 0;
    int len = strLen(src);
    char* dest = new char[len + 1];
    for (int i = 0; i < len; i++) {
        dest[i] = src[i];
    }
    dest[len] = '\0';
    return dest;
}
__fastcall TMainForm::TMainForm(TComponent* Owner) : TForm(Owner)
{
    lexer = new LexicalBlock();
    parser = new SyntaxAnalyzer();
    currentTokens = 0;
    currentTokenCount = 0;

    SetupGrids();

    Caption = "Syntactic Analyzer";
    Width = 1000;
    Height = 750;
    Position = poScreenCenter;

    MemoSource->Text = "";
    MemoSource->Font->Name = "Courier New";
    MemoSource->Font->Size = 10;

    StatusBar->SimpleText = "Ready";
}

__fastcall TMainForm::~TMainForm()
{
    delete lexer;
    delete parser;
    delete[] currentTokens;
}

void __fastcall TMainForm::SetupGrids()
{
    GridTokens->ColCount = 5;
    GridTokens->RowCount = 1;
    GridTokens->FixedRows = 0;
    GridTokens->Cells[0][0] = "#";
    GridTokens->Cells[1][0] = "Lexem";
    GridTokens->Cells[2][0] = "Class";
    GridTokens->Cells[3][0] = "Token";
    GridTokens->Cells[4][0] = "Position";
    GridTokens->ColWidths[0] = 40;
    GridTokens->ColWidths[1] = 150;
    GridTokens->ColWidths[2] = 120;
    GridTokens->ColWidths[3] = 120;
    GridTokens->ColWidths[4] = 80;

    GridParseSteps->ColCount = 5;
    GridParseSteps->RowCount = 1;
    GridParseSteps->FixedRows = 0;
    GridParseSteps->Cells[0][0] = "Step";
    GridParseSteps->Cells[1][0] = "Stack";
    GridParseSteps->Cells[2][0] = "Input";
    GridParseSteps->Cells[3][0] = "Action";
    GridParseSteps->Cells[4][0] = "Status";
    GridParseSteps->ColWidths[0] = 50;
    GridParseSteps->ColWidths[1] = 250;
    GridParseSteps->ColWidths[2] = 100;
    GridParseSteps->ColWidths[3] = 400;
    GridParseSteps->ColWidths[4] = 80;
}

UnicodeString TMainForm::GetTokenClass(int classId)
{
    switch (classId) {
        case 1:
            return "Identifier";
        case 2:
            return "Keyword";
        case 3:
            return "Integer";
        case 4:
            return "Delimiter";
        default:
            return "Unknown";
    }
}

UnicodeString TMainForm::GetTokenName(int tokenType)
{
    switch (tokenType) {
        case TOKEN_IDENTIFIER:
            return "IDENTIFIER";
        case TOKEN_INTEGER:
            return "INTEGER";
        case TOKEN_IF:
            return "IF";
        case TOKEN_ELSE:
            return "ELSE";
        case TOKEN_END_IF:
            return "END_IF";
        case TOKEN_WHILE:
            return "WHILE";
        case TOKEN_END_WHILE:
            return "END_WHILE";
        case TOKEN_ASSIGN:
            return "ASSIGN";
        case TOKEN_PLUS:
            return "PLUS";
        case TOKEN_MULTIPLY:
            return "MULTIPLY";
        case TOKEN_POWER:
            return "POWER";
        case TOKEN_SEMICOLON:
            return "SEMICOLON";
        case TOKEN_LPAREN:
            return "LPAREN";
        case TOKEN_RPAREN:
            return "RPAREN";
        case TOKEN_LESS:
            return "LESS";
        case TOKEN_GREATER:
            return "GREATER";
        case TOKEN_EQUAL:
            return "EQUAL";
        case TOKEN_EOF:
            return "EOF";
        default:
            return "UNKNOWN";
    }
}

void __fastcall TMainForm::ButtonLoadExampleClick(TObject* Sender)
{
	const char* example =         "d=2*3+1;\n"
		"a=3+2*d;\n"
		"c=2*d+3*a;\n"
		"IF(d>c)\n"
		"    a=d*2;\n"
		"ELSE\n"
		"    a=d;\n"
		"END_IF\n"
		"i=1;\n"
		"WHILE(i<10)\n"
		"    i=i+1;\n"
		"END_WHILE\n";


	MemoSource->Text = example;
    StatusBar->SimpleText = "Example program loaded";
}

void __fastcall TMainForm::ButtonClearClick(TObject* Sender)
{
    MemoSource->Text = "";
    GridTokens->RowCount = 1;
    GridParseSteps->RowCount = 1;
    delete[] currentTokens;
    currentTokens = 0;
    currentTokenCount = 0;
    StatusBar->SimpleText = "Cleared";
}

void __fastcall TMainForm::ButtonLexicalClick(TObject* Sender)
{
    if (MemoSource->Text.IsEmpty()) {
        ShowMessage("Enter source code for lexical analysis");
        return;
    }

    AnsiString source = MemoSource->Text;
    const char* sourceCode = source.c_str();

    lexer->analyze(sourceCode);

    delete[] currentTokens;
    currentTokenCount = lexer->getLexemCount();
    currentTokens = new Token[currentTokenCount];

    for (int i = 0; i < currentTokenCount; i++) {
        Lexem* lex = lexer->getLexem(i);

        currentTokens[i].type = TOKEN_UNKNOWN;

        if (lex->classId == LEXEM_CLASS_IDENTIFIER) {
            currentTokens[i].type = TOKEN_IDENTIFIER;
        } else if (lex->classId == LEXEM_CLASS_KEYWORD) {
            if (strEqual(lex->value, "IF"))
                currentTokens[i].type = TOKEN_IF;
            else if (strEqual(lex->value, "ELSE"))
                currentTokens[i].type = TOKEN_ELSE;
            else if (strEqual(lex->value, "END_IF"))
                currentTokens[i].type = TOKEN_END_IF;
            else if (strEqual(lex->value, "WHILE"))
                currentTokens[i].type = TOKEN_WHILE;
            else if (strEqual(lex->value, "END_WHILE"))
                currentTokens[i].type = TOKEN_END_WHILE;
        } else if (lex->classId == LEXEM_CLASS_INTEGER) {
            currentTokens[i].type = TOKEN_INTEGER;
        } else if (lex->classId == LEXEM_CLASS_DELIMITER) {
            if (strEqual(lex->value, "="))
                currentTokens[i].type = TOKEN_ASSIGN;
            else if (strEqual(lex->value, "=="))
                currentTokens[i].type = TOKEN_EQUAL;
            else if (strEqual(lex->value, "<"))
                currentTokens[i].type = TOKEN_LESS;
            else if (strEqual(lex->value, ">"))
				currentTokens[i].type = TOKEN_GREATER;
            else if (strEqual(lex->value, "+"))
                currentTokens[i].type = TOKEN_PLUS;
            else if (strEqual(lex->value, "*"))
                currentTokens[i].type = TOKEN_MULTIPLY;
            else if (strEqual(lex->value, "^"))
                currentTokens[i].type = TOKEN_POWER;
            else if (strEqual(lex->value, ";"))
                currentTokens[i].type = TOKEN_SEMICOLON;
            else if (strEqual(lex->value, "("))
                currentTokens[i].type = TOKEN_LPAREN;
            else if (strEqual(lex->value, ")"))
                currentTokens[i].type = TOKEN_RPAREN;
        }
    }

    DisplayTokens();

    StatusBar->SimpleText = "Lexical analysis complete. Tokens: " +
                            UnicodeString(currentTokenCount);
}

void TMainForm::DisplayTokens()
{
    GridTokens->RowCount = currentTokenCount + 1;

    for (int i = 0; i < currentTokenCount; i++) {
        GridTokens->Cells[0][i + 1] = i + 1;
        GridTokens->Cells[1][i + 1] = UnicodeString(currentTokens[i].value);
        GridTokens->Cells[2][i + 1] =
			GetTokenClass(lexer->getLexem(i)->classId);
        GridTokens->Cells[3][i + 1] = GetTokenName(currentTokens[i].type);
        GridTokens->Cells[4][i + 1] = UnicodeString(currentTokens[i].line) +
                                      ":" +
                                      UnicodeString(currentTokens[i].position);
    }
}

void __fastcall TMainForm::ButtonSyntacticClick(TObject* Sender)
{
    if (currentTokenCount == 0) {
        ShowMessage("Perform lexical analysis first");
        return;
    }

    parser->setTokens(currentTokens, currentTokenCount);

    bool result = parser->parse();

    DisplayParseHistory();

    if (result) {
        StatusBar->SimpleText =
            "Syntactic analysis: SUCCESS - Program is syntactically correct";
        ShowMessage("Program is syntactically correct!");
    } else {
        StatusBar->SimpleText = "Syntactic analysis: ERROR - " +
                                UnicodeString(parser->getErrorMessage());
        ShowMessage(
			"Syntax Error: " + UnicodeString(parser->getErrorMessage()));
	}
}

void TMainForm::DisplayParseHistory()
{
    int historyCount = parser->getHistoryCount();
    GridParseSteps->RowCount = historyCount + 1;

    for (int i = 0; i < historyCount; i++) {
        ParseStep* step = parser->getHistoryStep(i);

        GridParseSteps->Cells[0][i + 1] = step->stepNumber;

        UnicodeString stackStr = "";
        for (int j = 0; j <= step->stackTop; j++) {
            if (j > 0)
                stackStr += " ";
			stackStr += parser->getSymbolName(step->stack[j]);
        }
        GridParseSteps->Cells[1][i + 1] = stackStr;

        GridParseSteps->Cells[2][i + 1] =
            parser->getSymbolName(step->currentToken);
        GridParseSteps->Cells[3][i + 1] = UnicodeString(step->action);
		GridParseSteps->Cells[4][i + 1] = step->isError ? "ERROR" : "OK";

    }
}

