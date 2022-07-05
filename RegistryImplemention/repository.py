from Core.IRepository import IDistributedRepository
from Core.RepException import *
import dill
import Pyro4


@Pyro4.expose
class Repository(IDistributedRepository):

    def __init__(self, id):
        self.id = id
        self.repo = IDistributedRepository.repo

    def set_variable(self, variable: str, value: int):
        IDistributedRepository.repo[variable] = [value]
        return False, "OK"

    def add_variable(self, variable: str, value: int):
        error = False
        res = "OK"
        try:
            IDistributedRepository.repo[variable].append(value)
        except:
            error = True
            res = str(VariableDoesNotExist(variable))
        return error, res

    def get_value(self, variable):
        error = False
        try:
            value = IDistributedRepository.repo[variable][0]
        except:
            value = str(VariableDoesNotExist(variable))
            error = True

        return error, value

    def get_values(self, variable):
        error = False
        try:
            value = IDistributedRepository.repo[variable]
        except:
            value = str(VariableDoesNotExist(variable))
            error = True

        return error, value

    def delete_variable(self, variable: str) -> bool:
        error = False
        res = "OK"
        try:
            del IDistributedRepository.repo[variable]
        except:
            error = True
            res = str(VariableDoesNotExist(variable))
        return error, res
    
    def list_keys(self):
        list_repo = list(IDistributedRepository.repo.keys())
        return False, ", ".join(list_repo)

    def sum(self, variable: str):
        error = False
        try:
            value = sum(self.repo[variable])
        except:
            value = str(VariableDoesNotExist(variable))
            error = True
        return error, value

    def reset(self):
        IDistributedRepository.repo = {}
        return False, "OK"

    def aggregate(self, peer_list):
        err = False
        for peer in peer_list:
            if peer == self.id:
                return err, dill.dumps(Repository(self.id))
        return True, str(RepoDoesNotExist)

    @Pyro4.callback
    def enum_keys(self, callback):
        callback.call(False, IDistributedRepository.repo.keys())

    @Pyro4.callback
    def enum_values(self, variable, callback):
        if variable not in IDistributedRepository.repo.keys():
            callback.call(True, "")
        else:
            callback.call(False, IDistributedRepository.repo[variable])






