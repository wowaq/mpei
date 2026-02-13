#ifndef LEXICALBLOCK_H
#define LEXICALBLOCK_H

#define LEXEM_CLASS_IDENTIFIER   1
#define LEXEM_CLASS_KEYWORD      2
#define LEXEM_CLASS_INTEGER      3
#define LEXEM_CLASS_DELIMITER    4
#define LEXEM_CLASS_UNKNOWN      0

struct Lexem {
    int classId;
    wchar_t value[256];
    int line;
    int position;
    int intValue;
};

struct TableEntry {
	wchar_t* name;
    int classId;
    int intValue;
    bool isUsed;
};

class LexicalBlock {
private:
    TableEntry** identifierTable;
    int identifierCount;
    int identifierCapacity;

    TableEntry** constantTable;
    int constantCount;
    int constantCapacity;

    Lexem* lexems;
    int lexemCount;
    int lexemCapacity;

    const wchar_t* keywords[5];
    int keywordCount;

    const wchar_t* delimiters[10];
    int delimiterCount;

    static bool strEqual(const wchar_t* a, const wchar_t* b);
    static void strCopy(wchar_t* dest, const wchar_t* src);
    static int strLen(const wchar_t* str);
    static wchar_t* strDup(const wchar_t* src);
    static bool isDigit(wchar_t c);
    static bool isLetter(wchar_t c);
    static bool isWhitespace(wchar_t c);
    static void intToStr(int value, wchar_t* buffer);

    void expandIdentifierTable();
    void expandConstantTable();
    void expandLexemTable();
    int findIdentifier(const wchar_t* name);
    int findConstant(int value);

public:
    LexicalBlock();
    ~LexicalBlock();

    void analyze(const wchar_t* sourceCode);

    int addIdentifier(const wchar_t* name);
    int addConstant(int value);

    int getIdentifierCount() { return identifierCount; }
    TableEntry* getIdentifier(int index) {
        if (index >= 0 && index < identifierCount)
            return identifierTable[index];
        return 0;
    }

    int getConstantCount() { return constantCount; }
    TableEntry* getConstant(int index) {
        if (index >= 0 && index < constantCount)
            return constantTable[index];
        return 0;
    }

    int getLexemCount() { return lexemCount; }
    Lexem* getLexem(int index) {
        if (index >= 0 && index < lexemCount)
            return &lexems[index];
        return 0;
    }

    void clear();
};

#endif
