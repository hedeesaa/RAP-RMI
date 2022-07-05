import Pyro4
from Core.IDirectory import IRegistry


@Pyro4.expose
class Registry(IRegistry):

    def find(self, server_id):
        for server_id in IRegistry.peers.keys():
            return IRegistry.peers[server_id]

    def list_peers(self):
        return IRegistry.peers

    def unregister(self, server_id):
        del IRegistry.peers[server_id]
        print(IRegistry.peers)

    def register(self, server_id, url):
        IRegistry.peers[server_id] = url
        print(IRegistry.peers)

    def all(self):
        return IRegistry.peers





