import cv2

class Camera:
    
    def __init__(self):
        self.__camera = cv2.VideoCapture(0)

    def capture(self):
        return_value, image = self.__camera.read()
        return image

    def debug_snapshot(self):
        image = self.capture()
        cv2.imshow("debug", image)
        cv2.waitKey(0)

    def __del__(self):
        '''
        destructor to ensure that the camera is closed properly.
        '''
        self.__camera.release()

if __name__ == '__main__':
    Camera().debug_snapshot()
