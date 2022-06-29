import Pyro4
from Core.connector import Connector

# Just need to send to r1 directly - Done
while True:
    server = Pyro4.Proxy("PYRONAME:connect.repo.r3")
    command = input("...")
    if command.upper() == "FINISH":
        break

    cc = Connector()
    command = cc.get_command(command)
    if command[0] == "SET":
        server.set_variable(command[1], command[2])
    elif command[0] == "GET":
        print(server.get_value(command[1]))
    elif command[0] == "ADD":
        server.add_variable(command[1], command[2])
    elif command[0] == "GET_VALUES":
        print(server.get_values(command[1]))
