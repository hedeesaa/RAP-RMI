import rap_model
import Pyro4

@Pyro4.expose
class RAP(object):
    ERROR_VARIABLE_NOT_EXIST = "[ERROR]: This Variable is not existed!"
    URL = "repository.server."
    repo = {}

    # def __init__(self):
    #     self.repo = {}

    def set_variable(self,variable,value):
        error, RAP.repo=rap_model.set_variable(variable, value,RAP.repo)
        if error == False:
            return "OK"
        return "[ERROR]: SET variable value"
    def add_variable(self,variable,value):
        error, RAP.repo=rap_model.add_to_variable(variable, value,RAP.repo)
        if error:
            return RAP.ERROR_VARIABLE_NOT_EXIST
        return "OK"

    def get_variable(self,variable):
        error, value = rap_model.get_value(variable,RAP.repo)
        if error:
            return RAP.ERROR_VARIABLE_NOT_EXIST
        return str(value)

    def dsum(self, variable, peer_list):
        sums = []
        for peer in peer_list:
            address = self.URL+peer
            server = Pyro4.Proxy(f"PYRONAME:{address}")
            ee = server.sum(variable)
            sums.append(int(ee))

        return sum(sums)

    def sum(self,variable):
        error, value = rap_model.sum_of_variable(variable,RAP.repo)
        
        if error:
            return RAP.ERROR_VARIABLE_NOT_EXIST
        return value