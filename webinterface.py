import cv2
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime, timedelta
from time import sleep

class WebInterface:

    def __init__(self, tracer, controller, period=60):
        '''
        @param tracer: instance of sensor_tracer class.
        @param controller: instance of the controller class.
        @param period: update period of the website
        '''
        self.__tracer = tracer
        self.__controller = controller
        self.__period = period
        # init webpage
        self.__construct_webinterface()

    def get_period(self):
        return self.__period

    def __get_data(self):
        # get latest data
        image_cv = self.__tracer.get_images()[-1]
        temps = list(self.__tracer.get_temperature())
        humidity = list(self.__tracer.get_humidity())
        actions = list(self.__controller.get_history())
        # adapt scaling
        actions = list(map(lambda x: int(x) * 100.0, actions))
        # extrapolate data
        while len(temps) < 100:
            if (len(temps) < 100):
                temps.append(temps[-1])
                humidity.append(humidity[-1])
            else:
                temps.pop(0)
                humidity.pop(0)
        while len(actions) != 100:
            if (len(actions) < 100):
                actions.append(actions[-1])
            else:
                actions.pop(0)
        # Convert OpenCV image to pillow Image
        image_pil = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
        # pack data together
        df = pd.DataFrame({
            'index': np.arange(1, len(temps) + 1),
            'temperature in Celsius': temps,
            'humidity in Percentage': humidity,
            'Relais State' : actions
        })
        # Set the index of the DataFrame to the date column
        df.set_index('index', inplace=True)
        return temps, humidity, image_pil, df

    def __construct_webinterface(self):
        st.title("Fermentation Box Monitor")
        temp_placeholder = st.empty()
        humid_placeholder = st.empty()
        image_placeholder = st.empty()
        linechart_placeholder = st.empty()
        while True:
            temps, humidity, image_pil, df = self.__get_data()
            # display image
            image_placeholder = image_placeholder.image(image_pil, caption='Content of Fermentation Box', use_column_width=True)
            # display low level sensorics info
            temp_placeholder.text("Current Temperature in Celsius: {}".format(temps[-1]))
            humid_placeholder.text("Current Humidity in Percentage: {}".format(humidity[-1]))
            # create time plots
            linechart_placeholder.line_chart(df, use_container_width=True)
            sleep(self.get_period())

if __name__ == '__main__':
    # small local test to check if it is working
    from dht22_sensor import DHT22Sensor
    from sensor_tracer import SensorTracer
    from relais import Relais
    from controller import Controller
    from time import sleep
    sensor = DHT22Sensor()
    tracer = SensorTracer(sensor)
    print("sensor tracer initialized")
    relais = Relais(4)
    relais.open_circuit()
    my_con = Controller(relais, tracer, 27)
    website = WebInterface(tracer, my_con)
