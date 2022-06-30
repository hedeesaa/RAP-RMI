# Service Daemon
import Pyro4
from Distribution.registry import Registry
import threading
import time


class RepositoryService:
    # RMI Responsible
    URL_JOIN = "join.repo."
    URL_REPO = "connect.repo."

    def __init__(self, server_id, repository):
        self.id = server_id
        self.daemon_join = Pyro4.Daemon()
        self.daemon_repo = Pyro4.Daemon()
        self.repository = repository
        self.ns = Pyro4.locateNS()

    def start_daemon(self):
        
        t1 = threading.Thread(target=self.start_join_daemon)
        t1.start()

        t2 = threading.Thread(target=self.start_repo_daemon)
        t2.start()

    def start_join_daemon(self):
        r_join = self.daemon_join.register(Registry)
        address_join = RepositoryService.URL_JOIN + self.id
        self.ns.register(address_join, str(r_join))

        print(f'Listening to {address_join} ...')
        self.daemon_join.requestLoop()

    def start_repo_daemon(self):
        r_repo = self.daemon_repo.register(self.repository)
        address_repo = RepositoryService.URL_REPO + self.id
        self.ns.register(address_repo, str(r_repo))

        print(f'Listening to {address_repo} ...')
        self.daemon_repo.requestLoop()

    def join_peer_startup(self, peer):
        if peer != self.id:
            try:
                # saving itself in the peer
                self.__join_helper(peer, self.id)
            except:
                print(f"Peer {peer} Does Not Respond")
                exit()

    def join_peer(self, peer):
        # saving itself in itself
        self.__join_helper(self.id, self.id)

        if peer != self.id:
            # saving peer in itself
            self.__join_helper(self.id, peer)

        t1 = threading.Thread(target=self.getting_update())
        t1.start()

    def __join_helper(self, dst, info):
        print(f"dest: {dst}, info: {info}")
        server = Pyro4.Proxy("PYRONAME:"+RepositoryService.URL_JOIN + dst)
        server.register(info, RepositoryService.URL_REPO + info)

    def __remove_helper(self, info):
        server = Pyro4.Proxy("PYRONAME:" + RepositoryService.URL_JOIN + self.id)
        server.unregister(info)

    def getting_update(self):
        while True:
            for peer in Registry.peers.copy().keys():
                if self.id != peer:
                    server = Pyro4.Proxy("PYRONAME:" + RepositoryService.URL_JOIN + peer)
                    try:
                        neighbors = set(server.list_peers().items()) - set(Registry.peers.items())
                        for neigh in neighbors:
                            self.__join_helper(self.id, neigh[0])
                    except:
                        print(f"Peer {peer} Does Not Respond")
                        self.__remove_helper(peer)
            time.sleep(5)
