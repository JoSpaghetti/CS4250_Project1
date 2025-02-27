import sys
import urllib.request as urllib
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
import langid


def read_webpage(url):
    """Given a URL, it returns the string value of a webpage\n
    Arguments: url (string): the URL to fetch\n
    Returns: the string value of the webpage
    """

    try: #read HTML from URL
        webpage_text = urllib.urlopen(url)
        webpage_bytes = webpage_text.read()
    except HTTPError as e:
        print(f"HTTP Error: {e.code}")
    except URLError as e:
        print(f"URL Error: {e.reason}")
    else: # convert from bytearray to string datatype
        webpage_string = webpage_bytes.decode('utf-8')
        return webpage_string


def download_to_file(text, filename, extension="html"):
    """Given text and a filename, it writes it to a file\n
    Arguments: text (string): the text to write\n
    Arguments: filename (string): the name of the file\n
    Arguments: extension (string): the extension of the file [the default is "html"]\n
    Returns: None
    """
    #format filename to repository directory
    filename = f"Repository/{filename}.{extension}"

    #throw error if text or filename is null or empty
    if text is None or filename is None:
        raise TypeError("Input values  cannot be None")
    if text == "" or filename == "":
        raise ValueError("Input values cannot be empty")

    try : # write to file
        file = open(filename, 'w')
    except FileNotFoundError: #create new file and write to file
        file = open(filename, 'x')
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
        sys.exit()
    else:
        file.write(text)
        file.close()

def url_format(url):
    """Given a URL, it returns the validity of said URL \n
    Arguments: url (string): a URL to validate \n
    Returns: boolean expression based on validity of URL"""
    try:
        valid_url = urlparse(url)
        return all([valid_url.scheme, valid_url.netloc])
    except AttributeError:
        return False

def detect_language(text):
    """Using the langid library, it returns the language of a string sequence \n
    Arguments: text (string): the text to identify\n
    Returns: language of given input
    """
    return langid.classify(text)[0]

def main():
    url = "https://www.google.com"

    if not url_format(url):
        # work on code to handle malformed url strings
        print("Bad URL")
        sys.exit()

    web_string = read_webpage(url)
    web_string_language = detect_language(web_string)
    print(web_string, web_string_language)
    download_to_file(web_string, "web_scrape_demo")

if __name__=="__main__":
    main()