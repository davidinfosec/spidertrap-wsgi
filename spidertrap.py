#!/usr/bin/env python3

# Spider Trap

### Configuration Section ###
LINKS_PER_PAGE = (5, 10)
LENGTH_OF_LINKS = (3, 20)
DELAY = 350
CHAR_SPACE = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-/'
### End Configuration Section ###

import sys
import random
import time
import logging
import logging.handlers
import csv

# Logging Configuration
log_filename = 'spidertrap.csv'
max_log_size = 10 * 1024 * 1024 * 1024  # 10 GB
log_backup_count = 1  # Number of backup files to keep

# Setting up CSV logging
class CSVLogHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)
        self.writer = csv.writer(self.stream)

    def emit(self, record):
        if self.stream is None:
            self.stream = self._open()
        self.writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), record.message])
        self.flush()

logger = logging.getLogger('SpiderTrapLogger')
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=max_log_size, backupCount=log_backup_count)
logger.addHandler(handler)

class SpiderTrapApp:
    webpages = None

    def __init__(self):
        pass

    def generate_page(self, seed):
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
        requester_ip = environ.get('REMOTE_ADDR', 'Unknown IP')
        user_agent = environ.get('HTTP_USER_AGENT', 'Unknown Agent')
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"{current_time}, {requester_ip}, {user_agent}")
        
        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        start_response(status, headers)
        return [self.generate_page(environ.get('PATH_INFO', '')).encode()]

app = SpiderTrapApp()
if len(sys.argv) == 2:
    app.webpages = load_webpages(sys.argv[1])
