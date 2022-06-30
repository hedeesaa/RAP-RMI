# Service Daemon
import Pyro4
# uses Registry
from Distribution.registry import Registry
import threading
import time
# Aggregation to Repository - Needs Repository


class RepositoryService:
    # RMI Responsible
    def __init__(self, server_id, repository, url_join="join.repo."):
        self.url_join = url_join
        self.url_repo = "connect.repo."
        self.id = server_id
        self.daemon_join = Pyro4.Daemon()
        self.daemon_repo = Pyro4.Daemon()
        self.repository = repository
        self.ns = Pyro4.locateNS()

    def start_demon(self):
        
        t1 = threading.Thread(target=self.start_join_daemon)
        t1.start()

        t2 = threading.Thread(target=self.start_repo_daemon)
        t2.start()

    def start_join_daemon(self):
        r_join = self.daemon_join.register(Registry)
        address_join = self.url_join + self.id
        self.ns.register(address_join, str(r_join))

        print(f'Ready to listen to {address_join}')
        self.daemon_join.requestLoop()

    def start_repo_daemon(self):
        r_repo = self.daemon_repo.register(self.repository)
        address_repo = self.url_repo + self.id
        self.ns.register(address_repo, str(r_repo))

        print(f'Ready to listen to {address_repo}')
        self.daemon_repo.requestLoop()

    def join_peer(self, peer):

        # saving itself in itself
        server = Pyro4.Proxy("PYRONAME:join.repo."+self.id)
        server.register(self.id, "connect.repo."+self.id)

        # saving itself in the peer
        if peer != self.id:
            server = Pyro4.Proxy("PYRONAME:join.repo." + peer)
            server.register(self.id, "connect.repo." + self.id)
            # saving peer in itself
            server = Pyro4.Proxy("PYRONAME:join.repo." + self.id)
            server.register(peer, "connect.repo." + peer)

        t1 = threading.Thread(target=self.getting_update())
        t1.start()

    def getting_update(self):
        while True:
            for i in Registry.peers.copy().keys():
                if self.id != i:
                    server = Pyro4.Proxy("PYRONAME:join.repo." + i)
                    a = server.list_peers()
                    set1 = set(Registry.peers.items())
                    set2 = set(a.items())
                    i_dont_have = set2 - set1
                    for j in i_dont_have:
                        server = Pyro4.Proxy("PYRONAME:join.repo." + self.id)
                        server.register(j[0], "connect.repo." + j[0])

            time.sleep(5)
