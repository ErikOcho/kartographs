import kivy
kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform

Builder.load_file('kartographs.kv')

class KartographsLayout(FloatLayout):
    window_size = Window.size


class KartographsApp(App):
    def build(self):
        if (platform == 'android' or platform == 'ios'):
            Window.maximize()
        else:
            Window.size = (800, 600)

        return KartographsLayout()
 
 
if __name__ == "__main__":
    KartographsApp().run()