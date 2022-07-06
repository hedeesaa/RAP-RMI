from Core.RepException import *
import Pyro4
from Core.ICallback import ICallback
import threading
import dill

class Connector():
    COMMANDS_LIST = ["ENUM_VALUES",
                     "ENUM_KEYS",
                     "RESET",
                     "SUM",
                     "GET_VALUES",
                     "LIST",
                     "GET",
                     "DELETE",
                     "ADD",
                     "SET",
                     "DSUM",
                     "FINISH"]

    URL = "connect.repo."

    def examine(self, msg,ns):
        result = self.__check_input(msg)
        if result:
            command = msg.split()

            # SET
            if command[0].upper() == "SET":
                dst, var = self.__break_command(command)
                server = self.__bring_up_server(dst, ns)
                return "SET", server, var, int(command[-1])

            # ADD
            if command[0].upper() == "ADD":
                dst, var = self.__break_command(command)
                server = self.__bring_up_server(dst, ns)
                return "ADD", server, var, int(command[-1])

            # GET
            if command[0].upper() == "GET":
                dst, var = self.__break_command(command)
                server = self.__bring_up_server(dst, ns)
                return "GET", server, var

            # GET_VALUES
            if command[0].upper() == "GET_VALUES":
                dst, var = self.__break_command(command)
                server = self.__bring_up_server(dst, ns)
                return "GET_VALUES", server, var

            # DELETE
            if command[0].upper() == "DELETE":
                dst, var = self.__break_command(command)
                server = self.__bring_up_server(dst, ns)
                return "DELETE", server, var

            # LIST KEYS
            if command[0].upper() == "LIST":
                server = self.__bring_up_server(self.__able_no_arg(command), ns)
                return "LIST", server

            # SUM
            if command[0].upper() == "SUM":
                dst, var = self.__break_command(command)
                server = self.__bring_up_server(dst, ns)
                return "SUM", server, var

            # RESET
            if command[0].upper() == "RESET":
                server = self.__bring_up_server(self.__able_no_arg(command), ns)
                return "RESET", server

            # DSUM
            if command[0].upper() == "DSUM":
                var = command[1]
                dst = command[3:]
                return "DSUM", dst, var

            # ENUM_KEYS
            if command[0].upper() == "ENUM_KEYS":
                return "ENUM_KEYS", self.__bring_up_server(self.__able_no_arg(command), ns)

            # ENUM_VALUES
            if command[0].upper() == "ENUM_VALUES":
                dst, var = self.__break_command(command)
                server = self.__bring_up_server(dst, ns)
                return "ENUM_VALUES", server, var
            
            if command[0].upper() == "FINISH":
                return "FINISH", False

    def __check_input(self, msg):
        """
        Checks Message Input of a User
        Returns True or False
        """
        if isinstance(msg, str):
            command = msg.split()[0].upper()
            if command in Connector.COMMANDS_LIST:
                return True
        raise CommandIsNotValid

    def __break_command(self, msg):
        var = msg[1]
        dst = []
        if "." in msg[1]:
            var_and_dst = msg[1].split(".")
            dst.append(var_and_dst[0])
            var = var_and_dst[1]
        return dst, var

    def __able_no_arg(self, msg):
        dst = []
        if len(msg) == 2:
            dst = [msg[1]]
        return dst

    def __bring_up_server(self, command_, ns):
        if command_:
            ns = command_[0]
        Pyro4.config.SERIALIZER = 'dill'
        return Pyro4.Proxy("PYRONAME:" + Connector.URL + ns)

    def enum_controller(self):
        Pyro4.config.SERIALIZERS_ACCEPTED.add('dill')
        daemon = Pyro4.core.Daemon()
        callback = CallbackHandler()
        daemon.register(callback)
        t1 = threading.Thread(target=daemon.requestLoop)
        t1.start()
        return callback

    def commander(self,command):
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

                    Pyro4.config.SERIALIZER = 'dill'
                    server = Pyro4.Proxy("PYRONAME:" + Connector.URL + i)
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
                command[1].enum_keys(self.enum_controller())

            case "ENUM_VALUES":
                command[1].enum_values(command[2], self.enum_controller())

            case "FINISH":
                return True


@Pyro4.expose
class CallbackHandler(ICallback):

    @Pyro4.callback
    def call(self, err, repo):
        if not err:
            print(list(enumerate(repo)))
        else:
            print("Not Existed!")
