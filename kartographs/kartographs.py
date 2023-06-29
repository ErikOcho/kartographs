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

Builder.load_file('kartographs.kv')

class MyLayout(Widget):
    pass


class KartographsApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MyLayout()
        # f = FloatLayout()
        # s = Scatter()
        # l = Label(text="Edureka!", font_size=40)
 
        # f.add_widget(s)
        # s.add_widget(l)
        # return f
 
 
if __name__ == "__main__":
    KartographsApp().run()