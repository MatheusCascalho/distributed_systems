from model.opc_communication import OPCDataClient
from opcua import Client
from flask import Flask, request, jsonify
from time import sleep
from threading import Thread


motors_to_run: list = [0, 1, 2, 3]
motors_speed: dict[str, float] = {}


class CLPClient(OPCDataClient):
    def __init__(self, update_rate: float = 0.2):
        self.client = Client(self.server_url)
        self.client.connect()
        self.last_motors = ""
        self.update_rate = update_rate

    def set_motors_to_run(self):
        global motors_to_run
        motors = [str(m) for m in motors_to_run]
        command = ".".join(motors)
        if not self.last_motors or (self.last_motors and self.last_motors != command):
            node_id = self.process_map.get("StartMotors")
            node = self.client.get_node(node_id)
            res = self.client.set_values([node], [command])
            print(f"Motores atualizados: {command}")
            self.last_motors = command

    def read_motors_speed(self):
        global motors_speed
        motors = [k for k in self.process_map if 'motor' in k.lower()]
        for motor in motors:
            node_id = self.process_map.get(motor)
            node = self.client.get_node(node_id)
            speed = self.client.get_values([node])
            if speed:
                motors_speed[motor] = speed

    def run(self):
        while True:
            self.read_motors_speed()
            self.set_motors_to_run()
            sleep(self.update_rate)


# class TCPServer:
server = Flask(__name__)


def are_valid_engines(motors):
    ordered_motors = sorted(motors)
    for i, motor in enumerate(ordered_motors[:-1]):
        if ordered_motors[i+1] == motor:
            return False
    return True


@server.route("/set_motors", methods=['POST'])
def set_motors_to_run():
    data = request.get_json()
    motors = data.get('motors', [])
    if not are_valid_engines(motors):
        return jsonify({"error": "Não é possível ligar dois motores consecutivos"}), 400
    global motors_to_run
    motors_to_run = motors
    return jsonify({"status": "ok"})


@server.get("/motors_speed")
def read_motors_speed():
    global motors_speed
    data = motors_speed.copy()
    return jsonify(data)


opc_client = CLPClient()

opc = Thread(target=opc_client.run)
tcp = Thread(target=server.run)

tcp.start()
opc.start()

tcp.join()
opc.join()
