import string, re
import PyPDF2


'''
    Script to read Mueller PDF report and parse to text  
'''

def parsePDF(filename, page_start, page_end):
    '''

    :param filename: PDF file to extract data from
    :param page_start: integer - start page
    :param page_end: integer - end page
    :return: string with text
    '''
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


def cleanup_text(text_string):
    '''
    Function to remove digits & punctuation from string (utf-8)
    Also lower case
    :param text_string: string to clean
    :return: clean string
    '''

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
    tokens = [word for word in tokens if word not in set(stopWords.words("English"))]
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [word for word in tokens if word != '']
    tokens = [word for word in tokens if len(word) > 2]
    return tokens



if __name__ == '__main__':
    """
    Script to read Mueller PDF report and parse to text  
    
    Flags:    
        -toFile: y to write to file or n
        -outputFile: name of txt file to write parsed output

    # to use with flags to write to file:
    python extract_mueller_text.py -toFile y -o <data/testfile.txt> 
    """

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outputFile", help="example.txt")
    parser.add_argument("-toFile", "--toFile", help="y or n")

    # get arguments
    args = parser.parse_args()

    outputFile = args.outputFile
    toFile= args.toFile

    # Mueller report starts at page 9
    start = 9
    end =  439
    pdffile = "mueller-report-searchable.pdf"
    # read PDF and parse to text
    text_result = parsePDF(filename = pdffile, page_start= start, page_end=end)
    # clean string
    clean_text = cleanup_text(text_result)
    print("*"*20)
    print("Cleaned text")
    print("*" * 20)
    # split words into list
    tokens = get_tokens(clean_text)

    if toFile =='y':
        print("*"*20)
        print("writing to file")
        print("*" * 20)
        # write text to file
        with open(outputFile, 'w+') as text_file:
            text_file.write(clean_text.encode('utf-8'))

    # write words to file
    with open('mueller_words.txt', 'w+') as word_file:
        for l in tokens:
            word_file.write(l.encode('utf-8').strip())
            word_file.write('\n')
