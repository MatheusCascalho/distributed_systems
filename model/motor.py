import control
import control as ctrl
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np


@dataclass
class MotorDataModel:
    resistence: float
    inductance: float
    torque: float
    inertia_moment: float
    viscous_friction: float
    electrical_constant: float


class Motor:
    def __init__(self, data_model: MotorDataModel):
        self.data_model = data_model

    def armature_circuit(self) -> ctrl.TransferFunction:
        num = [1 / self.data_model.resistence]
        den = [
            self.data_model.inductance / self.data_model.resistence,
            1
        ]
        armature = ctrl.TransferFunction(num, den)
        return armature

    def axis_dynamic(self) -> ctrl.TransferFunction:
        num = [1]
        den = [
            self.data_model.inertia_moment,
            self.data_model.viscous_friction
        ]
        axis = ctrl.TransferFunction(num, den)
        return axis

    def open_loop(self, load_torque=0) -> ctrl.TransferFunction:
        armature = self.armature_circuit()
        motor_torque = armature * self.data_model.torque
        axis = self.axis_dynamic()
        system = (motor_torque + load_torque) * axis
        return system

    def closed_loop(self, load_torque=0) -> ctrl.TransferFunction:
        system = self.open_loop(load_torque)
        closed = ctrl.feedback(system, self.data_model.electrical_constant)
        return closed

    def step_response(self, horizon, discretization=1e-3):
        time_steps = int(horizon / discretization)
        time = np.linspace(0, horizon, time_steps)
        time, response = ctrl.step_response(self.closed_loop(), time)
        return time, response

    def plot_step_response(self, horizon):
        time, response = self.step_response(horizon=horizon)
        plt.plot(time, response)
        plt.xlabel('Tempo')
        plt.ylabel('Resposta do Sistema')
        plt.title('Resposta ao Degrau Unitário')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    import json
    with open("../data/data_plant.json", "r") as inp:
        data = json.load(inp)

    data_model = MotorDataModel(**data['engines'][0])
    motor = Motor(data_model)
    r = motor.step_response(horizon=10)
    print(r)

