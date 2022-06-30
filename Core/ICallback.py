from abc import ABC, abstractmethod


class ICallback(ABC):
    @abstractmethod
    def call(self): pass
