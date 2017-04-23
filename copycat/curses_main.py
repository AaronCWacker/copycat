import argparse
import curses
import logging
import sys

from copycat import Copycat
from curses_reporter import CursesReporter


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s', filename='./copycat.log', filemode='w')

    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None, help='Provide a deterministic seed for the RNG.')
    parser.add_argument('initial', type=str, help='A...')
    parser.add_argument('modified', type=str, help='...is to B...')
    parser.add_argument('target', type=str, help='...as C is to... what?')
    options = parser.parse_args()

    try:
        window = curses.initscr()
        copycat = Copycat(reporter=CursesReporter(window), rng_seed=options.seed)
        copycat.run_forever(options.initial, options.modified, options.target)
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()
