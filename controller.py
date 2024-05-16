import datetime
import json
from threading import Thread
from time import sleep

class Controller:

    def __init__(self, relais, tracer, target_temp=27, offset=0.25, sampling_period=1, buffer_size=1800):
        '''
        Two Point controller.
        @param relais: instance of relais class.
        @param tracer: instance of sensor tracer.
        @param target_temp: desired target temperature.
        @param offset: value that will be subtracted from the target temperature as the heatbed will still exhaust heat after being switched off.
        @param sampling_period: sampling period of the control algorithm.
        @param buffer_size: size of the control history buffer.
        '''
        self.__target_temp = target_temp
        self.__relais = relais
        self.__tracer = tracer
        self.__running = False
        self.__control_states =  [False]
        self.__temps = []
        self.__times = [datetime.datetime.now().isoformat()]
        self.__offset = offset
        self.__sampling_period = sampling_period
        self.__buffer_size = buffer_size
        self.__start_control()
        self.__thread = Thread(target=self.__control_two_point)
        self.__thread.start()

    def __start_control(self):
        self.__running = True

    def __control_two_point(self):
        '''
        Two point control algorithm that runs in an infinity loop until the boolean flag __running is set to false.
        As well saves the control history in a buffer and periodically to disc.
        Periodically checks the temperature. I. e. the method is not event based.
        '''
        count = 0
        while self.__running:
            curr_temp = self.__tracer.get_temp_now()
            if curr_temp < (self.__target_temp - self.__offset) and self.__relais.is_opened():
                self.__relais.close_circuit()
                print("close circuit")
            if curr_temp > (self.__target_temp - self.__offset) and self.__relais.is_closed():
                self.__relais.open_circuit()
                print("open circuit")
            self.__control_states.append(self.__relais.is_closed())
            self.__temps.append(curr_temp)
            self.__times.append(datetime.datetime.now().isoformat())
            while len(self.__control_states) > self.__buffer_size:
                self.__control_states.pop(0)
                self.__times.pop(0)
                self.__temps.pop(0)
            count = count + 1
            if count % (self.__buffer_size) == 0:
                with open("control" + str(int(count / self.__buffer_size)) + ".json", "w") as file:
                    json.dump([self.__control_states, self.__temps, self.__times], file)
            sleep(self.__sampling_period)

    def __delete(self):
        self.__running = False

    def stop(self):
        self.__running = False

    def get_history(self):
        return tuple(self.__control_states)

if __name__ == '__main__':
    # local test
    from dht22_sensor import DHT22Sensor
    from relais import Relais
    from sensor_tracer import SensorTracer
    sensor = DHT22Sensor()
    tracer = SensorTracer(sensor)
    relais = Relais(4)
    relais.open_circuit()
    my_con = Controller(relais, tracer, 27)
    
    
