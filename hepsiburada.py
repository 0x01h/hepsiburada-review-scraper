#!/usr/bin/env python3

import numpy
import os
import sys
import tqdm
import urllib.request
from bs4 import BeautifulSoup
from colorama import Fore, Back
from fake_useragent import UserAgent
from multiprocessing.dummy import Pool, Semaphore
from time import sleep


def show_banner():
    print(Fore.RED + Back.BLACK + r'''
 _     ____    ____  _____ _     _  _____ _        ____  ____  ____  ____  ____  _____ ____
/ \ /|/  __\  /  __\/  __// \ |\/ \/  __// \  /|  / ___\/   _\/  __\/  _ \/  __\/  __//  __\
| |_||| | //  |  \/||  \  | | //| ||  \  | |  ||  |    \|  /  |  \/|| / \||  \/||  \  |  \/|
| | ||| |_\\  |    /|  /_ | \// | ||  /_ | |/\||  \___ ||  \_ |    /| |-|||  __/|  /_ |    /
\_/ \|\____/  \_/\_\\____\\__/  \_/\____\\_/  \|  \____/\____/\_/\_\\_/ \|\_/   \____\\_/\_\
''')


def prepare_scraping(url):

    try:
        request = urllib.request.Request(
            url,
            headers={
                'User-Agent': ua.random,
                'Accept': 'text/html'})
        response = urllib.request.urlopen(request, timeout=selected_to)

        if (response.getcode() != 200):
            return None

        else:
            content_byte = response.read()
            content = content_byte.decode('utf-8')
            scrape = BeautifulSoup(content, 'html.parser')
            return scrape

    except BaseException:
        return None


def paginate_cats(cat_url):

    pure_cat = cat_url.split('?')[0]

    if (pag_cats[pure_cat] == '1'):
        request = urllib.request.Request(
            cat_url, headers={"User-Agent": ua.random})

        try:
            response = urllib.request.urlopen(request, timeout=selected_to)

            if (response.getcode() == 200 and len(
                    response.geturl().split('?')) > 1):
                with open('categories.txt', 'a') as wFile:
                    wFile.write(cat_url + '\n')
                return

            else:
                pag_cats.update({pure_cat: '0'})
                return

        except BaseException:
            return

    else:
        return


def get_reviews(prod_page):

    scrape = prepare_scraping(prod_page)
    next_page = False
    global semaphore

    if (scrape is not None):
        reviews = scrape.find_all(attrs={"class": "review-text"})
        ratings = scrape.find_all(attrs={"class": "ratings active"})

        pagination = scrape.find(rel="next")

        if (pagination is not None):
            next_page = True
            pagination = 'https:' + str(pagination['href'])

        for i in range(0, len(reviews)):
            rating = int(ratings[i + 6]['style'][7])

            if (rating == 1):
                rating = 5
            elif (rating == 8):
                rating = 4
            elif (rating == 6):
                rating = 3
            elif (rating == 4):
                rating = 2
            elif (rating == 2):
                rating = 1
            else:
                rating = 0

            row = (
                '__label__' +
                str(rating) +
                ' ' +
                reviews[i].get_text() +
                '\n')

            semaphore.acquire()
            with open('hepsiburada.txt', 'a') as wFile:
                wFile.write(row)
            semaphore.release()

        if (next_page):
            return get_reviews(pagination)

        else:
            return

    else:
        return


def get_categories(home_url):

    categories = []

    scrape = prepare_scraping(home_url)

    if (scrape is not None):
        all_links = scrape.find_all('a')

        for get_link in all_links:
            link = str(get_link.get('href'))

            if ('-c-' in link and 'https://' not in link):
                link = 'https://www.hepsiburada.com' + link
                link = link.split('?')[0]
                categories.append(link)

            elif ('-c-' in link and 'https://www.hepsiburada.com/' in link):
                link = link.split('?')[0]
                categories.append(link)

        return categories

    else:
        print('Categories couldn\'t be scraped!')
        return None


def get_products(cat_url):

    products = []

    scrape = prepare_scraping(cat_url)

    if (scrape is not None):
        all_links = scrape.find_all('a')

        for get_link in all_links:
            link = str(get_link.get('href'))

            if ('-p-' in link and 'https://' not in link):
                link = 'https://www.hepsiburada.com' + link
                link = link.split('?')[0] + '-yorumlari'

            elif ('-p-' in link and 'https://www.hepsiburada.com/' in link):
                link = link.split('?')[0] + '-yorumlari'

            else:
                continue

            if (link not in products):
                products.append(link)

            else:
                continue

        with open('products.txt', 'a') as wFile:
            for product in products:
                wFile.write(product + '\n')

        return

    else:
        return None


if __name__ == '__main__':

    semaphore = Semaphore(3)
    show_banner()

    try:
        ua = UserAgent()
    except BaseException:
        ua = UserAgent(use_cache_server=False)

    all_categories_url = 'https://www.hepsiburada.com/tum-kategoriler'

    print(Back.RESET + Fore.BLUE + '\n' + 'Process was started successfully!')

    while True:
        try:
            auto_shutdown = input(
                Fore.GREEN +
                'Do you want to shutdown computer after finishing the job? [Y/N]: ')[0].lower()
            if (auto_shutdown == 'y' or auto_shutdown == 'n'):
                break

            elif (not isinstance(auto_shutdown, str)):
                print(Fore.RED + 'Please enter Y or N.')

            else:
                auto_shutdown == 'n'
                break

        except KeyboardInterrupt:
            sys.exit()

        except BaseException:
            pass

    while True:
        try:
            thread_num = int(
                input(
                    Fore.GREEN +
                    'Enter number of threads to work: '))
            if (thread_num < 1 or thread_num > 512):
                print(
                    Fore.RED +
                    'Number of threads have to be between 1 and 512.')

            elif (not isinstance(thread_num, int)):
                print(Fore.RED + 'Please enter an integer.')

            else:
                break

        except KeyboardInterrupt:
            sys.exit()

        except BaseException:
            pass

    while True:
        try:
            selected_to = int(
                input(
                    Fore.GREEN +
                    'Enter timeout second(s) for HTTP requests: '))
            if (selected_to < 2 or selected_to > 1024):
                print(Fore.RED + 'Timeout has to be between 2 and 1024.')

            elif (not isinstance(selected_to, int)):
                print(Fore.RED + 'Please enter an integer.')

            else:
                break

        except KeyboardInterrupt:
            sys.exit()

        except BaseException:
            pass

    print(Fore.BLUE + 'Categories are coming!')

    categories = get_categories(all_categories_url)

    categories = list(set(categories))

    print(Fore.BLUE + 'Total number of categories: ' + str(len(categories)))

    while True:
        try:
            pag_num = int(input(Fore.GREEN + 'Enter pagination depth: '))
            if (not (pag_num >= 1 and pag_num <= 999)):
                print (Fore.RED + 'Page number has to be in between 1 and 999.')

            elif (not isinstance(pag_num, int)):
                print(Fore.RED + 'Please enter an integer.')

            else:
                break

        except KeyboardInterrupt:
            sys.exit()

        except BaseException:
            pass

    print(Fore.BLUE + 'Paginating the categories!' + '\n' + Fore.RESET)

    pag_cats = {}

    for category in range(0, len(categories)):
        pag_cats.update({categories[category]: '1'})

    for category in range(0, len(categories)):
        with open('categories.txt', 'a') as wFile:
            wFile.write(categories[category] + '\n')
        for page in range(2, pag_num + 1):
            paginated = categories[category] + '?sayfa=' + str(page)
            categories.append(paginated)

    paginationWorkers = Pool(thread_num if len(
        categories) > thread_num else len(categories))

    for _ in tqdm.tqdm(paginationWorkers.imap_unordered(
            paginate_cats, categories), total=len(categories)):
        pass

    paginationWorkers.close()
    paginationWorkers.join()

    categories = None
    pag_cats = None

    with open('categories.txt') as rFile:
        categories = [line.rstrip('\n') for line in rFile]

    print(Fore.BLUE +
          '\n' +
          'Total number of paginated categories: ' +
          str(len(categories)))

    productWorkers = Pool(thread_num if len(categories) >
                          thread_num else len(categories))

    print(Fore.BLUE + 'Products are coming!' + '\n' + Fore.RESET)

    for _ in tqdm.tqdm(productWorkers.imap_unordered(
            get_products, categories), total=len(categories)):
        pass

    productWorkers.close()
    productWorkers.join()

    categories = None

    with open("products.txt") as rFile:
        products = [line.rstrip('\n') for line in rFile]

    print(Fore.BLUE +
          '\n' +
          'Total number of fetched products: ' +
          str(len(products)))

    #products = list(filter(None, products))
    #products = numpy.concatenate(products, axis=0)
    #products = products.tolist()
    #products = list(set(products))

    reviewWorkers = Pool(thread_num)

    print(Fore.BLUE + 'Preparing and exporting reviews!' + '\n' + Fore.RESET)

    for _ in tqdm.tqdm(reviewWorkers.imap_unordered(
            get_reviews, products), total=len(products)):
        pass

    reviewWorkers.close()
    reviewWorkers.join()

    products = None

    print (Fore.BLUE + '\n' + 'Process was finished successfully!' + '\n')

    if (auto_shutdown == 'y'):
        os.system('shutdown -h')
    else:
        pass
