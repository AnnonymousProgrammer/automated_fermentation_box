import cv2

class Camera:
    
    def __init__(self):
        # self.__camera = cv2.VideoCapture(0)
        self.__old = []

    def capture(self):
        try:
            camera = cv2.VideoCapture(0)
            return_value, image = camera.read()
            self.__old = image
            camera.release()
        except Exception as _:
            pass
        return self.__old

    def debug_snapshot(self):
        image = self.capture()
        cv2.imshow("debug", image)
        cv2.waitKey(0)

    def __del__(self):
        '''
        destructor to ensure that the camera is closed properly.
        '''
        pass
        # self.__camera.release()

if __name__ == '__main__':
    Camera().debug_snapshot()
