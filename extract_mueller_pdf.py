'''
    Script to parse Mueller PDF report - uses PDFMiner

'''

import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO


def pdfparser(data):
    '''

    :param data: pdf file to read and extract text from
    :return:
    '''
    result = ''
    fp = file(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        temp =  retstr.getvalue()
        result += temp
    return(result)

data = 'mueller-report-searchable.pdf'
result = pdfparser(data=data)

if __name__ == '__main__':
    pdfparser(sys.argv[1])