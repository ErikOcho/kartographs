import re
import random as rnd
from pathlib import Path


from game_defs import Card, CardType, GamePhase


def get_all_png_file_names(cards_dir: str) -> list[Path]:
    """Get all png files from directory. Match any pattern with *.png."""
    return Path(cards_dir).glob('*.png')


def read_all_cards_as(cards_dir: str, as_card_type: CardType) -> list[Card]:
    """Get all cards from directory. Match any pattern with *.png."""
    cards = []
    pattern = re.compile(r"(\d+)_.+\.png")
    for card_name in get_all_png_file_names(cards_dir):
        if re.match(r"\d+.*", card_name.name):
            res = re.search(pattern, card_name.name)
            cards.append(Card(int(res.group(1)), card_name.as_posix(), as_card_type))
        else:
            cards.append(Card(0, card_name.as_posix(), as_card_type))
    return cards


def get_all_beast_cards(cards_dir: str) -> list[Card]:
    """
    Get all cards from directory.
    Match any pattern with *.png.
    Value set to zero.
    """
    cards = []
    path_names = Path(cards_dir).glob('*.png')
    for file_name in path_names:
        cards.append(Card(0, file_name.as_posix(), CardType.BEAST))
    return cards


def get_all_temple_cards(cards_dir: str) -> list[Card]:
    cards = []
    path_names = Path(cards_dir).glob('*.png')
    for file_name in path_names:
        cards.append(Card(0, file_name.as_posix(), CardType.BEAST))
    return cards


def get_all_search_cards(cards_dir: str) -> list[Card]:
    """Get all serach cards from directory. These cards have cost."""
    cards = []
    path_names = Path(cards_dir).glob('*.png')
    pattern = re.compile(r"(\d+)_.+\.png")
    for file_name in path_names:
        res = re.search(pattern, file_name.name)
        if re.match(r".*temple.*", file_name.name):
            cards.append(Card(int(res.group(1)), file_name.as_posix(), CardType.TEMPLE))
        else:
            cards.append(Card(int(res.group(1)), file_name.as_posix(), CardType.SEARCH))
    return cards


class Year():
    def __init__(self) -> None:
        self.game_phase = GamePhase.JAR
        self.game_phases_lengths = {
            GamePhase.JAR: 8,
            GamePhase.LETO: 8,
            GamePhase.JESEN: 7,
            GamePhase.ZIMA: 6
        }
        self.points_left = self.game_phases_lengths[self.game_phase]

    def move_by(self, value: int) -> tuple[bool, bool]:
        """Posunie čas o zadanú hodnotu.

        Args:
            value: hodnota vyjadrujúca posun času.

        Returns:
            Príznak či nasleduje zmena fázy hry.
            Priznak ci sa jedna o koniec hry.
        """
        new_phase_begun: bool = False
        end_game: bool = False
        if self.points_left <= 0:
            if self.game_phase == GamePhase.ZIMA:
                end_game = True
            else:
                self.game_phase = GamePhase(self.game_phase.value + 1)
                self.points_left = self.game_phases_lengths[self.game_phase]
                new_phase_begun = True

        self.points_left -= value
        return (new_phase_begun, end_game)


class CardsStacks():
    """Stack of cards."""
    def __init__(self, free_cards: list[Card], beast_cards: list[Card]):
        self.free_cards: list[Card] = free_cards
        self.drawn_cards: list[Card] = []
        self.beast_cards: list[Card] = beast_cards

        rnd.shuffle(self.beast_cards)
        rnd.shuffle(self.free_cards)

    def switch_phase(self) -> None:
        """Shuffle cards together and add one beast."""
        # Pridam karky ktore boli uz pouzite.
        self.free_cards = self.free_cards + self.drawn_cards
        self.drawn_cards = []
        self.free_cards.append(self.beast_cards.pop())

        rnd.shuffle(self.free_cards)

    def get_card(self) -> Card:
        """Get card from stack."""
        card = self.free_cards.pop()
        if card.type != CardType.BEAST:
            self.drawn_cards.append(card)
        return card


class Game():
    """Game class."""
    def __init__(self) -> None:
        self.cards.switch_phase()

    year: Year = Year()
    all_search_cards: list[Card] = read_all_cards_as("./media/search", CardType.SEARCH) \
        + (read_all_cards_as("./media/temples", CardType.TEMPLE))
    all_beasts_cards: list[Card] = read_all_cards_as("./media/beasts", CardType.BEAST)
    cards = CardsStacks(all_search_cards, all_beasts_cards)
    game_over = False

    def next(self) -> tuple[int, str, GamePhase, bool]:
        """We need new card."""
        if len(self.cards.free_cards) == 0:
            # show_final_popup("No more cards!")
            return (0, "", GamePhase.ZIMA, True)

        # Ziskam novu kartu.
        card = self.cards.get_card()
        new_phase_begun, end_game = self.year.move_by(card.value)

        if end_game:
            # show_final_popup("Game is over!")
            return (0, "", GamePhase.ZIMA, True)

        if new_phase_begun:
            # if self.year.game_phase == GamePhase.ZIMA:
            #     show_final_popup("Game is over!")
            #     return (0, "", GamePhase.ZIMA, True)
            self.cards.switch_phase()

        return (
            self.year.points_left,
            card.image,
            self.year.game_phase,
            False
        )

