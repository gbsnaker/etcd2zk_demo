from twisted.internet.task import react
from twisted.internet.defer import inlineCallbacks

import txaio
from txaioetcd import Client, KeySet

@inlineCallbacks
def main(reactor):
    etcd = Client(reactor, u'http://192.168.0.172:2379')

    status = yield etcd.status()
    print(status)

    # insert one of the snippets below HERE

if __name__ == '__main__':
    txaio.start_logging(level='debug')
    react(main)