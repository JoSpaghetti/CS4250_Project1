# imports necessary libraries
from bs4 import BeautifulSoup
from nltk.stem import *
import re
import os

def clean_HTML(html_doc):
    """
    This function cleans the HTML file using BeautifulSoup to extract the plain text.
    """
    # with open(html_doc) as doc:
    with open(html_doc, encoding='utf-8', errors='ignore') as doc: # prevent encoding issues when opening files
        # soup = BeautifulSoup(doc, "html5lib") # creates a BeautifulSoup object using HTML file
        soup = BeautifulSoup(doc, "html.parser") # faster than html5lib

    for tags in soup(['script', 'style']):
        tags.decompose() # removes script and style tags

    # extracts text from HTML and returns it as a string
    cleaned_text = soup.get_text(separator=' ') # separator checks for spacing between tags
    return cleaned_text

def tokenize(text):
    """
    This function tokenizes the text by retaining alphanumeric characters.
    """
    # tokens = re.findall(r'\b\w+\b', text) # tokenize cleaned HTML
    tokens = re.findall(r'\b\w+\b', text.lower()) # tokenize cleaned HTML AND case handling
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
    return tokens, stemmed_tokens   # returns both tokens and stemmed tokens

def process_repository(directory):
    """
    This function applies text processing to the HTML files in a given directory.
    Save both tokenized and stemmed outputs to separate .txt files.
    """
    output_dir = os.path.join(directory, "Processed_Text") # create a full path for the output folder
    os.makedirs(output_dir, exist_ok=True) # ensure output directory exists

    for file in os.listdir(directory): # traverses all files in a directory
        if file.endswith('.html'):     # checks for HTML files
            '''
            with open(os.path.join(directory, file)) as doc: # applies text processing to HTML files
                text = text_process(doc.name)
                print(text)
                print(len(text))
            '''
            filepath = os.path.join(directory, file) # construct the full file path for the current html file
            tokens, stemmed_text = text_process(filepath)

            # construct the output file path
            # tokenized_file = os.path.join(output_dir, f"{file}_tokenized.txt")
            stemmed_file = os.path.join(output_dir, f"{file}_stemmed.txt") 
            
            # Save tokenized text
            #with open(tokenized_file, "w", encoding="utf-8") as out:
            #    out.write(" ".join(tokens))

            # Save stemmed text
            with open(stemmed_file, "w", encoding="utf-8") as out: # write the processed text to a new .txt file
                out.write(" ".join(stemmed_text)) # join the tokens into a space-separated string

            print(f"Processed: {file} → Stemmed: {stemmed_file}")


def main():
    """
    This function executes tokenizing and stemming on HTML files in specific directories.
    """

    # directory = "../CodePart1-WebCrawler/Repository" # sample run on current repository
    # process_repository(directory)

    directory = "Code/CodePart1-WebCrawler/Repository"
    print(f"Processing HTML files in: {os.path.abspath(directory)}")

    if os.path.exists(directory):
        process_repository(directory)
        print("\nProcess completed! Check 'Processed_Text/' for output.")
    else:
        print(f"Error: Directory {directory} not found.")

    '''
    # Sample Output: Testing to see the first 50 stemmed words
    
    test_file = "texting.html"  
    test_path = os.path.join(directory, test_file)
    
    if os.path.exists(test_path):
        print(f"Testing file: {test_file}")
        stemmed_tokens = text_process(test_path)
        print("\nSample Output (First 50 Tokens):")
        print(stemmed_tokens[:50])  # Print first 50 stemmed words
        print(f"\nTotal Tokens: {len(stemmed_tokens)}")
    else:
        print(f"Error: File {test_file} not found in {directory}")
    '''

if __name__ == "__main__":
    main()
