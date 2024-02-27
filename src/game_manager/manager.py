from asyncio import Event

from game_manager.callback import turn_menu


class Player:
    def __init__(self, name: str, chips: int, bet: int):
        self.name = name
        self.chips = chips
        self.bet = bet
        self.status: str = ''
        self.message: str = ''

    def __hash__(self) -> int:
        return hash(self.name)
    
    def __eq__(self, other) -> bool:
        return self.__hash__() == hash(other) if type(other) == type(self) else False


class Manager:
    def __init__(self, user: int, lobby_title: str, message_id: int):
        self.user = user
        self.lobby_title = lobby_title
        self.message_id = message_id

        self.stage: str = 'wait'
        self.user_name: str = ''
        self.my_cards: list[str] = []
        self.cards: list[str] = []
        self.is_my_turn: bool = False
        self.players: set[Player] = set()

        self.last_updates: list[dict] = []
        self.new_update_event: Event = Event()

        self.data_for_back: list[dict] = []
        self.new_data_for_back: Event = Event()

    def construct_tg_representation(self) -> tuple:
        body = f"""lobby: {self.lobby_title}
stage: {self.stage}
my_cards: {', '.join(self.my_cards)}
cards: {', '.join(self.cards)}""" + '\n' + ''.join(
    f'{player.name}: chips={player.chips} bet={player.bet} {player.status}\n' for player in self.players
    ) + ''.join(f'\n{player.name}: {player.message}' for player in self.players if player.message)
        markup = turn_menu if self.is_my_turn else None
        return body, markup
