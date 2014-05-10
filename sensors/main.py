#!/usr/bin/env python

from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol, Factory
from twisted.python import log
from twisted.web import server, resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import reactor
from twisted.web.resource import Resource
import sys
import json

from database import Database

class TemperatureSaver(DatagramProtocol):
    def __init__(self):
        log.msg("Connecting DB")
        self.db = Database()
        self.db.connect()
        log.msg("Database connected")

    def startProtocol(self):
        "Called when transport is connected"
        pass

    def stopProtocol(self):
        "Called after all transport is teared down"

    def datagramReceived(self, datagram, addr):
        data = json.loads(datagram.strip())
        self.db.temperatures.save(data)
        log.msg("%s\t%s" % (data, addr))


class TemperatureFetcher(Resource):
    isLeaf = True

    def getChild(self, name, request):
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        log.msg("[Temperature]: %s" % request.args)
        return "<html>Hello, world!\n%s\n%s</html>" % (request.uri, request.args)

log.startLogging(sys.stdout)

# Webservice for fetching sensors reading from DB
root = resource.Resource()
site = server.Site(root)
root.putChild('temperature', TemperatureFetcher())

# Service for saving readings to DB
protocol = TemperatureSaver()

reactor.listenMulticast(9891, protocol, listenMultiple=True)
reactor.listenTCP(8080, site)
reactor.run()
