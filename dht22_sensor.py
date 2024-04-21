import sys

import Adafruit_DHT

class DHT22Sensor:
    '''
    wrapper class for the Adafruit_DHT implementation lib
    '''
    
    def __init__(self, gpio_pin=2):
        '''
        @param gpio_pin: pin to which the data pin of the sensor connected to.
        '''
        self.__sensor = Adafruit_DHT.DHT22
        self.__gpio_pin = gpio_pin

    def read_values(self):
        '''
        @return: tuple containing humidity and temperature
        '''
        humidity, temperature = Adafruit_DHT.read_retry(self.__sensor, self.__gpio_pin)
        return humidity, temperature

if __name__ == '__main__':
    sensor = DHT22Sensor()
    print(sensor.read_values())
