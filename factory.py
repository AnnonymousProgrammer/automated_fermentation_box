import configparser
import os
from dht22_sensor import DHT22Sensor
from sensor_tracer import SensorTracer
from relais import Relais
from controller import Controller
from webinterface import WebInterface

class Factory:

    def __init__(self, filename):
        '''
        @param filename: path to the config file.
        '''
        self.__filename = filename

    def __convert_value(self, value):
        '''
        @param value: value to convert

        @return: converted parameter (a number)
        '''
        try:
            # Try converting to integer
            if abs(int(value) - float(value)) < 0.0001:
                return int(value)
        except ValueError:
            try:
                # Try converting to float
                return float(value)
            except ValueError:
                # Return the string as is
                return value

    def __read_ini_file(self):
        if not os.path.exists(self.__filename):
            print("config file not found: " + self.__filename)
        config = configparser.ConfigParser()
        config.read(self.__filename)
        
        config_dict = {}
        
        for section in config.sections():
            config_dict[section] = {}
            for key, value in config.items(section):
                config_dict[section][key] = self.__convert_value(value)
        
        return config_dict

    def build_application(self):
        config_dict = self.__read_ini_file()
        print("set DHT22 sensor pin to: " + str(config_dict["DHT22"]["gpio_pin"]))
        sensor = DHT22Sensor(config_dict["DHT22"]["gpio_pin"])
        print("set sensor tracer period to: " + str(config_dict["Tracer"]["period_s"]))
        print("set sensor tracer tolerance to: " + str(config_dict["Tracer"]["error_tolerance"]))
        tracer = SensorTracer(sensor, config_dict["Tracer"]["period_s"], config_dict["Tracer"]["error_tolerance"])
        print("set relay pin to: " + str(config_dict["Relay"]["gpio_pin"]))
        relais = Relais(config_dict["Relay"]["gpio_pin"])
        relais.open_circuit()
        print("set controller period to: " + str(config_dict["Controller"]["period_s"]))
        print("set controller buffer size to: " + str(config_dict["Controller"]["buffer_size"]))
        print("set controller target temperature to: " + str(config_dict["Controller"]["target_temp"]))
        print("set controller target temperature offset to: " + str(config_dict["Controller"]["offset"]))
        my_con = Controller(relais, tracer, config_dict["Controller"]["target_temp"], config_dict["Controller"]["offset"], 
                            config_dict["Controller"]["period_s"], config_dict["Controller"]["buffer_size"])
        return WebInterface(tracer, my_con, config_dict["Website"]["period_s"])

if __name__ == '__main__':
    # actual main function
    root = os.path.abspath(__file__)
    root = root[:(len(root) - len(os.path.basename(root)))]
    config_path = root + os.sep + "config.ini"
    website = Factory(config_path).build_application()
