from abc import ABC, abstractmethod

class IServer(ABC):

    @abstractmethod
    def send(self, data):
        pass

    def send_current_time(self, data):
        pass

    @abstractmethod
    def read_start_motors(self):
        pass
