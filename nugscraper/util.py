__author__ = 'tom caruso'

import re
import requests

from bs4 import BeautifulSoup as Soup
from pathlib import Path
from tqdm import tqdm

# regex to get file name from URL
FILE_NAME = re.compile('/([\w\d]+\.mp3)')
# Login link
NUGS_LOGIN_LINK = "https://nugs.net/login.aspx?rdto=redirToCatalog.aspx&rdtoParams=goto,rto&rdtoParamValues=csite,default.aspx"


def download_file_with_progressbar(url, file_path, n, lock):

    r = requests.get(url, stream=True)
    full_size = r.headers['content-length']

    path = Path(file_path)
    file_name = path.name
    parent_path = path.parent

    if not parent_path.exists():
        parent_path.mkdir()

    with open(file_path, 'wb') as f:
        with lock:
            progress = tqdm(total=int(full_size), desc=file_name, position=(1+n)*2, unit='bytes', unit_scale=True)
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                with lock:
                    progress.update(1024)
        with lock:
            progress.close()


def get_payload(username, password):
    return {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': 'f2MQGv7IXJU0jVWy683f42IRx/B5AKQ7C+kPjnN25bwhoZJ4s+oFVzpwLjhlaTnjSUPvf4+vSjKH1hIPpK3KfroRncVgugkzaJkYYAXQ8Y67qt3q7PhUhP/ZZY0Yrq3yzV0vkhsLpdfHzpeikwEA616vslJCE8M+ZUqMlNf2walY7L5fBNp6gjZdApMiLeUb7boyYH5Tbq/VK8XBnmsY/0v7MX94opVA4+5/hrKd9yRNnYHsf94dIXh2i2D4b7CgKZhp3DiiQ0TpX1mHXAQz5pulqnYhjY9eh4nT+amqZDmhew5EaKUqfLoOW4HFJoDf9g5p/U15F0tmzWuUFDheOQ3tfrpSAGvSahCiFjC5O8v9Vtd9Fpg2VVQLpt4ei++SwXI6ENCF4FA3otDKVRvfuk6NTsQTQjeNV/BqSw7Cdy5dZEezx98tqKzb7dqpPOp631uU6n+GSZ6QrX0EDS4B5NiYzT/M7Oc5yxtHJPf3zV076LSrs1ZFdq3adBh1e79yNoxIGVetozjyqT7IjVXIvHBYjMITgAUb0eQAYyNQt10d7KKycvVTQZnswDmP6sVBvwRLb80b8jXV2dT2eMwZclQDF7EgguyzLXe70FQiwIwoqJxVqQFgaXl/6bJMX+T4IyzTKBah6ulIfv186QxO6ZbK30dPCV/XCSozcYx1I1V1s4UvwRnzuY2HBHf8lrl60k2OiUJiZcupglf26yUAnDImJiRkjMZcwE6wqxj/ErIely3vG+MXw67F1YxxQfBndbL1WnqneEvWyULxpNC4Rqm5t0oKUVkFnbdUspcec9F9689rh9Q4/+1278F3kIdsqMHZm0e6BjEPyqRTdHTdnX6BYuRSaO2/PV89lcsH/+IvhLgOKxHPCM48sifTpuGOz1eZpawiDi4EacTwU9YGTwQ7kY2/khMnyWBCNRJjqe5w8am5CjuVfJEti7YZPJCw48mZapdPKxHQ+r7VP/Bcmt1Nw6tKWhGTox9qM+wSoshCieRKfJnitsL1odMBk2Dfqe4Q940ZxoepL09TPl+hscyLI39Naly4FnmobuHWGDSTwvVUMp7gTkaMsbJas+M494nsE0AtAqhHUr1txThU4YHTy4NkGnyI7jy9RnjovLLEOPnL35Kg1KRJpPRFuAnsYV5Z9rq095ecTRaW+LUqbRPqpIk6/BkHrfWyMLBKTchLFDWvDTjzJ5PfiEsKUtMhAbLbs8ktoZGrkgzb/vq7JzhltsoENDtRHtnjx2uxoV3vZGMMRfuOa81mNBzo0m9m',
        '__VIEWSTATEGENERATOR': 'C2EE9ABB',
        '__EVENTVALIDATION': 'CG4AvGVH6Z6bKkqL6oSGX6SeKdVyKeIQQc1KdkdIyKUJ3DgjJA02URNTx0gAfEJCewcEle5v8ywR3T4r7pjzBu8aNTl9p5pyJThsc96myd/rSiZVbyptjssVQIcz8bV1tQxTlApIWYx1Vt00nwqjSJ+SL1rW+riR7MUCAeYmmZee2XaAOz6Wom16iy90LeRUxSfeNhBJy6WwxmV9n9cpf+2G4nazXW/0jCs/cjS+un/5+Z/wLm0hfDHcISaZ8re2',
        'ctl00$cphAuth$ctl00$frmUsername': username,
        'ctl00$cphAuth$ctl00$frmPassword': password,
        'ctl00$cphAuth$ctl00$rdto': 'redirToCatalog.aspx',
        'ctl00$cphAuth$ctl00$rdtoParams': 'goto,rto',
        'ctl00$cphAuth$ctl00$rdtoParamValues': 'csite,default.aspx',
        'ctl00$cphAuth$ctl00$TextBox1': '',
        'ctl00$cphAuth$ctl00$btnSubmitButton': 'LOGIN'
    }


def get_login_session(payload):
    """
    Get a logged-in requests.Session() instance from a payload included the user's login info.

    :param payload: a payload object
    :return: a requests.Session() insance.
    """
    s = requests.Session()
    s.post(NUGS_LOGIN_LINK, data=payload)
    if not s.cookies:
        raise ConnectionError("Login to nugs.net failed. Check credentials.")
    return s


def scrape_url(session, url):
    queue_url = get_nugs_queue_link(url)
    resp = session.get(queue_url)
    all_songs = scrape_for_song_links(resp.content)
    return all_songs


def scrape_for_song_links(page_content):
    downloads = []
    parsed = Soup(page_content, 'html.parser')
    links = parsed.find_all('a')
    for link in links:
        url = str(link.get('href'))
        match = FILE_NAME.findall(url)
        if match:
            downloads.append((url, match[0]))
    return downloads


def get_nugs_queue_link(url):
    return url.replace('choose_files', 'queue')
