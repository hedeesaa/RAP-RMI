import Pyro4
from Core.connector import Connector
import sys

URL = "connect.repo."


def connect_to_server(server_name_):

    while True:
        command = input("... ")
        if command.upper() == "FINISH":
            break

        connector = Connector()
        command = connector.examine(command)
        ns = server_name_

        match command[0]:
            case "SET":
                server = bring_up_server(command[1], ns)
                _, value = server.set_variable(command[2], command[3])
                print(value)

            case "ADD":
                server = bring_up_server(command[1], ns)
                _, value = server.add_variable(command[2], command[3])
                print(value)

            case "GET":
                server = bring_up_server(command[1], ns)
                _, value = server.get_value(command[2])
                print(value)

            case "GET_VALUES":
                server = bring_up_server(command[1], ns)
                _, value = server.get_values(command[2])
                print(value)

            case "DELETE":
                server = bring_up_server(command[1], ns)
                _, value = server.delete_variable(command[2])
                print(value)

            case "LIST":
                server = bring_up_server(command[1], ns)
                _, value = server.list_keys()
                print(value)

            case "SUM":
                server = bring_up_server(command[1], ns)
                _, value = server.sum(command[2])
                print(value)

            case "RESET":
                server = bring_up_server(command[1], ns)
                _, value = server.reset()
                print(value)

            case "DSUM":
                server = bring_up_server([], ns)
                print(command)
                value = server.aggregate(command[-1],command[1])
                print(value)


def bring_up_server(command_, ns):
    if command_:
        ns = command_[0]
    return Pyro4.Proxy("PYRONAME:" + URL + ns)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        server_name = sys.argv[1]
        connect_to_server(server_name)
    else:
        print("Not Valid Command - client [server_name]")
        exit()
