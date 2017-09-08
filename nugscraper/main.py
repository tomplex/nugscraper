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

    scraped_songs = scrape_url(session, url)

    song_info = [(url, os.path.join(dest_dir,filename), idx) for idx, (url, filename) in enumerate(scraped_songs)]
    # song_info = [(url, path, idx) for idx, (url, path) in enumerate(zip(links, paths))]

    pool = ThreadPool(num_procs)
    lock = Lock()

    for url, path, idx in song_info:
        pool.apply_async(download_file_with_progressbar, args=(url, path, idx, lock))
    pool.close()
    pool.join()


def scratch():
    pass
    # links = ['http://ipv4.download.thinkbroadband.com/5MB.zip',
    #          'http://ipv4.download.thinkbroadband.com/20MB.zip',
    #          'http://ipv4.download.thinkbroadband.com/5MB.zip',
    #          'http://ipv4.download.thinkbroadband.com/20MB.zip',
    #          'http://ipv4.download.thinkbroadband.com/5MB.zip'
    #          ]
    # paths = [
    #     '/tmp/5mb1',
    #     '/tmp/20mb1',
    #     '/tmp/5mb2',
    #     '/tmp/20mb2',
    #     '/tmp/5mb3',
    # ]
    # def main():
    #
    #     all_songs = []
    #
    #     for a in soup.findAll('a'):
    #         match = song_title.findall(str(a))
    #         if match:
    #             title = match[0][3]
    #             date = match[0][0]
    #             disc_num = match[0][1]
    #             song_num = match[0][2]
    #             date = '20' + date
    #
    #             title = disc_num + song_num + '_' + title
    #
    #             link = a.get('href')
    #             all_songs.append(
    #                 {
    #                     'title' : title,
    #                     'date'  : date,
    #                     'link'  : link
    #                 }
    #             )
    #
    #     with open('/home/tom/Music/aqueous_links.json', 'w') as f:
    #         json.dump(all_songs, f)
    #
    #     for song in all_songs:
    #         song_folder = os.path.join('/home/tom/Music/Aqueous/', song['date'])
    #         try:
    #             os.mkdir(song_folder)
    #         except:
    #             pass
    #         song_path = os.path.join(song_folder, song['title'])
    #         download_file(song['link'], song_path)
    #         print("downloaded {} to {}".format(song['title'], song_folder))



if __name__ == '__main__':
    nugscraper()
