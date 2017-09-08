__author__ = 'tom caruso'

import click
import os
import sys

from multiprocessing.pool import ThreadPool
from prompt_toolkit import prompt
from threading import Lock

from nugscraper.util import download_file_with_progressbar, get_payload, get_login_session, scrape_url


@click.command()
@click.option('--url', '-u', required=True, multiple=True, help="URL of 'download all' window")
@click.option('--dest-dir', '-d', required=True, help="Destination for downloaded files")
@click.option('--num-procs', '-n', required=False, default=3, help="Number of download processes [default: 3]")
def nugscraper(url, dest_dir, num_procs):
    login_info = collect_user_input()
    process(login_info, url, dest_dir, num_procs)


def collect_user_input():
    """
    Get the username/password
    :return:
    """
    username = prompt("Enter your nugs.net account email: ")
    password = prompt("Enter your nugs.net account password: ", is_password=True)

    return str(username), str(password)


def process(login_info, url, dest_dir, num_procs):
    p = get_payload(login_info[0], login_info[1])
    try:
        session = get_login_session(p)
    except ConnectionError:
        click.echo("Unable to connect to nugs.net. Please check your login credentials.")
        exit(1)

    scraped_songs = []
    [scraped_songs.extend(scrape_url(session, u)) for u in url]

    song_info = [(url, os.path.join(dest_dir, filename), idx) for idx, (url, filename) in enumerate(scraped_songs)]

    pool = ThreadPool(num_procs)
    lock = Lock()

    for url, path, idx in song_info:
        pool.apply_async(download_file_with_progressbar, args=(url, path, idx, lock))
    pool.close()
    pool.join()


if __name__ == '__main__':
    nugscraper()
