import control as ctrl
from model.motor import Motor
from time import sleep
from interfaces.server_interface import IServer
from dataclasses import dataclass
from typing import Generator
from multiprocessing import Process
from threading import Thread
from collections import defaultdict


@dataclass
class MotorSnapshot:
    motor: str
    is_working: bool
    current_speed: float

def default_snapshot():
    return MotorSnapshot(
        motor='motor',
        is_working=False,
        current_speed=0
    )


power_board: dict[str, bool] = {}
plant_state: dict[str, MotorSnapshot] = defaultdict(default_snapshot)
process_map: dict[str, Process] = {}


def simulated_data(
        motor: Motor,
        control_law: ctrl.TransferFunction,
        discretization: float = 1e-4,
        horizon: int = 60,
        time_discretization: float = 0.1,
) -> Generator:
    time_steps = horizon / time_discretization
    system = (control_law*motor.closed_loop())/(1 + control_law*motor.closed_loop())

    while True:
        global power_board
        is_working: bool = power_board.get(str(motor), False)

        if is_working:
            for i in range(int(time_steps)):
                time_data = [0, ((i + 1) * discretization)]
                _, response = ctrl.step_response(system, time_data)
                yield response[-1]
        else:
            yield 0


def motor_thread(
        motor: Motor,
        data_motor: Generator,
        simulation_period: float = 0.1
):
    while True:
        data = next(data_motor)
        global plant_state, power_board
        state = MotorSnapshot(
            motor=str(motor),
            is_working=power_board.get(str(motor), False),
            current_speed=data
        )
        plant_state[str(motor)] = state
        sleep(simulation_period)


def control_thread(
        motors: list[Motor],
        reference_speed: float,
        server: IServer,
        time_by_motor: int = 60,
        simulation_time: int = 60,
        time_discretization: float = 0.2
):
    # Project a proportional control
    set_point = reference_speed / 2
    k_p = 2
    control_law = ctrl.TransferFunction([k_p], [1])

    # Put control law in motors and create simulators
    motor_simulators: dict[str, Generator] = {}

    for motor in motors:
        simulated_motor = simulated_data(
            motor=motor,
            control_law=control_law,
            horizon=time_by_motor,
        )
        motor_simulators[str(motor)] = simulated_motor
        simulation_args = (motor, simulated_motor, 0.1)
        motor_process = Thread(target=motor_thread, args=simulation_args)
        motor_process.start()
        process_map[str(motor)] = motor_process

    # Choosing motor
    chosen_motors = motors[:4]

    global power_board, plant_state

    while True:
        # Turn On chosen motors
        for motor in chosen_motors:
            power_board[str(motor)] = True

        # send simulations to server
        for motor in motors:
            snapshot = plant_state[str(motor)]
            server.send(data=snapshot)

        sleep(time_discretization)


if __name__ == '__main__':
    import json
    from model.motor import MotorDataModel


    file = '../data/data_plant.json'
    with open(file, "r") as inp:
        data = json.load(inp)

    data_models = [MotorDataModel(**model) for model in data['engines']]
    motors = [Motor(dm) for dm in data_models]

    class FakeServer(IServer):
        def send(self, data):
            print(data)

    server = FakeServer()
    cp = Thread(target=control_thread, args=(motors, 1, server))

    cp.start()

    cp.join()

