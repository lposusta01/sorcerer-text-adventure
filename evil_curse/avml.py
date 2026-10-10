"""
AdVenture Markup Language (AVML) interpreter(?)
Elizabeth Posusta - Aug 2026
"""

import os, sys, time
from enum import Enum
from pathlib import Path
from collections.abc import Callable

class ParserState(Enum):
    INIT = 0
    PROMPT_SELECT = 1

def populate_dict() -> dict[str, str]:
    script: dict[str, str] = dict()

    text = Path("assets/script").open().read().split("~LINE")

    if not text:
        print("File doesn't exist or otherwise can't be accessed properly")
        exit()

    for line in text:
        if line:
            if line[0] == "#":
                pass

            else:
                line = line.lstrip()

                try:
                    script[line[:line.find(" ")]] = line
                except:
                    pass

    return script

"""
    clear the screen. delay in units of 100ms. defaults to an indefinite delay
"""
def clear_delay(delay: int | None = None): # units of 100ms/.1s
    if delay:
        time.sleep(float(delay) / 10.0)
    else:
        input("... Press Enter to Continue ...")
    os.system("clear")

# chopped function
def trigger(parser: Parser, trigger_function: Callable, start: int, end: int):
    trigger_function(parser, start, end)

# The poor man's parser
class Parser:
    _state: ParserState = ParserState.INIT
    _script: dict[str, str] = populate_dict()
    _index: str = ""
    _trigger_function: Callable = print
    _select_map: dict[str, str]

    token_pos: int = 0
    current_token: str = ""

    def __init__(self, trigger: Callable):
        self._state = ParserState.INIT
        self._script = populate_dict()
        self._select_map = dict()
        self._index = "START"
        self._trigger_function = trigger

    def _valid_input(self, state: ParserState):
        if state == ParserState.PROMPT_SELECT:
                return ("~SELECT", "~PROMPT")    
        else:
                return ("~CLEAR", "~TRIGGER", "~SELECT")

    def _exec_for(self, token: list[str]):
        match token[0]:
            case "~CLEAR":
                try:
                    clear_delay(int(token[1]))
                except:
                    clear_delay()
            case "~TRIGGER":
                try:
                    trigger(self, self._trigger_function, int(token[1]), int(token[2]))
                except:
                    print(f"trigger() expects (int, int), got ({token[1], token[2]})")
                    exit()
            case "~PROMPT":
                while True:
                    try:
                        choice = input()
                        self._index = self._select_map[choice]
                        break
                    except:
                        print(f"Invalid input. Try again bud. (Got {choice} expected one of {self._select_map})")
                        clear_delay()
                        pass
            case "~SELECT":
                try:
                    self._select_map[token[1]] = token[2]
                except:
                    print("im tired of writing error messages")
                    exit()
            case _:
                print("????????????")
                exit()
    
    def try_parse(self) -> None:
        line = self._script[self._index]
        
        pos: int = 0
        
        for token in line.split(" "):
            if token[0] == "~":
                if token in self._valid_input(self._state):
                    # print(f"check passed {token}")

                    if token == "~PROMPT" or token == "~SELECT":
                        self._state = ParserState.PROMPT_SELECT

                    else:
                        self._state = ParserState.INIT
                    if token == "~PROMPT":
                        self.current_token = ""
                        self.token_pos = 0
                                 
                    self._exec_for([token, line.split(" ")[pos + 1], line.split(" ")[pos + 2]])
                    
                else:
                    pass

            else:
                if pos >= 2:
                    if token.isnumeric():
                        if line.split(" ")[pos - 1][0] == "~" or line.split(" ")[pos - 2][0] == "~":
                            pass
                    else:
                        self.current_token += token + " "
                        self.token_pos += len(token)
                elif pos == 1:
                        self.current_token += token + " "
                        self.token_pos += len(token)
                else:
                    pass

            pos += 1
            self._trigger_function(self, 0, 0)

        return None
    
if __name__ == "__main__":
    exit()
