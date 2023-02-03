from random_word import RandomWords

def getWord(r = RandomWords()):
    return r.get_random_word(hasDictionaryDef='true', includePartOfSpeech='noun,adjective', minCorpusCount='20', minLength='5', maxLength='7')

def Head(num = 0):
    return ' ___ \n/   \\\n\   /\n ---   \n'

def Body(arms = 0):
    result = ''
    if arms == 2:
        result = ' /|\\\n/ | \\'
    elif arms == 1:
        result = ' /|  \n/ |  '
    else:
        result = '  |  \n  |  '
    return result + '\n  |  \n'

def Legs(legs = 0):
    if legs == 2:
        return ' / \\ \n/   \\'
    else:
        return ' /\n/'

HANGMAN = {
    0: [''],
    1: [Head()],
    2: [Head(), Body()],
    3: [Head(), Body(1)],
    4: [Head(), Body(2)],
    5: [Head(), Body(2), Legs()],
    6: [Head(), Body(2), Legs(2)],
}