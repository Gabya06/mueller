import string, re
import PyPDF2
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as stopWords

def parsePDF(filename, page_start, page_end):
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

    text = ''
    for i in range(start, end):
        print("processed page" , str(i))
        pageObj = pdfReader.getPage(i)
        text += pageObj.extractText()
    return(text)

start = 9
end =  439
pdffile = "mueller-report-searchable.pdf"
text_result = parsePDF(filename = pdffile, page_start= start, page_end=end)


stop_words = set(stopWords.words('English'))
# since we have unicode
punct =  dict((ord(char), None) for char in string.punctuation)
# clean up punctuation
text = text_result.translate(punct)
# remove numbers
text = re.sub(r'\d+', '', text)
text = text.lower()
# split words into list
tokens = word_tokenize(text)

# remove stop words
tokens = [word for word in tokens if word not in set(stopWords.words("English"))]
tokens = [word for word in tokens if word not in stop_words]
tokens = [word for word in tokens if word != '']
tokens = [word for word in tokens if len(word)>2]

# write text to file
with open('mueller_text.txt', 'w+') as text_file:
    text_file.write(text.encode('utf-8'))

# write words to file
with open('mueller_words.txt', 'w+') as word_file:
    for l in tokens:
        word_file.write(l.encode('utf-8').strip())
        word_file.write('\n')
