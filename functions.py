

def clean_word(word):
    '''
    Function to remove non alpha characters for a word
    :param word: string
    :return: cleaned string
    '''
    delete_chars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
    return word.translate(None, delete_chars)

def lematize_word(word, pos):
    '''
    Function uses WordNetLemmatizer
    :param word: string to lemmatize
    :param pos: n or v (part of speech to give context on how to lematize)
    :return: lemmatized string
    '''
    from nltk.stem import WordNetLemmatizer
    wnl = WordNetLemmatizer()
    token_lem = wnl.lemmatize(word, pos=pos)

    return token_lem

def stem_word(word, stemmer):
    '''

    :param word:string to stem
    :param stemmer: which stemmer to use: specify 'port', 'lancaster' or 'snowball'
    :return: string
    '''
    from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer
    port = PorterStemmer()
    lancaster = LancasterStemmer()
    snowball = SnowballStemmer('english', ignore_stopwords=False)
    if stemmer == 'port':
        token_stem = port.stem(word=word)
    elif stemmer == 'lancaster':
        token_stem = lancaster.stem(word=word)
    elif stemmer == 'snowball':
        token_stem = snowball.stem(word=word)
    return token_stem
