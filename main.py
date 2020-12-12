import asyncio
import sys
import threading

from monkey_patched.game import Game

# Init components
game = Game()


def start_server(loop):
    from backend.server import main

    threading.Thread(target=main, args=(loop,)).start()


def test_server(loop, rand_sleep=False):
    from api_tester import ApiTester

    threading.Thread(target=ApiTester(loop, rand_sleep=rand_sleep).start_test).start()


def run_ui():
    from board_drawing import BDManager

    BDManager()


if __name__ == '__main__':
    _loop = asyncio.get_event_loop()
    start_server(_loop)
    if sys.argv.__len__() > 1 and sys.argv[1] == 'test':
        test_server(_loop, rand_sleep=False)
    run_ui()
