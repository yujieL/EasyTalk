#-*-coding:utf-8
from twisted.internet import reactor
from autobahn.websocket import (WebSocketServerFactory,
                                WebSocketServerProtocol,
                                listenWS)                               
import json
chatRoom = {}
AdminMsg = 'Notice:'
Header = ['status','rid','content']
STATUS = ('connect','chat','close')
class EchoServerProtocol(WebSocketServerProtocol):
    
    def generate(self,msg):
        self.msg = msg
        self.rid = msg[Header[1]]
    def onMessage(self, msg, binary):
        print msg
        msg = eval(msg)
        if msg[Header[0]] == STATUS[0]:
            self.generate(msg)
            if not chatRoom.has_key(self.rid):
                chatRoom[self.rid] =[]
            chatRoom[self.rid].append(self)
            for user in chatRoom[self.rid]:
                m = AdminMsg + msg[Header[2]] + STATUS[0]
                user.sendMessage(m,binary)
        elif msg[Header[0]] == STATUS[1]:
            room = chatRoom[self.rid]
            #potential bug
            for user in room:
                user.sendMessage(msg[Header[2]])
    def onClose(self, wasClean, code, reason):
        room = chatRoom[self.rid]
        for user in room:
            m = AdminMsg + self.msg[Header[2]] + STATUS[2]
            user.sendMessage(m)
        room.remove(self)
        if len(room) == 0:
            room.pop(self.rid)
class EchoServerFactory(WebSocketServerFactory):
    protocol = EchoServerProtocol
    
if __name__ == '__main__':
    factory = WebSocketServerFactory("ws://localhost:9000")
    factory.protocol = EchoServerProtocol
    listenWS(factory)
    print 'Server is running at 9000'
    reactor.run()
