object MainForm: TMainForm
  Left = 0
  Top = 0
  Caption = 'MainForm'
  ClientHeight = 852
  ClientWidth = 1195
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -25
  Font.Name = 'Segoe UI'
  Font.Style = []
  Position = poScreenCenter
  TextHeight = 35
  object PanelTop: TPanel
    Left = 0
    Top = 0
    Width = 1195
    Height = 50
    Align = alTop
    Caption = 'Lexical Analyzer'
    Font.Charset = RUSSIAN_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = 'Arial'
    Font.Style = [fsBold]
    ParentFont = False
    TabOrder = 0
    ExplicitWidth = 900
  end
  object MemoSource: TMemo
    Left = 8
    Top = 68
    Width = 320
    Height = 549
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -12
    Font.Name = 'Arial'
    Font.Style = []
    ParentFont = False
    ScrollBars = ssVertical
    TabOrder = 1
  end
  object GroupBoxLexems: TGroupBox
    Left = 340
    Top = 68
    Width = 389
    Height = 541
    Caption = 'Lexem Table'
    DefaultHeaderFont = False
    HeaderFont.Charset = DEFAULT_CHARSET
    HeaderFont.Color = clWindowText
    HeaderFont.Height = -20
    HeaderFont.Name = 'Segoe UI'
    HeaderFont.Style = []
    TabOrder = 2
    object GridLexems: TStringGrid
      Left = 4
      Top = 37
      Width = 382
      Height = 500
      ColCount = 4
      DefaultRowHeight = 30
      FixedCols = 0
      RowCount = 1
      FixedRows = 0
      Font.Charset = RUSSIAN_CHARSET
      Font.Color = clWindowText
      Font.Height = -25
      Font.Name = 'Arial'
      Font.Style = []
      ParentFont = False
      TabOrder = 0
    end
  end
  object GroupBoxIdentifiers: TGroupBox
    Left = 761
    Top = 68
    Width = 349
    Height = 188
    Caption = 'Identifier Table'
    TabOrder = 3
    object GridIdentifiers: TStringGrid
      Left = 17
      Top = 46
      Width = 415
      Height = 170
      ColCount = 4
      DefaultRowHeight = 30
      FixedCols = 0
      RowCount = 1
      FixedRows = 0
      Font.Charset = RUSSIAN_CHARSET
      Font.Color = clWindowText
      Font.Height = -25
      Font.Name = 'Arial'
      Font.Style = []
      ParentFont = False
      TabOrder = 0
    end
  end
  object GroupBoxConstants: TGroupBox
    Left = 764
    Top = 254
    Width = 349
    Height = 200
    Caption = 'Constant Table'
    TabOrder = 4
    object GridConstants: TStringGrid
      Left = 11
      Top = 42
      Width = 335
      Height = 170
      ColCount = 4
      DefaultRowHeight = 30
      FixedCols = 0
      RowCount = 1
      FixedRows = 0
      Font.Charset = RUSSIAN_CHARSET
      Font.Color = clWindowText
      Font.Height = -25
      Font.Name = 'Arial'
      Font.Style = []
      ParentFont = False
      TabOrder = 0
    end
  end
  object ButtonAnalyze: TButton
    Left = 8
    Top = 644
    Width = 100
    Height = 30
    Caption = 'Analyze'
    TabOrder = 5
    OnClick = ButtonAnalyzeClick
  end
  object ButtonClear: TButton
    Left = 114
    Top = 644
    Width = 100
    Height = 30
    Caption = 'Clear'
    TabOrder = 6
    OnClick = ButtonClearClick
  end
  object ButtonLoadExample: TButton
    Left = 230
    Top = 644
    Width = 171
    Height = 30
    Caption = 'Load Example'
    TabOrder = 7
    OnClick = ButtonLoadExampleClick
  end
  object StatusBar: TStatusBar
    Left = 0
    Top = 832
    Width = 1195
    Height = 20
    Panels = <>
    SimplePanel = True
    ExplicitTop = 680
    ExplicitWidth = 900
  end
end
