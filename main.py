from wordel import Wordel
import argparse


parser = argparse.ArgumentParser(description="Wordle but bad.")
parser.add_argument("--hard", action="store_true", help="Enable hard mode.")
parser.add_argument("--debug", action="store_true", help="Debug.")
parser.add_argument("--ans", default=None, help="Set the answer to a specific word.")
args = parser.parse_args()

w = Wordel(hard=args.hard, debug=args.debug)
w.run(ans=args.ans)
