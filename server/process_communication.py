import json
from model.motor import MotorDataModel, Motor
from model.clp_communication import CLPCommunication
from model.process import control_thread
from threading import Thread


file = '../data/data_plant.json'
with open(file, "r") as inp:
    data = json.load(inp)

data_models = [MotorDataModel(**model) for model in data['engines']]
motors = [Motor(dm) for dm in data_models]


server = CLPCommunication()
reference_speed = 1

cp = Thread(target=control_thread, args=(motors, reference_speed, server))

cp.start()

cp.join()
