from twisted.web.resource import Resource
from twisted.web.static import File
from twisted.web.server import Site
from twisted.internet import reactor
    
file = File('./web')
site = Site(file)
reactor.listenTCP(81,site)
print 'site is running at 81'
reactor.run()