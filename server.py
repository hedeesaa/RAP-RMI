from ServiceDaemon.repositoryService import RepositoryService
from RegistryImplemention.repository import Repository
import sys


def start_server(server_name_, known_registry_):
    rs = RepositoryService(server_name_, Repository)
    # Join to peer which was defined at startup
    rs.join_peer_startup(known_registry_)

    rs.start_daemon()
    rs.join_peer(known_registry_)


if __name__ == "__main__":
    server_name = sys.argv[1]
    known_registry = sys.argv[1]
    if len(sys.argv) == 3:
        # It has known registry
        known_registry = sys.argv[2]

    start_server(server_name, known_registry)

