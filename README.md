# text-based_uno
Text-based Uno card game

How to play:

put the two files, "main.py" and "cards.py" in the same folder, then run "python main.py" in that folder from the terminal.

After entering your name, when it's your turn, you have a bunch of commands you can call (listed in the start of the game).
When using the "put" command, you can either type the numeric location of your card, the literal card name, or a short-hand
notation of the card name in the form of:
w (for wild)
wd (for wild_draw4)
cn (where c is a "color" letter such as yellow, and n is a "number" or "tool" letter, such as 3 or reverse)

for example: yr will convert to yellow_reverse, b4 to blue_4, rr to red_reverse, and gs to green_skip.

it is you against the bots (there are 3 bots, but you can customize the number of bots in the source code by adjusting the "num_bots" variable).
