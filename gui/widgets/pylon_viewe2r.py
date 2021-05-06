'''
PylonViewer
'''

from pypylon import pylon
import cv2
import time
from threading import Thread
import os

from pypylon import pylon
class ConfigurationEventListener(pylon.ConfigurationEventHandler):
    """
        Contains a Configuration Event Handler that prints a message for each event method call.
    """
    def OnCameraDeviceRemoved(self, camera):
        logger.info(
            f"\n\n\n\nOnCameraDeviceRemoved event for device {camera.GetDeviceInfo().GetModelName()}")

def init_camera(time_for_capture):
    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())


    camera.MaxNumBuffer = 5000

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_OneByOne) 
    converter = pylon.ImageFormatConverter()

    camera.Gamma.SetValue(1.0)
    camera.ExposureTime.SetValue(5739)  #(7840)  # 32670
    camera.BalanceWhiteAuto.SetValue('Off')
    # print(dir(camera))
    camera.AcquisitionFrameRateEnable.SetValue(True)
    camera.AcquisitionFrameRate.SetValue(30)
    # print(camera.AcquisitionFrameRate.GetValue(), camera.ResultingFrameRate.GetValue())

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    return camera, converter

def get_photo(camera, converter):


    grabResult = camera.RetrieveResult(2000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        grabResult.Release()
        

    return img



import logging
import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture


logger = logging.getLogger(__name__)

console = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)-7s] [%(name)-12s] %(asctime)s %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)
logger.setLevel(logging.INFO)


logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')


class PylonViewer(Image):
    capture = None

    def __init__(self, **kwargs):
        super(PylonViewer, self).__init__(**kwargs)
        logger.debug('> __init__()')


    def start(self, fps=30):
        try:

            self.camera, self.converter = init_camera(1)

        except Exception as e :
            print("\n\n\n \n\n!!!!!!!!!!!!!!!!", e,"\n\n\n\n")
        logger.debug('> start(fps={fps})'.format(fps=fps))
        print('start 1')
        if self.capture is None:
            print('start 2')
            #self.capture = cv2.VideoCapture(0)
            try:

                _frame = get_photo(self.camera, self.converter)  # read the camera frame
                self.capture = cv2.resize(_frame, (600, 300))
            except Exception as e :
                print("\n\n\n \n\n", e)

            print('start 3')
        Clock.schedule_interval(self.update, 1.0 / fps)
        print('start 4')
        logger.debug('< Start()')
    
    def stop(self):
        logger.debug('> stop()')
        self.capture = None
        Clock.unschedule(self.update)

    def update(self, dt):
        try:
            logger.debug('> __update()')
            #return_value, frame = self.capture.read()
            
            frame = get_photo(self.camera, self.converter)
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()

        except Exception as e :
            print("\n\n\n \n\n", e)



