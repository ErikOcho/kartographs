import kivy
kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image

def callback(instance):
	print('The image has been clicked')

class MyW(Widget):
	pass

class KartographsApp(App):
	def build(self):
		img = Image(source='edureka.png', pos=(100, 100))
		img.bind(on_touch_down=callback)
		return img

if __name__ == '__main__':
	KartographsApp().run()
