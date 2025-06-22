import sys
import os
import tty
import termios

def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char

def get_key_input():
    while True:
        sys.stdout.flush()
        char = get_char()

        if char == '\x1b': # Escape sequence start (Unix-like)
            sequence = get_char() + get_char()
            if sequence == '[D': # Left arrow (Unix-like)
                return "left"
            elif sequence == '[C': # Right arrow (Unix-like)
                return "right"
        else:
            return char
