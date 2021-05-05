import logging
from pypylon import pylon
from pypylon.genicam import node_vector
class ConfigurationEventListener(pylon.ConfigurationEventHandler):
    """
        Contains a Configuration Event Handler that prints a message for each event method call.
    """

    def set_callback(self, callback):
        self.callback = callback    

    def OnAttach(self, camera):
        logger.info(f"OnAttach event")

    def OnAttached(self, camera):
        logger.info(f"OnAttached event for device {camera.GetDeviceInfo().GetModelName()}")

    def OnOpen(self, camera):
        logger.info(f"OnOpen event for device {camera.GetDeviceInfo().GetModelName()}")
        if(self.callback is not None):
            self.callback()

    def OnOpened(self, camera):
        logger.info(f"OnOpened event for device {camera.GetDeviceInfo().GetModelName()}")

    def OnGrabStart(self, camera):
        logger.info(f"OnGrabStart event for device {camera.GetDeviceInfo().GetModelName()}")

    def OnGrabStarted(self, camera):
        logger.info(f"OnGrabStarted event for device {camera.GetDeviceInfo().GetModelName()}")

    def OnGrabStop(self, camera):
        logger.info(f"OnGrabStop event for device {camera.GetDeviceInfo().GetModelName()}")

    def OnGrabStopped(self, camera):
        logger.info(f"OnGrabStopped event for device {camera.GetDeviceInfo().GetModelName()}")

    def OnClose(self, camera):
        logger.info(f"OnClose event for device {camera.GetDeviceInfo().GetModelName()}")

    def OnClosed(self, camera):
        logger.info(f"OnClosed event for device {camera.GetDeviceInfo().GetModelName()}")

    def OnDestroy(self, camera):
        logger.info(f"OnDestroy event for device {camera.GetDeviceInfo().GetModelName()}")

    def OnDestroyed(self, camera):
        logger.info(f"OnDestroyed event")

    def OnDetach(self, camera):
        logger.info(f"OnDetach event for device {camera.GetDeviceInfo().GetModelName()}")

    def OnDetached(self, camera):
        logger.info(f"OnDetached event for device {camera.GetDevice().GetModelName()}")

    def OnGrabError(self, camera, errorMessage):
        logger.info(f"OnGrabError event for device {camera.GetDeviceInfo().GetModelName()}")
        logger.info(f"Error Message: {errorMessage}")

    def OnCameraDeviceRemoved(self, camera):
        logger.info(
            f"OnCameraDeviceRemoved event for device {camera.GetDeviceInfo().GetModelName()}")
MAX_CAMERAS = 1
COLLECT_PATH = '/data'

formatter = logging.Formatter(
    '%(asctime)s:%(levelname)s:%(process)d:%(thread)d:%(module)s:%(funcName)s:%(lineno)s:%(message)s')
logger = logging.getLogger(__name__)



class Camera:

    def __init__(self, register_event_listener=False, my_events=None):
        tlFactory = pylon.TlFactory.GetInstance()
        # Get all attached devices and raise an error if no devices found
        devices = tlFactory.EnumerateDevices()
        if not devices:
            raise pylon.RUNTIME_EXCEPTION("No camera present.")

        # Create an array of instant cameras for the found devices and avoid
        # exceeding a maximum number of devices.
        self.cameras = pylon.InstantCameraArray(min(len(devices), MAX_CAMERAS))

        # Create and attach all Pylon Devices.
        for i, cam in enumerate(self.cameras):
            cam.Attach(tlFactory.CreateDevice(devices[i]))
            cam.RegisterConfiguration(my_events, pylon.RegistrationMode_Append,
                                      pylon.Cleanup_Delete)
            # Print the model name of the camera.
            logger.info("Initalizing device : {}".format(cam.GetDeviceInfo().GetModelName()))
            if "NIR" in cam.GetDeviceInfo().GetModelName().upper()[-3:]:
                self.nir = self.cameras[i]
            else:
                self.rgb = self.cameras[i]

def my_callback(param1=''):
    print("\n\n\n\ncallback de fora da classe")


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG', format=formatter._fmt)
    my_events=ConfigurationEventListener()
    my_events.set_callback(my_callback)
    cams = Camera(my_events=my_events)

    for camera in cams.cameras:
        camera.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)
