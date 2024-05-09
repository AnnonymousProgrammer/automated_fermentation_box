import json
from dht22_sensor import DHT22Sensor
from threading import Thread
from time import sleep
from camera import Camera
import datetime

class SensorTracer:
    '''
    Class which concurrently reads out and saves images, humidity and temperature values.
    The values are saved in ringbuffers with fixed capacities to avoid memory issues for
    longtime usage.
    '''

    def __init__(self, dht22_sensor, period=30):
        '''
        @param dht22_sensor: instance of the DHT22 Sensor Class
        @param period: sampling period in seconds
        '''
        self.__dht22_sensor = dht22_sensor
        self.__camera = Camera()
        self.__running = False
        self.__period = 60
        # lists that serve as buffers
        self.__humidity = []
        self.__temperature = []
        self.__images = []
        self.__times = []
        # buffer capacities
        self.__capacity = period * 360
        # start concurrent measuring
        self.__start_measuring()
        self.__thread = Thread(target=self.__trace)
        ret_val = self.__thread.start()
        # warm up time for sensor
        while len(self.__images) == 0 and len(self.__temperature) == 0:
            sleep(1)
        self.__old = self.__temperature[-1]
        print("sensor warmed up")

    def __trace(self):
        '''
        periodically reads out temperature, humidity values and saves them to the buffers.
        In case of an overflow the oldest values are removed. Measures if and only if
        marked as running.
        '''
        count = 0
        while self.__running:
            humidity, temperature = self.__dht22_sensor.read_values()
            image = self.__camera.capture()
            self.__times.append(datetime.datetime.now().isoformat())
            self.__images.append(image)
            self.__humidity.append(humidity)
            self.__temperature.append(temperature)
            while len(self.__humidity) > self.__capacity:
                self.__humidity.pop(0)
                self.__temperature.pop(0)
                self.__images.pop(0)
                self.__times.pop(0)
            count = count + 1
            if count % 60 == 0:
                print("sensor tracer" + str(int(count / 60)))
                with open("sensor" + str(int(count / 60)) + ".json", "w") as file:
                    json.dump([self.__temperature, self.__humidity, self.__times], file)
            sleep(self.__period)

    def __start_measuring(self):
        self.__running = True

    def stop_measuring(self):
        self.__running = False

    def __del__(self):
        '''
        destructor to ensure that the thread terminates.
        '''
        self.__running = False

    def get_temp_now(self):
        curr = self.__dht22_sensor.read_values()[1]
        if curr is not None:
           if abs(curr - self.__old) > 0.5:
               return self.__old
           self.__old = curr
           return curr
        return self.__old

    def get_temperature(self):
        #print(len(self.__temperature))
        #print(self.__temperature)
        return tuple(self.__temperature)

    def get_humidity(self):
        return tuple(self.__humidity)

    def get_images(self):
        return tuple(self.__images)

if __name__ == '__main__':
    sensor = DHT22Sensor()
    tracer = SensorTracer(sensor)
    print(tracer.get_temp_now())
    print(tracer.get_images()[-1])
    print(tracer.get_temperature())
    print(tracer.get_humidity())

