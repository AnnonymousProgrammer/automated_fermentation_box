import configparser
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
        sensor = DHT22Sensor(config_dict["DHT22"]["gpio_pin"])
        tracer = SensorTracer(sensor, config_dict["Tracer"]["period_s"], config_dict["Tracer"]["error_tolerance"])
        print("sensor tracer initialized")
        relais = Relais(config_dict["Relay"]["gpio_pin"])
        relais.open_circuit()
        my_con = Controller(relais, tracer, config_dict["Tracer"]["target_temp"], config_dict["Tracer"]["offset"], 
                            config_dict["Tracer"]["period_s"], config_dict["Tracer"]["buffer_size"])
        return WebInterface(tracer, my_con, config_dict["Tracer"]["period_s"])

if __name__ == '__main__':
    # actual main function
    website = Factory().build_application()
