from ServiceDaemon.repositoryService import RepositoryService
from RegistryImplemention.repository import Repository
import sys

# TODO: Handle if peers are not here
# TODO: DO unregister when the server is going down
# TODO: DO Unregister when it is not resppnding anymore
# TODO: Do Enumeration

def start_server(server_name_, known_registry_):
    rs = RepositoryService(server_name_, Repository)
    rs.start_demon()
    rs.join_peer(known_registry_)


if __name__ == "__main__":
    server_name = sys.argv[1]
    known_registry = sys.argv[1]
    if len(sys.argv) == 3:
        # It has known registry
        known_registry = sys.argv[2]

    start_server(server_name, known_registry)

