from abc import ABC, abstractmethod


class ICallback(ABC):
    def call1(self):
        print("hey")
