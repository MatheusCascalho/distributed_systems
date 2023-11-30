from model.motor import Motor, MotorDataModel
import control as ctrl
import json
import time

file = '../data/data_plant.json'
with open(file, "r") as inp:
    data = json.load(inp)

signal = 1
signal_time = 3
DO_SIMULATION = True
simulation_time = 0
discretization = 1e-4
horizon = 2000
time_disctretization = 1/10000

data_models = [MotorDataModel(**model) for model in data['engines']]
motors = [Motor(dm) for dm in data_models]
calculus = {
    str(motor): motor.step_response(horizon=horizon * discretization, discretization=discretization)
    for motor in motors
}
history = {
    str(motor): {
        "simulated": [],
        "calculated": [0]*signal_time + list(calculus[str(motor)][1]),
        "time": calculus[str(motor)][0],
    }
    for motor in motors
}

while True:
    if not DO_SIMULATION:
        break
    s = 0 if simulation_time < signal_time else signal
    for motor in motors:
        if s > 0:
            time_data = [0, ((simulation_time+1)*discretization)-(signal_time*discretization)]
            _, response = ctrl.step_response(motor.closed_loop(), time_data)
        else:
            response = [0]
        history[str(motor)]['simulated'].append(response[-1])
    print("SIMULADO: ", history[str(motors[2])]['simulated'][-1])
    print("CALCULADO: ", history[str(motors[2])]['calculated'][simulation_time])
    simulation_time += 1

    if simulation_time >= horizon:
        DO_SIMULATION = False
    time.sleep(time_disctretization)







