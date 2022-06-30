import Pyro4
from Core.connector import Connector
import sys
import threading
URL = "connect.repo."


@Pyro4.expose
class CallbackHandler(object):

    @Pyro4.callback
    def call(self, err, repo):
        if not err:
            print(list(enumerate(repo)))
        else:
            print("Not Existed!")


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
                _, value = server.aggregate(command[-1], command[1])
                print(value)

            case "ENUM_KEYS":
                server = bring_up_server(command[1], ns)
                server.enum_keys(enum_controller())

            case "ENUM_VALUES":
                server = bring_up_server(command[1], ns)
                server.enum_values(command[2], enum_controller())

def enum_controller():
    daemon = Pyro4.core.Daemon()
    callback = CallbackHandler()
    daemon.register(callback)
    t1 = threading.Thread(target=daemon.requestLoop)
    t1.start()
    return callback


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
