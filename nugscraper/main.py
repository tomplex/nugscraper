__author__ = 'tom caruso'

import click

from prompt_toolkit import prompt

from nugscraper.util import download_file, payload, login_info

dl_link = 'http://nugs.net/bigriver/choose_files.aspx?show=17581&codec=MP3&mediaID=368012'
queue_link = "http://nugs.net/bigriver/queue.aspx?show=17581&codec=MP3&mediaID=368012"


@click.command()
@click.option('--url', '-u', required=True, help="URL of 'download all' window")
@click.option('--dest-dir', '-d', required=True, help="Destination for downloaded files")
def nugscraper(url, dest_dir):
    login_info = collect_user_input()
    print(url)
    print(dest_dir)


def collect_user_input():
    """
    Get the username/password
    :return:
    """
    username = prompt("Enter your nugs.net account email: ")
    password = prompt("Enter your nugs.net account password: ", is_password=True)

    return login_info(username=username, password=password)



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


