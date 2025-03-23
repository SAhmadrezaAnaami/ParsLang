#######################################
# IMPORTS
#######################################

import string
from utils.mapPersian2EnglishAlphabet import mapPersian2EnglishAlphabet_Get_Word

#######################################
# CONSTANTS
#######################################

DIGITS              = '0123456789'
LETTERS             = string.ascii_letters
LETTERS_DIGITS      = LETTERS + DIGITS
NONENGLISH_DIGITS   = '۰۱۲۳۴۵۶۷۸۹'
NONENGLISH_LETTERS  = "ابتپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیآ"
IF_STATEMENTS       = ['if', 'IF' , 'If']
ELIF_STATEMENTS     = ['elif', 'Elif', 'ELIF', 'ElseIf', 'ELSEIF']
ELSE_STATEMENTS     = ['else', 'Else', 'ELSE']
THEN_STATEMENTS     = ['then', 'Then', 'THEN']
VAR_STATEMENTS      = ['var' , 'Var' , 'VAR', 'LET', 'let', "Let"]
AND_STATEMENTS      = ['and' , 'AND' , 'And']
OR_STATEMENTS       = ['or'  , 'Or'  , 'OR']
NOT_STATEMENTS      = ['not' , 'Not' , 'NOT']
FOR_STATEMENTS      = ['for' , 'For' , 'FOR']
TO_STATEMENTS       = ['to'  , 'TO'  , 'To']
STEP_STATEMENTS     = ['STEP', 'step', 'Step']
WHILE_STATEMENTS    = ['while', 'While', 'WHILE']
TRUE_STATEMENTS     = ['true',  'TRUE', 'True', mapPersian2EnglishAlphabet_Get_Word('صحیح')]
FALSE_STATEMENTS    = ['false', 'FALSE','False', mapPersian2EnglishAlphabet_Get_Word('غلط')]
NULL_STATEMENTS     = ['null', 'NULL', 'Null', mapPersian2EnglishAlphabet_Get_Word('پوچ')]


NONENGLISH_MAP      = {

    "اگر"       : "if",
    "مگر"       : "elif",
    "اگرهم"     : "elif",
    "وگرنه"     : "else",
    
    "انگاه"     : "then",
    "اووخ"      : "then",
    
    "متغیر"     : "var",
    "بگیر"      : "var",
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
}


