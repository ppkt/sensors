__author__ = 'ppkt'

from pymongo import MongoClient
from twisted.python import log

import ConfigParser

class Database(object):
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('config.ini')

        self._hostname = config.get('Database', 'hostname')
        self._port = config.getint('Database', 'port')
        self._username = config.get('Database', 'username')
        self._password = config.get('Database', 'password')

    def connect(self):
        log.msg('Connecting to database')
        self._client = MongoClient(self._hostname, self._port)
        self._db = self._client.mo13594_sensors
        self._db.authenticate(self._username, self._password)

        self._temperatures = self._db.temperatures
        log.msg('Successful')

    @property
    def temperatures(self):
        return self._temperatures
