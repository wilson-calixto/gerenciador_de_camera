from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.uix.image import Image
from gui.widgets.pylon_viewer import PylonViewer
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2
import numpy as np

import logging

logger = logging.getLogger(__name__)

console = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)-7s] [%(name)-12s] %(asctime)s %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)
logger.setLevel(logging.INFO)


class ConfigurationPage(TabbedPanel):
    def __init__(self, **kwargs):
        super(ConfigurationPage, self).__init__(**kwargs)
        self.bind(current_tab = self.wich_tab)


    def wich_tab(self, instance, value):
        
        logger.debug('> wich_tab()')
        logger.info('in tab: ' + str(value.text))

        if value.text == 'Camera':
            self.ids.camera2.stop()
            print("aqui")
            self.ids.camera.start()
        elif value.text == 'HDMI':
            self.ids.camera.stop()
            self.ids.camera2.start()
        
        

    def dostart(self):
        pass