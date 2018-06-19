import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

# 'ynet'
PROJECT_NAME = 'efrwgrgergee'
# 'https://ynet.com'
HOME_PAGE = 'dfmff'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
# Can change...
NUMBER_OF_THREADS = 8
queue = Queue()

Spider(PROJECT_NAME, HOME_PAGE, DOMAIN_NAME)


# do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# create threads (die when finished)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# each queue link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# crawl links in the queue
def crawl():
    queue_links = file_to_set(QUEUE_FILE)
    if len(queue_links) > 0:
        print(str(len(queue_links)) + 'links in the queue')
        create_jobs()


create_workers()
crawl()