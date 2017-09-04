from bs4 import BeautifulSoup
import re
import sys
import json
import os
import subprocess

from nugscraper.util import download_file
from nugscraper.helpers import payload


song_title = re.compile(r'aqueous(\d\d\d\d\d\d)d(\d)_(\d\d)_(\w+.mp3)')

dl_link = 'http://nugs.net/bigriver/choose_files.aspx?show=17581&codec=MP3&mediaID=368012'


def main():

    
    all_songs = []

    for a in soup.findAll('a'):
        match = song_title.findall(str(a))
        if match:
            title = match[0][3] 
            date = match[0][0]
            disc_num = match[0][1]
            song_num = match[0][2]
            date = '20' + date

            title = disc_num + song_num + '_' + title

            link = a.get('href')
            all_songs.append(
                { 
                    'title' : title,
                    'date'  : date,
                    'link'  : link
                }   
            )

    with open('/home/tom/Music/aqueous_links.json', 'w') as f:
        json.dump(all_songs, f)

    for song in all_songs:
        song_folder = os.path.join('/home/tom/Music/Aqueous/', song['date'])
        try:
            os.mkdir(song_folder)
        except:
            pass
        song_path = os.path.join(song_folder, song['title'])
        download_file(song['link'], song_path)
        print(f"downloaded {song['title']} to {song_folder}")



if __name__ == '__main__':
    main()


