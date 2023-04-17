import sys

from prompt import main

if __name__ == '__main__':

    try:
        main()

    except KeyboardInterrupt :
        print('Exit')
        sys.exit()

    except EOFError :
        print('Exit')
        sys.exit()
    finally:
        print('Exiting program.')
