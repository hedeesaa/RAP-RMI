import Pyro4
from Core.connector import Connector
import sys
import threading
import dill
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
        try:
            command = input("... ")
            if command.upper() == "FINISH":
                break

            connector = Connector()
            command = connector.examine(command, server_name_)
            ns = server_name_

            match command[0]:
                case "SET":
                    _, value = command[1].set_variable(command[2], command[3])
                    print(value)

                case "ADD":
                    _, value = command[1].add_variable(command[2], command[3])
                    print(value)

                case "GET":
                    _, value = command[1].get_value(command[2])
                    print(value)

                case "GET_VALUES":
                    _, value = command[1].get_values(command[2])
                    print(value)

                case "DELETE":
                    _, value = command[1].delete_variable(command[2])
                    print(value)

                case "LIST":
                    _, value = command[1].list_keys()
                    print(value)

                case "SUM":
                    _, value = command[1].sum(command[2])
                    print(value)

                case "RESET":
                    _, value = command[1].reset()
                    print(value)

                case "DSUM":
                    summ = 0
                    ss = True
                    for i in command[1]:

                        server = bring_up_server([], i)
                        err, value = server.aggregate(command[1])
                        if err:
                            ss = False
                            break
                        else:
                            cls = dill.loads(value)
                            e, v = cls.sum(command[-1])
                            if e:
                                print(v)
                                ss = False
                                break
                            summ += v
                    if ss:
                        print(summ)

                case "ENUM_KEYS":
                    server = bring_up_server(command[1], ns)
                    server.enum_keys(enum_controller())

                case "ENUM_VALUES":
                    server = bring_up_server(command[1], ns)
                    server.enum_values(command[2], enum_controller())
        
        except Pyro4.errors.NamingError:
            print("Server Is Not Available")


def enum_controller():
    Pyro4.config.SERIALIZERS_ACCEPTED.add('dill')
    daemon = Pyro4.core.Daemon()
    callback = CallbackHandler()
    daemon.register(callback)
    t1 = threading.Thread(target=daemon.requestLoop)
    t1.start()
    return callback


def bring_up_server(command_, ns):
    if command_:
        ns = command_[0]
    Pyro4.config.SERIALIZER = 'dill'
    return Pyro4.Proxy("PYRONAME:" + URL + ns)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        server_name = sys.argv[1]
        connect_to_server(server_name)
    else:
        print("Not Valid Command - client [server_name]")
        exit()
