import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button

from game import Game
from game_defs import game_phase_dict, GamePhase


# Načítanie layoutu celého GUI.
Builder.load_file('kartographs.kv')


def show_final_popup(title: str) -> None:
    """Show popup with title."""
    content = Button(text='OK')
    popup = Popup(title=title, padding=30, content=content,
                  size_hint=(0.5, 0.2), auto_dismiss=False)

    # bind the on_press event of the button to the dismiss function
    content.bind(on_press=popup.dismiss)
    content.bind(on_release=App.get_running_app().stop)

    # open the popup
    popup.open()


class KartographsLayoutCallBacks(FloatLayout):
    def __init__(self):
        self.window_size = Window.size
        self.points_left_label = StringProperty("0")
        self.game_phase_label = StringProperty("JAR")
        self.image_path = StringProperty('./media/seasons/jar.png')

    def on_points_left_change(self, value: int):
        self.points_left_label = str(value)

    def on_game_phase_change(self, game_phase: GamePhase):
        self.game_phase_label = game_phase_dict[game_phase]

    def on_image_path_change(self, value: str):
        self.image_path = value


class KartographsApp(App):
    def build(self):
        if (platform == 'android' or platform == 'ios'):
            Window.maximize()
        else:
            Window.size = (600, 800)

        return KartographsLayoutCallBacks()




if __name__ == "__main__":
    KartographsApp().run()