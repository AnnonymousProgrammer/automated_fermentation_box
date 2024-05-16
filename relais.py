import RPi.GPIO as GPIO
from time import sleep

class Relais:

    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.output(self.gpio_pin, GPIO.HIGH)
        self.closed = False

    def open_circuit(self):
        GPIO.output(self.gpio_pin, GPIO.HIGH)
        self.closed = False

    def close_circuit(self):
        GPIO.output(self.gpio_pin, GPIO.LOW)
        self.closed = True

    def is_closed(self):
        return self.closed

    def is_opened(self):
        return (not self.closed)

    def __delete__(self):
        GPIO.cleanup()
        
if __name__ == '__main__':
    # local test
    relais = Relais(4)
    print(relais.is_closed())
    print(relais.is_opened())
    relais.close_circuit()
    sleep(5)
    relais.open_circuit()
    sleep(1)
    relais.close_circuit()
