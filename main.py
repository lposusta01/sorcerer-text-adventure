"""
    SUMMONER - A short metatext adventure
    Elizabeth Posusta - Sep 2026
"""
import os, threading
import math, time

from enum import Enum
from pathlib import Path

from text_rendering import Renderer

class Script:
    _raw: str = Path("assets/script").read_text()

    _populated: dict[str, str] = dict()
    _index: str = "START"   

    def __init__(self):
        for line in self._raw.split("~LINE"):
            try:
                self._populated[line.split(" ")[1]] = line.split(" ")[2:]
            except:
                pass

    def update(self, i: str):
        self._index = i

    def current(self):
        return self._populated[self._index.split("\n")[0]]

    def get_index(self):
        return self._index

"""
    The parser's state. This enum exists for the convenience of enforcing the following
        order of inputs:

        TRIGGER, CLEAR -> SELECT -> SELECT -> ... -> PROMPT

        before prompting the user and updating the Script
"""
class PState(Enum):
    PRE_PROMPT = 0
    SELECT = 1
    PROMPT = 2

    def from_str(self, string: str):
        if string[0] == "~":
            match string:
                case "~SELECT":
                    return self.SELECT
                case "~PROMPT":
                    return self.PROMPT
            return self.PRE_PROMPT

    """
        Encode valid state changes.

        This is disgusting, but I'm in a bit of a rush, so it will do for now.
    """
    def is_valid(self, state_a: PState, state_b: PState) -> bool:
        if state_a == self.PRE_PROMPT and state_b == self.PRE_PROMPT or state_a == self.PRE_PROMPT and state_b == self.SELECT or state_a == self.SELECT and state_b == self.PROMPT or state_a == self.SELECT and state_b == self.SELECT:
                return True
        return False

    def reset(self):
        return self.PRE_PROMPT

class Parser:
    _script: Script = Script()
    _state: PState = PState.PRE_PROMPT
    _word_index: int = 0
    _r: Renderer = Renderer(_script.current())
    _smap: dict[str, str] = dict()

    def __init__(self, s: Script):
        self._script = s

    def _exec_for(self, state: str):

        if "\n" in state or " " in state:
            if "~PROMPT" in state:
                state = "~PROMPT"
                
        match state:
            case "~CLEAR":
                pass
            case "~SELECT":
                self._smap[self._script.current()[self._word_index + 1]] = self._script.current()[self._word_index + 2]
            case "~PROMPT":
                self._r.render()
                while True:
                    next: str = input("== CHOOSE AN OPTION: \n\t>")
                    try:
                        self._script.update(self._smap[next])
                        break
                    except:
                        print("Bad input! Try again", self._smap)
                        continue
                self._state = self._state.reset()
                self._smap = {}


    def _switch(self, new_state: str) -> bool:
        if "~END" in new_state:
            self._r.render()
            os.system("clear")
            print("thanks for playing!")
            exit(0)
        if "~" in new_state:
            if "\n" in new_state or " " in new_state:
                if "~PROMPT" in new_state:
                    new_state = "~PROMPT"
                    # Manually covering the case where prompt is on its own line
                    # and does not come after a space on the previous line
                    #
                    # This would not be an issue if I had just remembered
                    # to split the file on newlines as well, but I'm not
                    # about to rework everything in the name of a relatively
                    # -m-i-n-o-r--p-r-o-b-l-e-m- TERRIBLE OVERSIGHT
            if self._state.is_valid(self._state, self._state.from_str(new_state)):
                self._state = self._state.from_str(new_state)
                return True
            else:
                print(f"Script syntax error. Attempt to switch from {self._state} to {new_state} states at line index \"{self._script.get_index()}\"")
                exit()
        return False

    def _advance(self) -> bool:
        self._r.update(self._script.current())
        try:
            if self._switch(self._script.current()[self._word_index]):
                self._exec_for(self._script.current()[self._word_index])
            self._word_index += 1
            return True
        except:
            return False

    def run(self):
        self._smap = dict()
        self._word_index = 0
        while self._advance():
            pass               

def advance(r: Renderer, p: Parser, s: Script):
    p.run()
    _ = input(". . .")

def main() -> None:
    s: Script = Script()
    p: Parser = Parser(s)
    r: Renderer = Renderer(s.current())

    while True:
        advance(r, p, s)

if __name__ == "__main__":
    main()
