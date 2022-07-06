import Pyro4
from Core.connector import Connector
import sys


def connect_to_server(server_name_):

    while True:
        try:
            command = input("... ")
            connector = Connector()
            command = connector.examine(command, server_name_)
            if connector.commander(command):
                break

        except Pyro4.errors.NamingError:
            print("Server Is Not Available")
            

if __name__ == "__main__":
    if len(sys.argv) == 2:
        server_name = sys.argv[1]
        connect_to_server(server_name)
    else:
        print("Not Valid Command - client [server_name]")
        exit()
