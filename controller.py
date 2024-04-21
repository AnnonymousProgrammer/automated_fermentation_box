from threading import Thread
from time import sleep

class Controller:

    def __init__(self, relais, tracer, target_temp):
        self.__target_temp = target_temp
        self.__relais = relais
        self.__tracer = tracer
        self.__running = False
        self.__control_states =  [False]
        self.__start_control()
        self.__thread = Thread(target=self.__control)
        self.__thread.start()

    def __start_control(self):
        self.__running = True

    def __control(self):
        while self.__running:
            if self.__tracer.get_temperature()[-1] < self.__target_temp and self.__relais.is_opened():
                self.__relais.close_circuit()
            if self.__tracer.get_temperature()[-1] > self.__target_temp and self.__relais.is_closed():
                self.__relais.open_circuit()
            self.__control_states.append(self.__relais.is_closed())
            while len(self.__control_states) > 180:
                self.__control_states.pop(0)
            sleep(60)

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
    
    