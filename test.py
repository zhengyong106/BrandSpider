import time
from twisted.web.client import Agent
from twisted.internet import reactor, task, defer


def hello(name):
    print("Hello world!===>" + name + '===>' + str(int(time.time())))


@defer.inlineCallbacks
def request_google():
    agent = Agent(reactor)

    result = yield agent.request('GET', 'https://www.baidu.com'.encode("utf-8"))

    print(result)


reactor.callWhenRunning(hello, 'yudahai')

reactor.callLater(1, request_google)

reactor.callLater(3, hello, 'yuyue')

reactor.run()