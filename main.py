import cards
import random
import time

def main():
    num_bots = 3
    bot_exclusive = False

    try:
        if not bot_exclusive:
            while not (username := input("Enter your name: ").strip()):
                continue
            names = [username]
            states = [False]
        else:
            username = None
            names = []
            states = []
        names.extend([f"bot{i + 1}" for i in range(num_bots)])
    except (EOFError, KeyboardInterrupt):
        return

    states.extend([True for _ in range(num_bots)])
    users = [cards.User(name, state, cards.applied_deck) for name, state in zip(names, states)]
    table = cards.Table(cards.applied_deck)

    turn, direction = 0, 1
    game_status, winning_user_index = check_game_status(users)

    print(f"Uno Game! Commands: {users[0].commands}")
    while not game_status:
        try:
            game_state = next_turn(users, username, table, turn, direction, cards.applied_deck)
        except (EOFError, KeyboardInterrupt):
            return

        card_attack, message, turn, direction = game_state

        turn = (turn + direction) % len(users)
        if card_attack:
            print(message)

        game_status, winning_user_index = check_game_status(users)


    winning_user = users[winning_user_index].name

    for user in users:
        print(f"{user.name}'s stack: {user.stack}")
    print(f"\nGood game! Congratulations, {winning_user}, you won!")

def check_game_status(users):
    for i, user in enumerate(users):
        if len(user.stack) == 0:
            return True, i
    return False, None

def next_turn(users, username, tb, turn, direction, target_deck):
    if users[turn].is_bot:
        bot_turn(users[turn], tb, target_deck)
    else:
        user_turn(users, username, tb, target_deck)

    return tb.check_attack_state(users, turn, direction, target_deck)


def user_turn(users, username, tb, target_deck):
    for player in users:
        if player.name == username:
            user = player

    print(f"\nyour hand: {user.stack}")
    print(f"({len(tb.stack)}) table: [{tb.stack[-1]}]")
    print()
    while True:
        commands = input(f"({len(user.stack)}) {user.name}'s turn: ").split()
        if len(commands) == 0:
            continue

        if commands[0] not in user.commands:
            print("invalid command")
            continue
        if commands[0] == "put":
            if len(commands) == 1:
                card = input("Enter card: ").strip()
                card = int(card) if card.isdigit() else card
                put_status = user.put(card, tb)
                if not put_status[0]:
                    print(put_status[1])
                    continue
                else:
                    print(f"{user.name} -> {tb.stack[-1]}")
                    break
            elif len(commands) == 2:
                if commands[1].isdigit():
                    put_status = user.put(int(commands[1]), tb)
                else:
                    put_status = user.put(commands[1], tb)
                if not put_status[0]:
                    print(put_status[1])
                    continue
                else:
                    print(f"{user.name} -> {tb.stack[-1]}")
                    print(f"next color: {tb.next_color}" if "wild" in tb.stack[-1] else "", end="")
                    break
        elif commands[0] == "draw":
            user.draw(target_deck, tb)
            print(f"{user.name} <- {user.stack[-1]}")
        elif commands[0] == "hand":
            user.show_hand()
        elif commands[0] == "tb":
            user.show_table(tb)
        elif commands[0] == "tb_full":
            user.show_full_table(tb)
        elif commands[0] == "cheat":
            if len(commands) == 2:
                for t_user in users:
                    if t_user.name == commands[1]:
                        target_user = t_user
                print(f"{target_user.name}: {target_user.stack}")
            else:
                print("\"cheat\" expects one argument")


def bot_turn(bot, tb, target_deck):
    print()
    print(f"({len(bot.stack)}) {bot.name}'s turn...")
    # print(f"{bot.name}'s stack: {bot.stack}")
    time.sleep(random.randint(1, 3))

    compatible_cards = []
    for card in bot.stack:
        if tb.card_is_compatible(card):
            compatible_cards.append(card)

    if not compatible_cards:
        drawn_card = ""
        while not tb.card_is_compatible(drawn_card):
            drawn_card = bot.draw(target_deck, tb)
            print(f"{bot.name} <- card")
        compatible_cards.append(drawn_card)
    while True:
        bot_card = random.choice(compatible_cards)
        if "wild" in bot_card or bot.put(bot_card, tb)[0]:
            bot.put(bot_card, tb)
            print(f"{bot.name} -> {bot_card}")
            print(f"next color: {tb.next_color}" if "wild" in tb.stack[-1] else "")
            time.sleep(2)
            # print(f"{bot.name}'s stack: {bot.stack}")
            break
#        elif bot.put(bot_card, tb)[0]:
#            break


if __name__ == '__main__':
    main()
