import sys
import urllib.request as urllib
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse


def read_webpage(url):
    """Given a URL, it returns the string value of a webpage"""
    #read HTML from URL
    try:
        webpage_text = urllib.urlopen(url)
        webpage_bytes = webpage_text.read()
    except HTTPError as e:
        print(f"HTTP Error: {e.code}")
    except URLError as e:
        print(f"URL Error: {e.reason}")
    else: # convert from bytearray to string datatype
        webpage_string = webpage_bytes.decode('utf-8')
        return webpage_string


def download_to_file(text, filename):
    """Given text and a filename, it writes it to a file"""
    #format filename to repository directory
    filename = f"Repository/{filename}.txt"

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
    """Given a URL, it returns the validity of said URL"""
    try:
        valid_url = urlparse(url)
        return all([valid_url.scheme, valid_url.netloc])
    except AttributeError:
        return False


def main():
    url = "https://www.google.com"
    if url_format(url) == False :
        # work on code to handle malformed url strings
        print("Bad URL")
        sys.exit()

    web_string = read_webpage(url)
    print(web_string)
    download_to_file(web_string, "web_scrape_demo")


if __name__=="__main__":
    main()