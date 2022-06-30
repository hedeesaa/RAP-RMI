from Core.IRepository import IDistributedRepository
import Pyro4


@Pyro4.expose
class Repository(IDistributedRepository):

    def set_variable(self, variable: str, value: int):
        IDistributedRepository.repo[variable] = [value]
        # Error, Response
        print(IDistributedRepository.repo)
        return False, "OK"

    def add_variable(self, variable: str, value: int):
        error = False
        res = "OK"
        try:
            IDistributedRepository.repo[variable].append(value)
        except:
            error = True
            res = "Variable Does Not Exist"
        print(IDistributedRepository.repo)
        return error, res

    def get_value(self, variable):
        error = False
        try:
            value = IDistributedRepository.repo[variable][0]
        except:
            value = "Variable Does Not Exist"
            error = True

        return error, value

    def get_values(self, variable):
        error = False
        try:
            value = IDistributedRepository.repo[variable]
        except:
            value = 0
            error = True

        return error, value

    def delete_variable(self, variable: str) -> bool:
        error = False
        try:
            del IDistributedRepository.repo[variable]
        except:
            error = True
        print(IDistributedRepository.repo)
        return error, "OK"
    
    def list_keys(self):
        list_repo = list(IDistributedRepository.repo.keys())
        return False, ", ".join(list_repo)

    def sum(self, variable: str):
        error = False
        try:
            value = sum(IDistributedRepository.repo[variable])
        except:
            value = 0
            error = True
        return error, value

    def reset(self):
        IDistributedRepository.repo = {}
        return False, "OK"

    def aggregate(self, peer_list): pass
        # for peer in peer_list:




