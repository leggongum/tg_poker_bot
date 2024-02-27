from game_manager.manager import Manager, Player

from utils import renew_message


async def upload_update(manager: Manager):
    while True:
        await manager.new_update_event.wait()
        last_update = {'type': None}
        while manager.last_updates:
            update = manager.last_updates.pop(0)
            print(update)

            match update['type']:
                case 'start_info':
                    for player in update['players']:
                        new_player = Player(player['name'], player['chips'], player['bet'])
                        new_player.message = player['message']
                        manager.players.add(new_player)
                case 'get_turn':
                    manager.is_my_turn = True
                    manager.user_name = update['name']
                case 'check' | 'pass':
                    for player in manager.players:
                        if player.name == update['from']:
                            player.status = update['type']
                            break
                    else:
                        player = Player(update['from'], -1, -1)
                        player.status = update['type']
                        manager.players.add(player)
                case 'raise' | 'call':
                    for player in manager.players:
                        if player.name == update['from']:
                            player.status = update['type']
                            player.bet = update['bet']
                            player.chips = update['chips']
                            break
                    else:
                        player = Player(update['from'], update['chips'], update['bet'])
                        player.status = update['type']
                        manager.players.add(player)
                case 'info':
                    if update['stage'] != 'preflop':
                        manager.cards = update['board_cards']
                    else:
                        manager.cards = []
                        for player in manager.players:
                            if player != manager.user_name:
                                player.bet = 5
                                player.status = 'wait'
                    for player in manager.players:
                        if player.name == manager.user_name:
                            player.bet = update['bet']
                            player.chips = update['chips']
                    manager.my_cards = update['self_cards']
                    manager.user_name = update
                    manager.stage = update['stage']
                case 'message':
                    for player in manager.players:
                        if player.name == update['from']:
                            player.message = update['content']
                case 'final':
                    for group in update['winners']:
                        for user in group:
                            for name, chips in user.items():
                                for player in manager.players:
                                    if player.name == name:
                                        player.chips += chips

            last_update = update

        if last_update['type'] == 'final':
            manager.message_id = await renew_message(manager.user, manager.message_id, ''.join(f'{k}: {v}\n' for k,v in last_update['players_cards'].items()) + f'{manager.cards}' + str(last_update['winners']), None)
        else:
            manager.message_id = await renew_message(manager.user, manager.message_id, *manager.construct_tg_representation())

        manager.new_update_event.clear()