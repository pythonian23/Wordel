import os
import random

import colorama
import requests
import hashlib

import utils


# Constants for color
WHITE = colorama.Fore.WHITE
GREY = colorama.Fore.WHITE + colorama.Style.DIM
YELLOW = colorama.Fore.YELLOW + colorama.Style.BRIGHT
GREEN = colorama.Fore.GREEN + colorama.Style.BRIGHT


def get_words(source, length, allowed, mod=(lambda x: x)):
    """
    get_words
    """
    cache_file = "cache/" + hashlib.sha256(source.encode("ascii")).hexdigest() + ".cache"
    if os.path.exists(cache_file):
        file = open(cache_file).read()
    else:
        file = requests.get(source).text
        with open(cache_file, "w") as f:
            f.write(file)

    words = []
    for word in file.split("\n"):
        word = mod(word)
        invalid = False

        invalid = invalid or len(word) != length
        if not invalid:
            for char in word:
                invalid = invalid or (char not in allowed)
        if invalid:
            continue
        words.append(word)
    return words


class Wordel:
    def __init__(self, *args, **kwargs):
        source, self.length, self.allowed, self.hard, self.debug, self.attempts \
            = utils.kwarg_parser({
            "source": "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt",
            "length": 5,
            "allowed": "qwertyuiopasdfghjklzxcvbnm",
            "hard": False,
            "debug": False,
            "attempts": -1,
        }, **kwargs)
        self.words = get_words(source, self.length, self.allowed, mod=(lambda x: x.lower()))

    def run(self, ans=None):
        def check_hard(data, check):
            if not self.hard:
                return True
            for i, char in check:
                if i == -1:
                    if not char in data:
                        return False
                elif not data[i] == char:
                    return False
            return True

        guesses = []
        known = []
        word: str
        if ans is None:
            word = random.choice(self.words)
        else:
            word = ans
        utils.clear()
        i = 0

        keyboard = {c: WHITE for c in self.allowed}

        def upgrade_keyboard(key, color):
            if keyboard[key] == WHITE:
                keyboard[key] = color
            elif keyboard[key] == GREY and color != WHITE:
                keyboard[key] = color
            elif keyboard[key] == YELLOW and color != GREY and color != WHITE:
                keyboard[key] = color

        def format_keyboard():
            out = []
            items = list(keyboard.items())
            out.append(
                " ".join([color + key + colorama.Style.RESET_ALL for key, color in items[0:len(items) // 3 + 2]]))
            out.append(" " + " ".join([color + key + colorama.Style.RESET_ALL for key, color in
                                       items[len(items) // 3 + 2:2 * (len(items) // 3) + 3]]))
            out.append("  " + " ".join(
                [color + key + colorama.Style.RESET_ALL for key, color in items[2 * (len(items) // 3) + 3:]]))
            return "\n".join(out)

        show = lambda: word * int(self.debug) + str(known) * int(self.debug) + colorama.Fore.BLUE + "=" * (
                    self.length * 2 - 1) + colorama.Style.RESET_ALL + "\n" + "\n".join(
            guesses + [" ".join([WHITE + "-" + colorama.Style.RESET_ALL] * (self.length)) for _ in
                       range(remaining)]) + "\n" + colorama.Fore.BLUE + "=" * (
                                   self.length * 2 - 1) + colorama.Style.RESET_ALL + f"\n{colorama.Fore.MAGENTA}{remaining}{colorama.Fore.CYAN} guesses remaining.{colorama.Style.RESET_ALL}\n{format_keyboard()}\n> "
        if self.attempts == -1:
            attempts = self.length + 1
        else:
            attempts = self.attempts
        for remaining in range(attempts, 0, -1):
            while True:
                i += 1
                inp = input(show()).lower()
                if not inp in self.words:
                    utils.clear()
                    print(
                        colorama.Fore.RED + "You're an idiot >:(((. That isn't a valid word." + colorama.Style.RESET_ALL)
                    continue
                if not check_hard(inp, known):
                    utils.clear()
                    print(colorama.Fore.RED + "You're an idiot >:(((. You're on hard mode." + colorama.Style.RESET_ALL)
                    continue
                formatted = []
                found = {c: 0 for c in word}
                for i, char in enumerate(inp):
                    if char in word:
                        found[char] += 1
                        if found[char] > word.count(char):
                            formatted.append(GREY + char + colorama.Style.RESET_ALL)
                            continue
                    if char == word[i]:
                        upgrade_keyboard(char, GREEN)
                        formatted.append(GREEN + char + colorama.Style.RESET_ALL)
                        known.append((i, char))
                    elif char in word:
                        upgrade_keyboard(char, YELLOW)
                        formatted.append(YELLOW + char + colorama.Style.RESET_ALL)
                        known.append((-1, char))
                    else:
                        upgrade_keyboard(char, GREY)
                        formatted.append(GREY + char + colorama.Style.RESET_ALL)
                guesses.append(" ".join(formatted))
                if inp == word:
                    print(show())
                    print(GREEN + "You actually did it :)))" + colorama.Style.RESET_ALL)
                    return
                utils.clear()
                break

        input(YELLOW + f"You used all of your guesses :((((. The word was \"{word}\"" + colorama.Style.RESET_ALL)
