# -*- coding: utf-8 -*-

"""
This file holds information about the pygame event, the asci value and the common name for the keys
Also it holds information about special keys, such as enter, backspace and escape.
"""

import pygame

keys = {
    pygame.K_SPACE: (' ', 'space'),
    pygame.K_EXCLAIM: ('!', 'exclaim'),
    pygame.K_QUOTEDBL: ('"', 'quotedbl'),
    pygame.K_HASH: ('#', 'hash'),
    pygame.K_DOLLAR: ('$', 'dollar'),
    pygame.K_AMPERSAND: ('&', 'ampersand'),
    pygame.K_LEFTPAREN: ('(', 'left parenthesis'),
    pygame.K_RIGHTPAREN: (')', 'right parenthesis'),
    pygame.K_ASTERISK: ('*', 'asterisk'),
    pygame.K_PLUS: ('+', 'plus sign'),
    pygame.K_COMMA: (',', 'comma'),
    pygame.K_MINUS: ('-', 'minus sign'),
    pygame.K_PERIOD: ('.', 'period'),
    pygame.K_SLASH: ('/', 'forward slash'),
    pygame.K_0: ('0', '0'),
    pygame.K_1: ('1', '1'),
    pygame.K_2: ('2', '2'),
    pygame.K_3: ('3', '3'),
    pygame.K_4: ('4', '4'),
    pygame.K_5: ('5', '5'),
    pygame.K_6: ('6', '6'),
    pygame.K_7: ('7', '7'),
    pygame.K_8: ('8', '8'),
    pygame.K_9: ('9', '9'),
    pygame.K_COLON: (':', 'colon'),
    pygame.K_SEMICOLON: (';', 'semicolon'),
    pygame.K_LESS: ('<', 'less-than sign'),
    pygame.K_EQUALS: ('=', 'equals sign'),
    pygame.K_GREATER: ('>', 'greater-than sign'),
    pygame.K_QUESTION: ('?', 'question mark'),
    pygame.K_AT: ('@', 'at'),
    pygame.K_LEFTBRACKET: ('[', 'left bracket'),
    pygame.K_BACKSLASH: ('\'', 'backslash'),
    pygame.K_RIGHTBRACKET: (']', 'right bracket'),
    pygame.K_CARET: ('^', 'caret'),
    pygame.K_UNDERSCORE: ('_', 'underscore'),
    pygame.K_BACKQUOTE: ('`', 'grave'),
    pygame.K_a: ('a', 'a'),
    pygame.K_b: ('b', 'b'),
    pygame.K_c: ('c', 'c'),
    pygame.K_d: ('d', 'd'),
    pygame.K_e: ('e', 'e'),
    pygame.K_f: ('f', 'f'),
    pygame.K_g: ('g', 'g'),
    pygame.K_h: ('h', 'h'),
    pygame.K_i: ('i', 'i'),
    pygame.K_j: ('j', 'j'),
    pygame.K_k: ('k', 'k'),
    pygame.K_l: ('l', 'l'),
    pygame.K_m: ('m', 'm'),
    pygame.K_n: ('n', 'n'),
    pygame.K_o: ('o', 'o'),
    pygame.K_p: ('p', 'p'),
    pygame.K_q: ('q', 'q'),
    pygame.K_r: ('r', 'r'),
    pygame.K_s: ('s', 's'),
    pygame.K_t: ('t', 't'),
    pygame.K_u: ('u', 'u'),
    pygame.K_v: ('v', 'v'),
    pygame.K_w: ('w', 'w'),
    pygame.K_x: ('x', 'x'),
    pygame.K_y: ('y', 'y'),
    pygame.K_z: ('z', 'z'),
    pygame.K_KP0: ('0', 'keypad 0'),
    pygame.K_KP1: ('1', 'keypad 1'),
    pygame.K_KP2: ('2', 'keypad 2'),
    pygame.K_KP3: ('3', 'keypad 3'),
    pygame.K_KP4: ('4', 'keypad 4'),
    pygame.K_KP5: ('5', 'keypad 5'),
    pygame.K_KP6: ('6', 'keypad 6'),
    pygame.K_KP7: ('7', 'keypad 7'),
    pygame.K_KP8: ('8', 'keypad 8'),
    pygame.K_KP9: ('9', 'keypad 9'),
    pygame.K_KP_PERIOD: ('.', 'keypad period'),
    pygame.K_KP_DIVIDE: ('/', 'keypad divide'),
    pygame.K_KP_MULTIPLY: ('*', 'keypad multiply'),
    pygame.K_KP_MINUS: ('-', 'keypad minus'),
    pygame.K_KP_PLUS: ('+', 'keypad plus'),
    pygame.K_KP_EQUALS: ('=', 'keypad equals')
    }

keys_special = {
    pygame.K_ESCAPE: ('', 'escape'),  # ^[
    pygame.K_KP_ENTER: ('', 'keypad enter'),  # \r
    pygame.K_RETURN: ('', 'return'),  # \r
    pygame.K_BACKSPACE: ('', 'backspace'),  # \b
    pygame.K_TAB: ('', 'tab'),  # \t
    pygame.K_DELETE: ('', 'delete'),
    pygame.K_UP: ('', 'up arrow'),
    pygame.K_DOWN: ('', 'down arrow'),
    pygame.K_RIGHT: ('', 'right arrow'),
    pygame.K_LEFT: ('', 'left arrow'),
    pygame.K_INSERT: ('', 'insert'),
    pygame.K_HOME: ('', 'home'),
    pygame.K_END: ('', 'end'),
    pygame.K_PAGEUP: ('', 'page up'),
    pygame.K_PAGEDOWN: ('', 'page down'),
    pygame.K_F1: ('', 'F1'),
    pygame.K_F2: ('', 'F2'),
    pygame.K_F3: ('', 'F3'),
    pygame.K_F4: ('', 'F4'),
    pygame.K_F5: ('', 'F5'),
    pygame.K_F6: ('', 'F6'),
    pygame.K_F7: ('', 'F7'),
    pygame.K_F8: ('', 'F8'),
    pygame.K_F9: ('', 'F9'),
    pygame.K_F10: ('', 'F10'),
    pygame.K_F11: ('', 'F11'),
    pygame.K_F12: ('', 'F12'),
    pygame.K_F13: ('', 'F13'),
    pygame.K_F14: ('', 'F14'),
    pygame.K_F15: ('', 'F15'),
    pygame.K_NUMLOCK: ('', 'numlock'),
    pygame.K_CAPSLOCK: ('', 'capslock'),
    pygame.K_SCROLLOCK: ('', 'scrollock'),
    pygame.K_RSHIFT: ('', 'right shift'),
    pygame.K_LSHIFT: ('', 'left shift'),
    pygame.K_RCTRL: ('', 'right ctrl'),
    pygame.K_LCTRL: ('', 'left ctrl'),
    pygame.K_RALT: ('', 'right alt'),
    pygame.K_LALT: ('', 'left alt'),
    pygame.K_RMETA: ('', 'right meta'),
    pygame.K_LMETA: ('', 'left meta'),
    pygame.K_LSUPER: ('', 'left windows key'),
    pygame.K_RSUPER: ('', 'right windows key'),
    pygame.K_MODE: ('', 'mode shift'),
    pygame.K_HELP: ('', 'help'),
    pygame.K_PRINT: ('', 'print screen'),
    pygame.K_SYSREQ: ('', 'sysrq'),
    pygame.K_BREAK: ('', 'break'),
    pygame.K_MENU: ('', 'menu'),
    pygame.K_POWER: ('', 'power'),
    pygame.K_EURO: ('', 'euro')
    }
