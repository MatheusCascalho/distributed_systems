from abc import ABC, abstractmethod

class IServer(ABC):

    @abstractmethod
    def send(self, data):
        pass
