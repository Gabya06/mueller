
def parsePDF(filename, page_start, page_end):
    '''

    :param filename: PDF file to extract data from
    :param page_start: integer - start page
    :param page_end: integer - end page
    :return: string with text
    '''
    import PyPDF2

    # name of PDF file to parse (creates an object)
    pdfFileObj = open(filename,'rb')
    # pdfReader will be parsed
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # get start and end pages
    if not page_start:
        start = 1
    else:
        start = page_start
    if not page_end:
        end = pdfReader.numPages
    else:
        end = page_end

    # go through each page and extract text to string
    text = ''
    for i in range(start, end):
        print("processed page" , str(i))
        pageObj = pdfReader.getPage(i)
        text += pageObj.extractText()
    return(text)


def clean_word(word):
    '''
    Function to remove non alpha characters for a word
    :param word: string
    :return: cleaned string
    '''
    delete_chars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
    return word.translate(None, delete_chars)

# def lematize_word(word, pos):
#     '''
#     Function uses WordNetLemmatizer
#     :param word: string to lemmatize
#     :param pos: n or v (part of speech to give context on how to lematize)
#     :return: lemmatized string
#     '''
#     from nltk.stem import WordNetLemmatizer
#     wnl = WordNetLemmatizer()
#     token_lem = wnl.lemmatize(word, pos=pos)
#
#     return token_lem


def lematize_word(word):
    '''
    Function to return lemma for a word - uses WordNetLemmatizer
    1) find part of speech tag (pos)
    2) convert penn pos to wordnet pos
    3) return lemma based on tag

    :param word: string to lemmatize
    :param pos: n or v (part of speech to give context on how to lematize)
    :return: lemmatized string
    '''
    from nltk.stem import WordNetLemmatizer
    from nltk import pos_tag
    if word == '':
        pass
    # print("word: {}".format(word))
    res = pos_tag([word])

    word, pos = res[0][0], res[0][1]
    # convert to wordnet tag
    tag = penn_to_wn(pos)
    if tag:
        wnl = WordNetLemmatizer()
        token_lem = wnl.lemmatize(word, pos=tag)
        return token_lem
    else:
        pass

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


from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import sent_tokenize, word_tokenize, pos_tag


def penn_to_wn(tag):
    """
    Function to convert from pentreebank pos tag to wordnet pos tag
    credit: https://nlpforhackers.io/sentiment-analysis-intro/
    :param tag: PennTreeBank tag
    :return: WordNet tag
    """

    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None

def cleanup_text(text_string):
    '''
    Function to remove digits & punctuation from string (utf-8)
    Also lower case
    :param text_string: string to clean
    :return: clean string
    '''
    import string, re
    # since we have unicode
    punct = dict((ord(char), None) for char in string.punctuation)
    # clean up punctuation
    clean_string = text_string.translate(punct)
    # remove numbers
    clean_string = re.sub(r'\d+', '', clean_string)
    clean_string = clean_string.lower()
    return clean_string

def get_tokens(text_string):
    '''
    Function that takes in text string and returns list of words
    removes stop words & empty spaces & words with less then 2 characters

    :param text_string: text string
    :return: list of words
    '''
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords as stopWords

    stop_words = set(stopWords.words('English'))
    # split words into list
    tokens = word_tokenize(text_string)

    # remove stop words
    tokens = [word.lower() for word in tokens if word not in set(stopWords.words("English"))]
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [word for word in tokens if word != '']
    tokens = [word for word in tokens if len(word) > 2]
    return tokens