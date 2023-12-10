from interfaces.server_interface import IServer
from opcua import Client
from process import MotorSnapshot


class MotorNotFoundError(Exception):
    def __init__(self, motor: str):
        self.message = f"{motor} not found"
        super().__init__(self.message)


class CLPCommunication(IServer):
    def __init__(self):
        self.client = Client(self.server_url)
        self.client.connect()

    @property
    def server_url(self):
        return "opc.tcp://LAPTOP-289TONJ4:53530/OPCUA/SimulationServer"

    @property
    def process_map(self):
        id_map = {
            "Motor 1": "ns=3;i=1013",
            "Motor 2": "ns=3;i=1015",
            "Motor 3": "ns=3;i=1017",
            "Motor 4": "ns=3;i=1016",
            "Motor 5": "ns=3;i=1014",
            "Motor 6": "ns=3;i=1012",
            "Motor 7": "ns=3;i=1011",
            "Motor 8": "ns=3;i=1018",
            "Motor 9": "ns=3;i=1020",
            "Motor 10": "ns=3;i=1019",
        }
        return id_map

    def send(self, data: MotorSnapshot):
        node_id = self.process_map.get(data.motor)
        if node_id is None:
            raise MotorNotFoundError(data.motor)
        node = self.client.get_node(node_id)
        self.client.set_values([node], [data.current_speed])
