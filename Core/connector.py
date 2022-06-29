class Connector:
    COMMANDS_LIST = ["FINISH", "RESET", "SUM", "GET_VALUES", "LIST", "GET", "DELETE", "ADD", "SET", "DSUM"]

    def get_command(self, msg):
        command_list = msg.split()
        if command_list[0].upper() == "SET":
            return "SET", command_list[1], int(command_list[2])
        if command_list[0].upper() == "GET":
            return "GET", command_list[1]
        if command_list[0].upper() == "ADD":
            return "ADD", command_list[1], int(command_list[2])
        if command_list[0].upper() == "GET_VALUES":
            return "GET_VALUES", command_list[1]




