#######################################
# IMPORTS
#######################################

import string
from utils.mapPersian2EnglishAlphabet import mapPersian2EnglishAlphabet_Get_Word

#######################################
# CONSTANTS
#######################################

DIGITS                  = '0123456789'
LETTERS                 = string.ascii_letters
LETTERS_DIGITS          = LETTERS + DIGITS
NONENGLISH_DIGITS       = '۰۱۲۳۴۵۶۷۸۹'
NONENGLISH_LETTERS      = "ابتپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیآ"
IF_STATEMENTS           = ['if', 'IF' , 'If']
ELIF_STATEMENTS         = ['elif', 'Elif', 'ELIF', 'ElseIf', 'ELSEIF']
ELSE_STATEMENTS         = ['else', 'Else', 'ELSE']
THEN_STATEMENTS         = ['then', 'Then', 'THEN']
VAR_STATEMENTS          = ['var' , 'Var' , 'VAR', 'LET', 'let', "Let"]
AND_STATEMENTS          = ['and' , 'AND' , 'And']
OR_STATEMENTS           = ['or'  , 'Or'  , 'OR']
NOT_STATEMENTS          = ['not' , 'Not' , 'NOT']
FOR_STATEMENTS          = ['for' , 'For' , 'FOR']
TO_STATEMENTS           = ['to'  , 'TO'  , 'To']
STEP_STATEMENTS         = ['STEP', 'step', 'Step']
WHILE_STATEMENTS        = ['while', 'While', 'WHILE']
TRUE_STATEMENTS         = ['true',  'TRUE', 'True', mapPersian2EnglishAlphabet_Get_Word('صحیح')]
FALSE_STATEMENTS        = ['false', 'FALSE','False', mapPersian2EnglishAlphabet_Get_Word('غلط')]
NULL_STATEMENTS         = ['null', 'NULL', 'Null', mapPersian2EnglishAlphabet_Get_Word('پوچ')]
FUN_STATEMENTS          = ['fun', 'Fun', 'FUN', 'def', 'DEF', 'Def']
END_STATEMENTS          = ['end', 'END', 'End']
CONTINUE_STATEMENTS     = ['continue', 'CONTINUE', 'Continue']
BREAK_STATEMENTS        = ['break', 'BREAK', 'Break']
RETURN_STATEMENTS       = ['return', 'RETURN', 'Return']
PRINT_STATEMENTS        = ['print', 'PRINT', 'Print', 'bechup']
PRINT_RET_STATEMENTS    = ['print_ret', 'PRINT_RET', 'Print_ret']
INPUT_STATEMENTS        = ['input', 'INPUT', 'Input']
INPUT_INT_STATEMENTS    = ['input_int', 'INPUT_INT', 'Input_int']
CLEAR_STATEMENTS        = ['clear', 'CLEAR', 'Clear']
IS_NUMBER_STATEMENTS    = ['is_number', 'IS_NUMBER', 'Is_number']
IS_STRING_STATEMENTS    = ['is_string', 'IS_STRING', 'Is_string']
IS_LIST_STATEMENTS      = ['is_list', 'IS_LIST', 'Is_list']
IS_FUNCTION_STATEMENTS  = ['is_function', 'IS_FUNCTION', 'Is_function']
APPEND_STATEMENTS       = ['append', 'APPEND', 'Append']
EXTEND_STATEMENTS       = ['extend', 'EXTEND', 'Extend']
POP_STATEMENTS          = ['pop', 'POP', 'Pop']
LEN_STATEMENTS          = ['len', 'LEN', 'Len']
RUN_STATEMENTS          = ['run', 'RUN', 'Run']



NONENGLISH_MAP      = {

    "اگر"       : "if",
    "مگر"       : "elif",
    "اگرهم"     : "elif",
    "وگرنه"     : "else",
    
    "انگاه"     : "then",
    "اووخ"      : "then",
    
    "متغیر"     : "var",
    "قرارده"    : "var",
    "موگوم"     : "var",
    
    "و"         : "and",
    "یا"        : "or",
    "نه"        : "not",
    
    "ازای"      : "for",
    "برای"      : "for",
    "واسه"      : "for",
    
    "تا"        : "to",

    "گام"       : "step",
    
    "هنگامیکه"  : "while",
    
    "تابع"      : "fun",
    
    "تمام"      : "end",
    
    "ادامه"     : "continue",
    
    "بیخیال"    : "break",
    
    "برگردان"   : "return",
    
}


