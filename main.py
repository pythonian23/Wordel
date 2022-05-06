#!/usr/bin/python3

from wordel import Wordel
import argparse


parser = argparse.ArgumentParser(description="Wordle but bad.")
parser.add_argument("--hard", "-H", action="store_true", help="Enable hard mode")
parser.add_argument("--debug", "-d", action="store_true", help="Debug")
parser.add_argument("--answer", "-A", default=None, help="Set the answer to a specific word")
parser.add_argument("--chars", "-c", default=5, help="The number of characters per row")
parser.add_argument("--attempts", "-a", default=-1, help="The number of attempts to allow")
args = parser.parse_args()

w = Wordel(hard=args.hard, debug=args.debug, length=int(args.chars), attempts=int(args.attempts))
w.run(ans=args.answer)
