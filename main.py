# from gui.widgets.pylon_viewer import PylonViewer
from kivy.app import App
from gui.widgets.control.configuration_page import ConfigurationPage

# a = PylonViewer()
# a.start()

class Main(App):
    kv_directory = 'gui/widgets/view/'
    kv_file = kv_directory + '/index_page.kv'

    def build(self):
        return ConfigurationPage()

if __name__ == '__main__':
    Main().run()