import unicodedata
NONENGLISH_LETTERS  = "ابتپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیآ"

def mapPersian2EnglishAlphabet(character):
    if character in NONENGLISH_LETTERS:
        return unicodedata.name(character).split()[-1]
    
    return character
     
def mapPersian2EnglishAlphabet_Get_Word(word):
    out = ''
    for character in word:
        out +=  unicodedata.name(character).split()[-1]
    
    return out
    
