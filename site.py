from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import reactor

filename = 'client.html'
class myResoure(Resource):
    isLeaf = True
    def render(self,request):
        return open(filename).read()

site = Site(myResoure())
reactor.listenTCP(81,site)
print 'site is running at 81'
reactor.run()