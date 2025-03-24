from pydoll.common.keys import Keys


class Keyboard(Keys):
    MODIFIER_KEYS = {'Alt': 1, 'Control': 2, 'Meta': 4, 'Shift': 8}
    SHIFT_MAP = {
        '1': '!',
        '2': '@',
        '3': '#',
        '4': '$',
        '5': '%',
        '6': '^',
        '7': '&',
        '8': '*',
        '9': '(',
        '0': ')',
        '-': '_',
        '=': '+',
        '[': '{',
        ']': '}',
        '\\': '|',
        ';': ':',
        "'": '"',
        ',': '<',
        '.': '>',
        '/': '?',
    }
    SHIFT_CODES = {
        '\\': 'Backslash',
        '|': 'Backslash',
        '[': 'BracketLeft',
        ']': 'BracketRight',
        ';': 'Semicolon',
        ':': 'Semicolon',
        '/': 'Slash',
        '?': 'Slash',
        '.': 'Period',
        ',': 'Comma',
        '-': 'Minus',
        '+': 'Equal',
        '=': 'Equal',
    }
    SHIFT_SPECIAL = {
        '?': 63,
        '|': 124,
        '~': 126,
        '+': 43,
        '_': 95,
        ':': 58,
        '!': 33,
        '*': 42,
        '(': 57,
        ')': 41,
        '<': 60,
        '>': 62,
        '.': 190,
    }

    def __init__(self):
        self.modifiers = set()

    @classmethod
    def get_special_key(cls, key: str, modifiers: int, key_code: int) -> str:
        """
        Return the appropriate text value for special keys
        like Shift, Enter, Space, etc.

        Args:
            key (str): The key code of the key to be pressed.
            modifiers (int): The modifiers code of the key to be pressed.
            key_code (int): The key code of the key to be pressed.
        """
        if key_code in cls.SPACE:
            return ' '
        elif key_code in cls.ENTER:
            return '\r'
        elif modifiers & 8 and key != 'Shift':
            return cls.SHIFT_MAP.get(key, key.upper())
        elif len(key) == 1 and key.isprintable():
            return key

        return ''

    @classmethod
    def get_special_code(cls, key) -> str:
        """
        Return the appropriate text value for special keys
        like Shift, Enter, Space, etc.

        Args:
            key (str): The key code of the special key.

        """
        code = cls.SHIFT_CODES.get(key, key)
        key_type = f'Digit{key}' if key.isdigit() else f'Key{key.upper()}'
        if len(key) == 1:
            return key_type
        elif code in cls.MODIFIER_KEYS.keys():
            return f'{code}Left'

        return code
