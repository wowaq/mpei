#ifndef MAINFORM_H
#define MAINFORM_H

#include <Forms.hpp>
#include <StdCtrls.hpp>
#include <ComCtrls.hpp>
#include <ExtCtrls.hpp>
#include "LexicalBlock.h"
#include <System.Classes.hpp>
#include <Vcl.Controls.hpp>
#include <Vcl.Grids.hpp>

class TMainForm : public TForm {
    __published:
        TPanel *PanelTop;
        TMemo *MemoSource;
        TGroupBox *GroupBoxLexems;
        TStringGrid *GridLexems;
        TGroupBox *GroupBoxIdentifiers;
        TStringGrid *GridIdentifiers;
        TGroupBox *GroupBoxConstants;
        TStringGrid *GridConstants;
        TButton *ButtonAnalyze;
        TButton *ButtonClear;
        TButton *ButtonLoadExample;
        TStatusBar *StatusBar;

        void __fastcall ButtonAnalyzeClick(TObject *Sender);
        void __fastcall ButtonClearClick(TObject *Sender);
        void __fastcall ButtonLoadExampleClick(TObject *Sender);

    private:
        LexicalBlock* lexer;
        void SetupGrids();
        void DisplayResults();
        UnicodeString GetClassName(int classId);

    public:
        __fastcall TMainForm(TComponent* Owner);
        __fastcall ~TMainForm();
};

#endif
