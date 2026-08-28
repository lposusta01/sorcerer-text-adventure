"""
SORCERER - A short work of interactive metafiction
Elizabeth Posusta - Aug 2026
"""

import os, sys, termios, math
from time import sleep
from pathlib import Path
from PIL import Image, ImageOps

import avml
    
term_res: tuple[int, int] = termios.tcgetwinsize(sys.stdin.fileno()) # height, width but PILlow likes width, height
term_width: int = term_res[1]
term_height: int = term_res[0]
textbox_top_left: tuple[int, int] = (int(term_width / 10), int(term_height / 10))
textbox_bottom_right: tuple[int, int] = (5 * textbox_top_left[0], 6 * textbox_top_left[1])

def textmap(string: str, pos: tuple[int, int]): # x, y
    if pos[0] > term_width or pos[1] > term_height: # again, termios does this weird and I'm deciding to stay consistent with PILlow instead
        return None
    else:
        x, y = pos[0], pos[1]
        mapped_text = dict()
        for p in range(0, len(string)):
            if x >= textbox_bottom_right[0]:
                y += 1
                x = pos[0]
            mapped_text[(x, y)] = string[p]
            x += 1
        return mapped_text

def image_prep(image_imported): # for whatever reason I can't specify PIL.Image as a type?
    image = ImageOps.grayscale(image_imported).quantize(5)
    if image.height <= term_res[0] and image.width <= term_res[1]:
        return image, term_res[1]
    else:
        new_width = int(image.width / (image.height / term_res[0]))
        size = (new_width, term_res[0])
        image_tty = image.resize(size)
        return image_tty, term_res[1]

def print_to_tty(parser: avml.Parser, index: int, scriptindex: int):
    pixel = dict({0: "█", 1: "▓", 2: "▒", 3: "░", 4: " "})
    fw = image_prep(Image.open(f"images/{index}.bmp"))
    frame = fw[0]
    width = fw[1]
    for y in range(0, frame.height):
        for x in range(0, width):
            if x >= width - frame.width:
                shade = frame.getpixel(tuple([x - width, y]))
                # I am genuinely lost on why quantize() sets values to {0,1,2,3,4} instead of {0,1,2,3,4}*255/4 or whatever
                # but this DOES work so I will not complain
                # ALSO the shades are inverted??? 4 is darkest, 0 is lightest?? What the hell?
                print(f"{pixel.get(shade)}", end = '')
            else:
                textbox_width: int = abs(textbox_top_left[0] - textbox_bottom_right[0])
                textbox_height: int = abs(textbox_top_left[1] - textbox_bottom_right[1])
                position: tuple[int, int] = textbox_top_left[0] + parser.token_pos % textbox_width, int(textbox_top_left[1] + parser.token_pos / textbox_height)
                if textmap(parser.current_token, textbox_top_left).get((x, y)) != None:
                    print(f"{textmap(parser.current_token, textbox_top_left).get((x, y))}", end = '')
                else:
                    print(" ", end = '')
        print('')
    sleep(0.15) # Keep some semblance of a framerate

def play_anim(parser: avml.Parser, start: int, end: int):
    for frame in range(start, end):
        os.system('clear')
        print_to_tty(parser, frame, 0)

def main() -> None:
    # play_anim(1, 30)
    parser = avml.Parser(play_anim)
    parser.try_parse()
    

if __name__ == "__main__":
    main()
