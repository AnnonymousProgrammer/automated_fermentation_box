import datetime
import json
from threading import Thread
from time import sleep

class Controller:

    def __init__(self, relais, tracer, target_temp):
        self.__target_temp = target_temp
        self.__relais = relais
        self.__tracer = tracer
        self.__running = False
        self.__control_states =  [False]
        self.__temps = []
        self.__times = [datetime.datetime.now().isoformat()]
        self.__start_control()
        self.__thread = Thread(target=self.__control)
        self.__thread.start()

    def __start_control(self):
        self.__running = True

    def __control(self):
        count = 0
        while self.__running:
            curr_temp = self.__tracer.get_temp_now()
            if curr_temp < (self.__target_temp - 0.25) and self.__relais.is_opened():
                self.__relais.close_circuit()
                print("close circuit")
            if curr_temp > (self.__target_temp - 0.25) and self.__relais.is_closed():
                self.__relais.open_circuit()
                print("open circuit")
            self.__control_states.append(self.__relais.is_closed())
            self.__temps.append(curr_temp)
            self.__times.append(datetime.datetime.now().isoformat())
            while len(self.__control_states) > 1800:
                self.__control_states.pop(0)
                self.__times.pop(0)
                self.__temps.pop(0)
            count = count + 1
            if count % (1800) == 0:
                with open("control" + str(int(count / 1800)) + ".json", "w") as file:
                    json.dump([self.__control_states, self.__temps, self.__times], file)
            sleep(1)

    def __delete(self):
        self.__running = False

    def stop(self):
        self.__running = False

    def get_history(self):
        return tuple(self.__control_states)

if __name__ == '__main__':
    from dht22_sensor import DHT22Sensor
    from relais import Relais
    from sensor_tracer import SensorTracer
    sensor = DHT22Sensor()
    tracer = SensorTracer(sensor)
    relais = Relais(4)
    relais.open_circuit()
    my_con = Controller(relais, tracer, 27)
    
    
