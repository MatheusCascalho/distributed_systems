import time

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
# matplotlib.use('agg')
# import tkinter as tk
import matplotlib.pyplot as plt
import requests


class HTTPCLient:

    @property
    def set_motors(self):
        return "set_motors"

    @property
    def motors_speed(self):
        return "motors_speed"

    @property
    def host(self):
        return "localhost"

    @property
    def port(self):
        return "5000"

    @property
    def protocol(self):
        return "http"

    @property
    def url(self):
        return f"{self.protocol}://{self.host}:{self.port}"

    def get_motors_speed(self):
        url = f"{self.url}/{self.motors_speed}"
        resp = requests.get(url=url)
        return resp.json()

    def set_motors_to_run(self, motors: list[int]):
        url = f"{self.url}/{self.set_motors}"
        payload = {
            "motors": motors
        }
        resp = requests.post(url=url, json=payload)
        return resp

    def speed_monitor(self):
        while True:
            resp = self.get_motors_speed()
            print(resp)
            # for
            with open("historiador.txt", "a") as file:
                file.write(str(resp))
                file.write("\n")
            time.sleep(2)


if __name__ == "__main__":
    client = HTTPCLient()
    res = client.speed_monitor()
    print(res)

# x = np.arange(1, 6)
#
# plt.ion()
# plt.style.use("ggplot")
# for _ in range(10):
#     y = np.random.randint(20, 30, 5)
#     plt.bar(x, y)
#     plt.pause(3)
#     plt.cla()
#     plt.clf()
#
#
# plt.ioff()
