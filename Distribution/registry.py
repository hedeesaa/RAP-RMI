import Pyro4
from Core.IDirectory import IRegistry
from Core.IRepository import IRepository


@Pyro4.expose
class Registry(IRegistry):

    def find(self, server_id: str) -> IRepository:
        pass

    def list_peers(self) -> list:
        return IRegistry.peers

    def unregister(self, server_id: str):
        del IRegistry.peers[server_id]

    def register(self, server_id, url):

        IRegistry.peers[server_id] = url
        print(IRegistry.peers)






