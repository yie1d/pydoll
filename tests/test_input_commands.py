from pydoll.commands import InputCommands
from pydoll.common.keys import Keys


def test_mouse_press():
    x, y = 100, 200
    expected_command = {
        'method': 'Input.dispatchMouseEvent',
        'params': {
            'type': 'mousePressed',
            'button': 'left',
            'x': x,
            'y': y,
            'clickCount': 1,
            'modifiers': 0,
        },
    }
    assert InputCommands.mouse_press(x, y) == expected_command


def test_mouse_release():
    x, y = 100, 200
    expected_command = {
        'method': 'Input.dispatchMouseEvent',
        'params': {
            'type': 'mouseReleased',
            'button': 'left',
            'x': x,
            'y': y,
            'clickCount': 1,
            'modifiers': 0,
        },
    }
    assert InputCommands.mouse_release(x, y) == expected_command


def test_key_press():
    char = 'a'
    expected_command = {
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'type': 'char',
            'text': char,
        },
    }
    assert InputCommands.key_press(char) == expected_command


def test_insert_text():
    text = 'hello'
    expected_command = {
        'method': 'Input.insertText',
        'params': {
            'text': text,
        },
    }
    assert InputCommands.insert_text(text) == expected_command


def test_key_down():
    key, code = Keys.ENTER
    expected_command = {
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'type': 'keyDown',
            'key': key,
            'code': 'Enter',
            'windowsVirtualKeyCode': code,
            'modifiers': 0,
            'text': '\r'
        },
        'id': 1
    }
    assert InputCommands.key_down(Keys.ENTER, 1) == expected_command


def test_key_up():
    key, code = Keys.ENTER
    expected_command = {
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'type': 'keyUp',
            'key': key,
            'code': 'Enter',
            'windowsVirtualKeyCode': code,
            'modifiers': 0
        },
        'id': 2
    }
    assert InputCommands.key_up(Keys.ENTER, 2) == expected_command
