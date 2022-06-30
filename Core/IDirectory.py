from abc import ABC, abstractmethod


class IDirectory(ABC):
    peers = {}

    @abstractmethod
    def find(self, server_id: str): pass

    @abstractmethod
    def list_peers(self) -> list: pass


class IRegistry(IDirectory):

    @abstractmethod
    def find(self, server_id: str): pass

    @abstractmethod
    def list_peers(self) -> list: pass

    @abstractmethod
    def register(self, server_id: str, url: str): pass

    @abstractmethod
    def unregister(self, server_id: str): pass
    