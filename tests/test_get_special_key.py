import pytest

from pydoll.common.keyboard import Keyboard


@pytest.mark.parametrize(
    'key, modifiers, expected',
    [
        ('A', 8, 'A'),
        ('a', 8, 'A'),
        ('.', 2, '.'),
        ('-', 8, '_'),
        ('?', 0, '?'),
        ('7', 8, '&'),
        ('Shift', 8, ''),
    ],
)
def test_get_special_key(key, modifiers, expected):
    result = Keyboard.get_special_key(key, modifiers, 8)
    assert result == expected
