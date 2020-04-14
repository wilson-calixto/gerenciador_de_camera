'''
PylonViewer
'''

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
        logger.debug('> start(fps={fps})'.format(fps=fps))
        print('start 1')
        if self.capture is None:
            print('start 2')
            self.capture = cv2.VideoCapture(0)
            print('start 3')
        Clock.schedule_interval(self.update, 1.0 / fps)
        print('start 4')
        logger.debug('< Start()')
    
    def stop(self):
        logger.debug('> stop()')
        self.capture = None
        Clock.unschedule(self.update)

    def update(self, dt):
        logger.debug('> __update()')
        return_value, frame = self.capture.read()
        if return_value:
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()
