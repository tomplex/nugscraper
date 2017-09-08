__author__ = 'tom caruso'

import click
import os

from multiprocessing.pool import ThreadPool
from threading import Lock

from nugscraper.util import download_file_with_progressbar, get_payload, get_login_session, scrape_url


def collect_user_input():
    username = os.environ.get('NUGS_USERNAME', None) or click.prompt("Enter your nugs.net username")
    password = os.environ.get('NUGS_PASSWORD', None) or click.prompt("Enter your nugs.net password", hide_input=True)

    return username, password


@click.command()
@click.option('--url', '-u', required=True, multiple=True, help="URL of 'download all' window. Can be used multiple times to scrape more than one page.")
@click.option('--dest-dir', '-d', required=True, help="Destination for downloaded files")
@click.option('--num-procs', '-n', required=False, default=3, help="Number of download processes [default: 3]")
def nugscraper(url, dest_dir, num_procs):

    login = collect_user_input()

    p = get_payload(login[0], login[1])
    try:
        session = get_login_session(p)
    except ConnectionError:
        click.echo("Unable to connect to nugs.net. Please check your login credentials.")
        exit(1)

    song_info = []
    for u in url:
        scraped_songs = scrape_url(session, u)
        for idx, (url, filename) in enumerate(scraped_songs):
            song_info.append((url, os.path.join(dest_dir,filename), idx))

    click.echo("Found {} songs.\nStarting downloads...".format(len(song_info)))

    pool = ThreadPool(num_procs)
    lock = Lock()

    for url, path, idx in song_info:
        pool.apply_async(download_file_with_progressbar, args=(url, path, idx, lock))

    pool.close()
    pool.join()
    exit(0)


if __name__ == '__main__':
    nugscraper()
