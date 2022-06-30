import Pyro4
import threading
URL = "connect.repo."

@Pyro4.expose
class CallbackHandler(object):

    @Pyro4.callback
    def call1(self):
        print("callback 1 received from server!")
        print("going to crash - you won't see the exception here, only on the server")
        # return self.crash()


daemon = Pyro4.core.Daemon()
callback = CallbackHandler()
daemon.register(callback)
server = Pyro4.Proxy(f"PYRONAME:"+URL+"r1")
server._pyroOneway.add("doCallback")
_, value = server.set_variable("a", 2)
print(value)
t1 = threading.Thread(target=daemon.requestLoop)
t1.start()
_, value = server.set_variable("b", 2)
print(value)
# daemon.requestLoop()
# print("hey")
server.doCallback(callback)
# t1 = threading.Thread(target=)
# t1.start()


