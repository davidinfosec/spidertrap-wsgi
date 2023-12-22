#!/usr/bin/env python3

# Spider Trap

### Configuration Section ###
# the lower and upper limits of how many links to put on each page
LINKS_PER_PAGE = (5, 10)
# the lower and upper limits of how long each link can be
LENGTH_OF_LINKS = (3, 20)
# the delay between receiving a request and serving up a webpage (in milliseconds)
DELAY = 350
# characters to compose random links from
CHAR_SPACE = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-/'
### End Configuration Section ###

import sys
import random
import time

class SpiderTrapApp:
    webpages = None

    def __init__(self):
        pass

    def generate_page(self, seed):
        """Generate a webpage containing only random links"""
        html = '<html>\n<body>\n'
        random.seed(seed)
        num_pages = random.randint(*LINKS_PER_PAGE)
        for i in range(num_pages):
            address = ''.join([random.choice(CHAR_SPACE) for _ in range(random.randint(*LENGTH_OF_LINKS))])
            html += '<a href="' + address + '">' + address + '</a><br>\n'
        html += '</body>\n</html>'
        return html

    def __call__(self, environ, start_response):
        time.sleep(DELAY / 1000.0)
        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        start_response(status, headers)
        return [self.generate_page(environ.get('PATH_INFO', '')).encode()]

def load_webpages(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except IOError:
        print("Can't read input file. Using randomly generated links.")
        return None

app = SpiderTrapApp()
if len(sys.argv) == 2:
    app.webpages = load_webpages(sys.argv[1])
