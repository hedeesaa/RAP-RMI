from Core.RepException import *
import Pyro4


class Connector:
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
                     "DSUM"]

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
                return "ENUM_KEYS", self.__able_no_arg(command)

            # ENUM_VALUES
            if command[0].upper() == "ENUM_VALUES":
                dst, var = self.__break_command(command)
                return "ENUM_VALUES", dst, var

    def __check_input(self, msg):
        """
        Checks Message Input of a User
        Returns True or False
        """
        if isinstance(msg, str):
            command = msg.split()[0].upper()
            if command in Connector.COMMANDS_LIST:
                return True
        # return False
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



