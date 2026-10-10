import termios, sys, os, time
from PIL import Image, ImageOps

TERM_WIDTH: int = termios.tcgetwinsize(sys.stdout.fileno())[1]
TERM_HEIGHT: int = termios.tcgetwinsize(sys.stdout.fileno())[0]
# Termios using (y, x) is maybe the single most infuriating
# API design decision of all time.

SCREEN_WIDTH: int = TERM_WIDTH - int(TERM_WIDTH / 4)
SCREEN_HEIGHT: int = TERM_HEIGHT - int(TERM_HEIGHT / 2)
SCREEN_TOP_LEFT: list[int] = [int((TERM_WIDTH - SCREEN_WIDTH) / 2), int((TERM_HEIGHT - SCREEN_HEIGHT) / 2)]
SCREEN_BOTTOM_RIGHT: list[int] = [SCREEN_WIDTH + SCREEN_TOP_LEFT[0], SCREEN_HEIGHT + SCREEN_TOP_LEFT[1]]

class Renderer:
    _mute: bool = False
    _onscreen: str = ""
    
    def __init__(self, s: list[str]):
        for word in s:
            if word != "":
                self._onscreen += (word + " ")

    def update(self, s: list[str]):
        self._onscreen = ""
        for word in s:
            if word != "":
                self._onscreen += (word + " ")

    def render(self) -> None:
        ch: int = 0
        for y in range(TERM_HEIGHT):
            for x in range(TERM_WIDTH):
                if SCREEN_BOTTOM_RIGHT[0] >= x >= SCREEN_TOP_LEFT[0] and SCREEN_BOTTOM_RIGHT[1] >= y >= SCREEN_TOP_LEFT[1]:
                    try:
                        print(self._onscreen[ch], end="")
                        if self._onscreen[ch] == "\n":
                            print()
                            for _ in range(SCREEN_TOP_LEFT[0]):
                                print(" ", end="")
                        ch += 1
                    except:
                        pass
                else:
                    print(" ", end="")
        _ = input()
