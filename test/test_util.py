__author__ = 'tom caruso'

from nugscraper import util


def test_download_file_with_progressbar():
    pass


def test_get_payload():
    payload = util.get_payload('some_username', 'some_password')
    assert payload['ctl00$cphAuth$ctl00$frmUsername'] == 'some_username'
    assert payload['ctl00$cphAuth$ctl00$frmPassword'] == 'some_password'


def test_get_login_session():
    pass


def test_scrape_url():
    pass


def test_scrape_for_song_links():
    pass


def test_get_nugs_queue_link():
    pass