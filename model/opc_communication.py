from interfaces.server_interface import IServer
from opcua import Client

from model.exceptions import MotorNotFoundError
from model.process import MotorSnapshot


class OPCDataClient:
    @property
    def server_url(self):
        return "opc.tcp://LAPTOP-289TONJ4:53530/OPCUA/SimulationServer"

    @property
    def process_map(self):
        id_map = {
            "Motor_0": "ns=3;i=1019",
            "Motor_1": "ns=3;i=1013",
            "Motor_2": "ns=3;i=1015",
            "Motor_3": "ns=3;i=1017",
            "Motor_4": "ns=3;i=1016",
            "Motor_5": "ns=3;i=1014",
            "Motor_6": "ns=3;i=1012",
            "Motor_7": "ns=3;i=1011",
            "Motor_8": "ns=3;i=1018",
            "Motor_9": "ns=3;i=1020",
            "StartMotors": "ns=3;i=1023",
            "CurrentSimulationTime": "ns=3;i=1024"
        }
        return id_map


class OPCProcessCommunication(IServer, OPCDataClient):
    def __init__(self):
        self.client = Client(self.server_url)
        self.client.connect()

    def send(self, data: MotorSnapshot):
        node_id = self.process_map.get(data.motor)
        if node_id is None:
            raise MotorNotFoundError(data.motor)
        node = self.client.get_node(node_id)
        self.client.set_values([node], [data.current_speed])

    def read_start_motors(self):
        node_id = self.process_map.get("StartMotors")
        if node_id is None:
            return [0, 1, 2, 3]
        node = self.client.get_node(node_id)
        value = self.client.get_values([node])
        if not value:
            value = ["0.2.4.6"]
        start_motors = [int(v) for v in value[0].split(".")]
        return start_motors

    def send_current_time(self, data):
        node_id = self.process_map.get("CurrentSimulationTime")
        node = self.client.get_node(node_id)
        self.client.set_values([node], [data], )

    def __del__(self):
        self.client.disconnect()
