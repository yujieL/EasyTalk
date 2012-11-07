from twisted.web.resource import Resource
from twisted.web.static import File
from twisted.web.server import Site
from twisted.internet import reactor
    
file = File('./chat')
site = Site(file)
reactor.listenTCP(80,site)
print 'site is running at 80'
reactor.run()