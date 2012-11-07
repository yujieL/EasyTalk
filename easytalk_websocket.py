#-*-coding:utf-8
from twisted.internet import reactor
from autobahn.websocket import (WebSocketServerFactory,
                                WebSocketServerProtocol,
                                listenWS)                               
import json
chatRoom = {}
AdminMsg = 'Notice:'
NameList = 'NameList'
Header = ['status','rid','content']
STATUS = ('connect','chat','close')
class EchoServerProtocol(WebSocketServerProtocol):
    
    def generate(self,msg):
        self.msg = msg
        self.rid = msg[Header[1]]
    def onMessage(self, msg, binary):
        #print msg
        msg = eval(msg)
        if msg[Header[0]] == STATUS[0]:#connect
            self.generate(msg)
            if not chatRoom.has_key(self.rid):
                chatRoom[self.rid] =[]
            chatRoom[self.rid].append(self)
            userList = [NameList]
            for user in chatRoom[self.rid]:
                m = AdminMsg + msg[Header[2]] + STATUS[0]
                user.sendMessage(m,binary)
                userList.append(user.msg[Header[2]].split('\t')[0])
            for user in chatRoom[self.rid]:
                user.sendMessage(str(userList),binary)
        elif msg[Header[0]] == STATUS[1]:#chat
            room = chatRoom[self.rid]
            #potential bug
            for user in room:
                user.sendMessage(msg[Header[2]])
    def onClose(self, wasClean, code, reason):
        #close
        room = chatRoom[self.rid]
        userList = [NameList]
        for user in room:
            m = AdminMsg + self.msg[Header[2]] + STATUS[2]
            user.sendMessage(m)
            userList.append(user.msg[Header[2]].split('\t')[0])
        rid = self.rid
        room.remove(self)
        if len(room) == 0:
            chatRoom.pop(rid)
        else:
            for user in chatRoom[rid]:
                user.sendMessage(str(userList))            
class EchoServerFactory(WebSocketServerFactory):
    protocol = EchoServerProtocol
    
if __name__ == '__main__':
    factory = WebSocketServerFactory("ws://localhost:9000")
    factory.protocol = EchoServerProtocol
    listenWS(factory)
    print 'Server is running at 9000'
    reactor.run()
