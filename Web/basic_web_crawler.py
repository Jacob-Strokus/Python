# A basic web crawler to scrape a webpage for links, and look for emails.
# Jacob Strokus

#imports

import requests
import re
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

# regex
link_re = re.compile(r'href="(.*?)"')

# Function to crawl the webpage. Takes in the url as parameter.
def crawl(url):

    getReq = requests.get(url)

    # Check if we get 200 (we are able to access the website)
    if(getReq.status_code != 200):
        return []

    # Find links
    links = link_re.findall(getReq.text)

    print("\nFound {} links".format(len(links)))

    # Search links for emails
    for link in links:

        # Get an absolute URL for a link
        link = urljoin(url, link)

        print(link)

if __name__ == '__main__':

    url = input('Enter a website: ')
    crawl('http://' + url)
