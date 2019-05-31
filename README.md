## Project Overview
The goal of this project is analyze the Mueller Report.

## Data Processing and Cleaning
Data downloaded from [CNN] (https://cdn.cnn.com/cnn/2019/images/04/18/mueller-report-searchable.pdf) as a PDF report and there were 448 pages in the report. 

To get the data in a usable format, the PDF report had to be converted to text. 

```python
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
```

Once the data was extracted using pdfReader in Python, data cleaning involved removing digits, punctuation and converting all words to lowercase. Words such as "the", "and", "as", "of" were also removed by using the [NLTK libary] (https://www.nltk.org) and words were converted using lemmatization. I used lemmatization over stemming because I wanted my data to include actual words and stemming sometimes can return words that arent in fact real words. 

Lemmatization with Python nltk package:
*"Lemmatization, unlike Stemming, reduces the inflected words properly ensuring that the root word belongs to the language. In Lemmatization root word is called Lemma. A lemma (plural lemmas or lemmata) is the canonical form, dictionary form, or citation form of a set of words."*

```python
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

# lematize words - first for nouns then verbs
lem_n_words = [lematize_word(x, 'n') for x in cleaned_words]
lem_v_words = [lematize_word(x, 'v') for x in lem_n_words]
lem_v_counts = Counter(lem_v_words)
print("top 10 words found in report", lem_v_counts.most_common(20))
```

## Data Exploration & Visualization
Now that the data is cleaned, we can move on to some visualization... what words appear the most?
Not surprisignly, it looks like "president", "Russia", "Trump", "campaign" appear most frequently.

![top20_barchart](/images/top20_barchart.png)

### WordClouds

Creating wordclouds is quite simple, using the wordcloud library:

```python

wordcloud = WordCloud(width = 512, height = 512, background_color='white', max_font_size=50, max_words=150)
wordcloud = wordcloud.generate_from_frequencies(lem_v_counts)
plt.figure(figsize=(10,8),facecolor = 'white', edgecolor='blue')
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()                      
```

![wordcloud1](/images/wordcloud1.png)

We could also make a wordcloud in a specific shape based on a picture, for example:

```python
from matplotlib import cm
# generate wordcloud with custom settings 
wordcloud = WordCloud(width = 512, height = 512, background_color='white', colormap=cm.coolwarm, contour_width=10, contour_color='black', max_font_size=70, max_words=150)
mueller_mask = np.array(Image.open("img/mask2.jpeg"))
# change the shape of the wordcloud
wordcloud.mask = mueller_mask
# generate from frequencies 
wordcloud = wordcloud.generate_from_frequencies(lem_v_counts)

# show plot
plt.figure(figsize=(10,8),facecolor = 'white', edgecolor='blue')
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()
```



![wordcloud2](/images/wordcloud2.png)

But... Is this a bird or a dinosaur wordcloud?
