__author__ = 'tom caruso'

import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

streamhandler = logging.StreamHandler()
streamhandler.setLevel(logging.INFO)

streamhandler.setFormatter(formatter)

LOGGER.addHandler(streamhandler)
