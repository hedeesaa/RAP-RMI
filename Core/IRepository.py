from abc import ABC, abstractmethod
from Core.IDirectory import IDirectory
from Core.ICallback import ICallback


class IAggregate(ABC):
    @abstractmethod
    def sum(self, variable: str) -> int: pass


class IRepository(IAggregate):
    repo = {}

    # IAggregate Interface Method
    @abstractmethod
    def sum(self, variable: str) -> int: pass

    @abstractmethod
    def set_variable(self, variable: str, value: int): pass

    @abstractmethod
    def add_variable(self, variable: str, value: int): pass

    @abstractmethod
    def delete_variable(self, variable: str) -> bool: pass

    @abstractmethod
    def list_keys(self): pass

    @abstractmethod
    def get_value(self, variable: str): pass

    @abstractmethod
    def get_values(self, variable: str): pass

    @abstractmethod
    def reset(self): pass
        

class IDistributedRepository(IRepository):
    peers = IDirectory.peers
    @abstractmethod
    def sum(self, variable: str) -> int: pass

    @abstractmethod
    def set_variable(self, variable: str, value: int): pass

    @abstractmethod
    def add_variable(self, variable: str, value: int): pass

    @abstractmethod
    def delete_variable(self, variable: str) -> bool: pass

    @abstractmethod
    def list_keys(self): pass

    @abstractmethod
    def get_value(self, variable: str): pass

    @abstractmethod
    def get_values(self, variable: str): pass

    @abstractmethod
    def reset(self): pass

    @abstractmethod
    def aggregate(self, peer_list) -> IAggregate: pass

    @abstractmethod
    def enum_keys(self, callback: ICallback): pass

    @abstractmethod
    def enum_values(self, variable, callback: ICallback): pass


    