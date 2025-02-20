# imports necessary libraries
from bs4 import BeautifulSoup
from nltk.stem import *
import re
import os

def clean_HTML(html_doc):
    """
    This function cleans the HTML file using BeautifulSoup to extract the plain text.
    """
    with open(html_doc) as doc:
        soup = BeautifulSoup(doc, "html5lib") # creates a BeautifulSoup object using HTML file

    for tags in soup(['script', 'style']):
        tags.decompose() # removes script and style tags

    # extracts text from HTML and returns it as a string
    cleaned_text = soup.get_text(separator=' ') # separator checks for spacing between tags
    return cleaned_text

def tokenize(text):
    """
    This function tokenizes the text by retaining alphanumeric characters.
    """
    tokens = re.findall(r'\b\w+\b', text) # tokenize cleaned HTML
    return tokens

def stem(tokens):
    """
    This function applies stemming to tokens and stores stems in an array.
    """
    stemmer = PorterStemmer() # used to stem tokens
    stemmed_tokens = [stemmer.stem(token) for token in tokens] # apply stemming to tokens
    return stemmed_tokens

def text_process(html_doc):
    """
    This function processes text in the HTML file and returns the stemmed tokens.
    """
    text = clean_HTML(html_doc)     # extracts text from HTML
    tokens = tokenize(text)         # tokenizes text
    stemmed_tokens = stem(tokens)   # stems tokens; can change how to stem tokens based on language of text
    return stemmed_tokens           # returns stemmed tokens

def process_repository(directory):
    """
    This function applies text processing to the HTML files in a given directory.
    """
    for file in os.listdir(directory): # traverses all files in a directory
        if file.endswith('.html'):     # checks for HTML files
            with open(os.path.join(directory, file)) as doc: # applies text processing to HTML files
                text = text_process(doc.name)
                print(text)
                print(len(text))

    # ADD CODE TO WRITE PROCESSED TEXT TO .TXT FILE


def main():
    """
    This function executes tokenizing and stemming on HTML files in specific directories.
    """

    directory = "../CodePart1-WebCrawler/Repository" # sample run on current repository
    process_repository(directory)

main()
