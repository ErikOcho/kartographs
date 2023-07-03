from enum import Enum

import kivy
kivy.require('2.0.0')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import StringProperty
from kivy.uix.popup import Popup


Builder.load_file('kartographs.kv')


class GamePhase(Enum):
    JAR = 1
    LETO = 2
    JESEN = 3
    ZIMA = 4


class Card():
    """Card class."""
    def __init__(self, value: int, image: str):
        self.value: int = value
        self.image: str = image


def get_all_cards(cards_dir: str) -> list[Card]:
    return [
        Card(2, "./media/2.png"),
        Card(1, "./media/2.png"),
        Card(0, "./media/2.png")
    ]


class GamePhases():
    def __init__(self, points_left: int, game_phase: GamePhase):
        self.points_left = points_left
        self.game_phase = game_phase

    game_phases_lengths = {
        GamePhase.JAR: 8,
        GamePhase.LETO: 8,
        GamePhase.JESEN: 7,
        GamePhase.ZIMA: 6
    }
    game_phase: GamePhase = GamePhase.JAR
    points_left = game_phases_lengths[game_phase]

    def move_by(self, value: int) -> bool:
        """Move game phase by value. Return True if game phase changed."""
        self.points_left -= value
        if self.points_left <= 0:
            if self.game_phase == GamePhase.ZIMA:
                return True  # TODO Ukoncit hru.
            else:
                self.game_phase = GamePhase(self.game_phase.value + 1)
                self.points_left = self.game_phases_lengths[self.game_phase]
                return True
        else:
            return False


class Game():
    def __init__(self, points_left_label, game_phase_label, image_path) -> None:
        self.points_left_label = points_left_label
        self.game_phase_label = game_phase_label
        image_path = image_path

    game_phases_lengths = {
        GamePhase.JAR: 8,
        GamePhase.LETO: 8,
        GamePhase.JESEN: 7,
        GamePhase.ZIMA: 6
    }
    game_phase: GamePhase = GamePhase.JAR
    points_left = game_phases_lengths[game_phase]
    cards_stack: list[Card] = get_all_cards("./media")

    def update_labels(self):
        self.points_left_label = str(self.points_left)
        self.game_phase_label = str(self.game_phase)

    def move_by(self, value: int):
        """Move game phase by value. Return True if game phase changed."""
        self.points_left -= value
        if self.points_left <= 0:
            if self.game_phase == GamePhase.ZIMA:
                pass  # TODO 
            else:
                self.game_phase = GamePhase(self.game_phase.value + 1)
                self.points_left = self.game_phases_lengths[self.game_phase]
        self.update_labels()

    def next(self):
        """We need new card."""
        card = self.cards_stack.pop()
        self.move_by(card.value)
        self.image_path = card.image


class KartographsLayout(FloatLayout):
    window_size = Window.size
    points_left_label = StringProperty("0")
    game_phase_label = StringProperty("JAR")
    image_path = StringProperty('')
    game_phases_lengths = {
        GamePhase.JAR: 8,
        GamePhase.LETO: 8,
        GamePhase.JESEN: 7,
        GamePhase.ZIMA: 6
    }
    game_phase: GamePhase = GamePhase.JAR
    points_left = game_phases_lengths[game_phase]
    cards_stack: list[Card] = get_all_cards("./media")

    game: Game = Game(points_left_label, game_phase_label, image_path)

    def update_labels(self):
        self.points_left_label = str(self.points_left)
        self.game_phase_label = str(self.game_phase)

    def next(self):
        """We need new card."""
        if self.cards_stack == []:
            popup = Popup(title='Test popup', content=Label(text='No cards left.'),
                auto_dismiss=False)
            popup.open()
        card = self.cards_stack.pop()
        self.points_left -= card.value
        if self.points_left <= 0:
            if self.game_phase == GamePhase.ZIMA:
                pass  # TODO 
            else:
                self.game_phase = GamePhase(self.game_phase.value + 1)
                self.points_left = self.game_phases_lengths[self.game_phase]
        self.image_path = card.image
        self.update_labels()


class KartographsApp(App):
    def build(self):
        if (platform == 'android' or platform == 'ios'):
            Window.maximize()
        else:
            Window.size = (600, 800)

        return KartographsLayout()
 
 
if __name__ == "__main__":
    KartographsApp().run()