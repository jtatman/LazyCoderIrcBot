#!/usr/bin/env python3

import sys
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor
from twisted.python import log
from stathat import StatHat

class MessageLogger:
    def __init__(self, file):
        self.file = file

    def log(self, message):
        #timestamp = time.srtftime("[%H:%M:%S]", time.localtime(time.time()))
        now = datetime.now()
        timestamp = bytes(int(datetime.timestamp(now)))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()

class MyBot(irc.IRCClient):
    #def _get_nickname(self):
    #    return self.factory.nickname
    #nickname = property(_get_nickname)
    #print(nickname)
    nickname = "jtlazybot"

    def signedOn(self):
        self.join(self.factory.channel, self.factory.channel_key)
        print(("Signed on as {}.".format(self.nickname)))

    def joined(self, channel):
        print(("Joined %s." % channel))

    def privmsg(self, user, channel, msg):
        """
        Whenever someone says "why" give a lazy programmer response
        """
        # doesn't work to parse multiple options for some reason
        # needs reworking
        if ('why' or 'wtf' or 'whatever') in msg.lower():
            # get lazy response
            because = self._get_because()
            # post message
            self.msg(self.factory.channel, str(because.decode()))

    def _get_because(self):
        req = requests.get('http://developerexcuses.com/')
        soup = BeautifulSoup(req.text, features="html.parser")
        elem = soup.find('a')
        print(elem.text)
        return elem.text.encode('ascii', 'ignore')
        #return bytes(elem)
        #return str(elem.decompose())

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))


    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^_^'

class MyBotFactory(protocol.ClientFactory):
    #protocol = MyBot

    def __init__(self, nickname, channel, channel_key=None):
        self.nickname = nickname
        self.channel = channel
        self.channel_key = channel_key

    def buildProtocol(self, addr):
        p = MyBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        print(("Lost connection (%s), reconnecting." % reason))
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print(("Could not connect: %s" % reason))
        reactor.stop()

if __name__ == "__main__":
    # init logging
    # msglog = MessageLogger("test.log")
    log.startLogging(sys.stdout)

    print(len(sys.argv))
    if len(sys.argv) == 1:
        reactor.connectTCP('irc.freenode.net', 6667, MyBotFactory( nickname='jtlazybot', channel='#jimtron', channel_key='' ))
        reactor.run()
    elif len(sys.argv) == 4:
        nick = sys.argv[1]
        channel = sys.argv[2]
        chan_key = None
        chan_key = sys.argv[3]
        reactor.connectTCP('chat.freenode.net', 6667, MyBotFactory( nickname=nick, channel=channel, channel_key=chan_key ))
        reactor.run()
#        elif len(sys.argv) == 5:
#            chan_key = sys.argv[3]
#            server = sys.argv[4]
#            reactor.connectTCP(server, 6667, MyBotFactory( nickname=nick, channel=channel, channel_key=chan_key ))
#        elif len(sys.argv) == 6:
#            chan_key = sys.argv[3]
#            server = sys.argv[4]
#            port = sys.argv[5]
#            reactor.connectTCP(server, port, MyBotFactory( nickname=nick, channel=channel, channel_key=chan_key ))
