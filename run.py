#!/bin/python3
import sys

from prompt import main

if __name__ == '__main__':

    try:
        main()

    except KeyboardInterrupt :
        sys.exit()
    except EOFError :
        sys.exit()

    finally:
        print('Exiting program.')
