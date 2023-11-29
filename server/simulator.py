from model.motor import Motor, MotorDataModel
import json
import time

file = '../data/data_plant.json'
with open(file, "r") as inp:
    data = json.load(inp)

signal = 1
signal_time = 0
DO_SIMULATION = True
simulation_time = 0
discretization = 1e-4
horizon = 20

data_models = [MotorDataModel(**model) for model in data['engines']]
motors = [Motor(dm) for dm in data_models]
calculus = {
    str(motor): motor.step_response(horizon=horizon * discretization, discretization=discretization)
    for motor in motors
}
history = {
    str(motor): {
        "simulated": [],
        "calculated": calculus[str(motor)][1],
        "time": calculus[str(motor)][0],
    }
    for motor in motors
}

while True:
    if not DO_SIMULATION:
        break
    s = 0 if simulation_time < signal_time else signal
    for motor in motors:
        last_response = 0 if not history[str(motor)]['simulated'] else history[str(motor)]['simulated'][-1]
        _, response = motor.forced_response(
            input=s,
            last_response=last_response,
            time=history[str(motor)]['time'][simulation_time],
            discretization=discretization
        )
        history[str(motor)]['simulated'].append(response[-1])
    print("SIMULADO: ", history[str(motors[0])]['simulated'][-1])
    print("CALCULADO: ", history[str(motors[0])]['calculated'][simulation_time])
    simulation_time += 1

    if simulation_time >= horizon:
        DO_SIMULATION = False
    time.sleep(1)







