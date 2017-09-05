__author__ = 'tom caruso'

login_url = 'https://nugs.net/login.aspx?rdto=redirToCatalog.aspx&rdtoParams=goto,rto&rdtoParamValues=csite,default.aspx'


import requests
from nugscraper.util import get_login_session, payload
p = payload('carusot42@gmail.com', 'quasarnebula91')
s = get_login_session(p)


from bs4 import BeautifulSoup as Soup