import random

class User:
    def __init__(self, name, user_state, target_deck):
        self.name = name
        self.stack = [target_deck.pop() for _ in range(7)]
        self.commands = ["put", "draw", "hand", "tb", "tb_full", "cheat"]
        # self.debug_commands = ["userhand", ""]
        self.is_bot = user_state

    def format_card(self, card):
        color_fmt = {
            "r": "red",
            "g": "green",
            "b": "blue",
            "y": "yellow",
            "w": "wild",
            "wd": "wild_draw4"
        }
        number_fmt = {
            "r": "reverse",
            "s": "skip",
            "d": "draw2"
        }

        if card == "w" or card == "wd":
            return color_fmt[card]
        elif len(card) == 2 and card[0] in color_fmt and (card[1] in number_fmt or card[1].isdigit()):
            return f"{color_fmt[card[0]]}_{number_fmt[card[1]] if not card[1].isdigit() else card[1]}"

        return False

    def put(self, card_i, tb):
        if type(card_i) == int:
            card_i -= 1
            if not (0 <= card_i < len(self.stack)):
                return (False, "invalid card index!")
            card = self.stack[card_i]
        else:
            card_i = self.format_card(card_i) if self.format_card(card_i) else card_i
            if card_i not in deck:
                return (False, "invalid card name!")
            elif card_i not in self.stack:
                return (False, "you don't have that card!")
            else:
                card = card_i

        card_loc = self.stack.index(card)
        success = (True, "card added to table")
        failure = (False, "incompatible card")

        if not tb.card_is_compatible(self.stack[card_loc]):
            return failure
        else:
            if "wild" in card:
                if self.is_bot:
                    user_color_choice = random.choice(["red", "green", "blue", "yellow"])
                else:
                    colors = {
                        'r': "red",
                        'g': "green",
                        'b': "blue",
                        'y': "yellow"
                    }
                    user_color_choice = colors[input("Enter color (r/g/b/y): ").strip()]
                tb.add(self.stack.pop(card_loc), color_choice=user_color_choice)
                return success
            else:
                tb.add(self.stack.pop(card_loc))
                return success


    def draw(self, target_deck, tb):
        if not target_deck:
            tb.refill_deck(target_deck)
            print("refilling the deck")
            # print(f"\ndeck:\n{target_deck}")
            # print(f"\ntable:\n{tb.stack}")

        # print(f"stack before drawing card: {self.stack}")
        drawn_card = target_deck.pop()
        self.stack.append(drawn_card)

        return drawn_card

    def show_hand(self):
        if len(self.stack) <= 10:
            print(self.stack)
        else:
            print("[", end='')
            for i in range(len(self.stack)):
                print(f"{self.stack[i]}{', ' if i < len(self.stack)-1 else ']\n'}{'\n' if (i + 1) % 10 == 0 else ''}",
                      end='')
    def show_table(self, tb):
        print(f"({len(tb.stack)}) [{tb.stack[-1]}]")

    def show_full_table(self, tb):
        if len(tb.stack) <= 10:
            print(tb.stack)
        else:
            print("[", end='')
            for i in range(len(tb.stack)):
                print(f"{tb.stack[i]}{', ' if i < len(tb.stack)-1 else ']\n'}{'\n' if (i + 1) % 10 == 0 else ''}",
                      end='')


class Table:
    first_card_filt = lambda self, card: "_" in card and card[card.index("_") + 1:].isdigit()
    def __init__(self, target_deck):
        self.first_card_i = next((i for i, card in enumerate(target_deck) if self.first_card_filt(card)), None)
        self.stack = [target_deck.pop(self.first_card_i) if self.first_card_i is not None else None]
        self.next_color = self.stack[-1][:self.stack[-1].index("_")] if self.stack[-1] is not None else None
        self.next_number = self.stack[-1][self.stack[-1].index("_") + 1:] if self.stack[-1] is not None else None

    def add(self, card, color_choice=None):
        self.stack.append(card)
        if color_choice is None:
            if "_" not in card:
                return (False, "error: undefined color choice for uncolored card")
            self.next_color = self.stack[-1][:self.stack[-1].index("_")]
            next_number = self.stack[-1][self.stack[-1].index("_") + 1:]
            self.next_number = next_number
            return (True, "card successfully added to table")
        self.next_color = color_choice
        self.next_number = None
        return (True, "card successfully added to table")

    def refill_deck(self, target_deck):
        target_deck.extend(self.stack[:-1])
        random.shuffle(target_deck)
        self.stack = [self.stack[-1]]

    def check_attack_state(self, users, turn, direction, target_deck):
        card = self.stack[-1]
        if "_" not in card:
            return (False, "no action card", turn, direction)

        card_action = card[card.index("_") + 1:]
        if card_action.isdigit():
            return (False, "no action card", turn, direction)

        if card_action in ["draw4", "draw2"]:
            next_user = (turn + direction) % len(users)
            num_draws = int(card_action[-1])
            for _ in range(num_draws):
                users[next_user].draw(target_deck, self)
            message = f"{users[next_user].name} draws {num_draws}"
            return (True, message, turn + direction, direction)
        elif card_action == "skip":
            return (True, f"{users[(turn + direction) % len(users)].name} is skipped", turn + direction, direction)
        elif card_action == "reverse":
            return (True, "direction is reversed", turn, -direction)

    def card_is_compatible(self, card):
        if "wild" in card:
            return True
        if "_" not in card:
            return False
        elif card[:card.index("_")] == self.next_color or card[card.index("_") + 1:] == self.next_number:
            return True
        return False

deck = []

for i in "red green blue yellow".split():
    deck.extend([f"{i}_{j}" for j in range(10)])
    deck.extend([f"{i}_{j}" for j in range(1, 10)])
    for _ in range(2):
        deck.extend([f"{i}_{j}" for j in "skip reverse draw2".split()])
    deck.extend(["wild", "wild_draw4"])

applied_deck = [card for card in deck]
random.shuffle(applied_deck)
