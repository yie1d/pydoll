from pydoll.commands import InputCommands
from pydoll.common.keys import Keys


def test_send_ctrl_key():
    key, code = Keys.CONTROL
    keydown_command = {
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'type': 'keyDown',
            'key': key,
            'code': 'ControlLeft',
            'windowsVirtualKeyCode': code,
            'modifiers': 2,
            'text': ''
        },
        'id': 1
    }
    assert InputCommands.key_down(Keys.CONTROL, 1) == keydown_command

    keyup_command = {
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'type': 'keyUp',
            'key': key,
            'code': 'ControlLeft',
            'windowsVirtualKeyCode': code,
            'modifiers': 0
        },
        'id': 2
    }
    assert InputCommands.key_up(Keys.CONTROL, 2) == keyup_command


def test_send_backspace_key():
    key, code = Keys.BACKSPACE

    keydown_command = {
        'id': 1,
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'code': 'Backspace',
            'key': key,
            'modifiers': 0,
            'text': '',
            'type': 'keyDown',
            'windowsVirtualKeyCode': 8,
        },
    }

    assert InputCommands.key_down(Keys.BACKSPACE, 1) == keydown_command

    keyup_command = {
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'type': 'keyUp',
            'key': key,
            'code': 'Backspace',
            'windowsVirtualKeyCode': code,
            'modifiers': 0
        },
        'id': 2
    }
    assert InputCommands.key_up(Keys.BACKSPACE, 2) == keyup_command


def test_send_escape_key():
    key, code = Keys.ESCAPE

    keydown_command = {
        'id': 1,
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'code': 'Escape',
            'key': key,
            'modifiers': 0,
            'text': '',
            'type': 'keyDown',
            'windowsVirtualKeyCode': 27,
        },
    }

    assert InputCommands.key_down(Keys.ESCAPE, 1) == keydown_command

    keyup_command = {
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'type': 'keyUp',
            'key': key,
            'code': 'Escape',
            'windowsVirtualKeyCode': code,
            'modifiers': 0
        },
        'id': 2
    }
    assert InputCommands.key_up(Keys.ESCAPE, 2) == keyup_command


def test_send_shift_key():
    key, code = Keys.SHIFT

    keydown_command = {
        'id': 1,
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'code': 'ShiftLeft',
            'key': key,
            'modifiers': 8,
            'text': '',
            'type': 'keyDown',
            'windowsVirtualKeyCode': 16,
        },
    }

    assert InputCommands.key_down(Keys.SHIFT, 1) == keydown_command

    keyup_command = {
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'type': 'keyUp',
            'key': key,
            'code': 'ShiftLeft',
            'windowsVirtualKeyCode': code,
            'modifiers': 0
        },
        'id': 2
    }
    assert InputCommands.key_up(Keys.SHIFT, 2) == keyup_command


def test_send_alt_key():
    key, code = Keys.ALT

    keydown_command = {
        'id': 1,
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'code': 'AltLeft',
            'key': key,
            'modifiers': 1,
            'text': '',
            'type': 'keyDown',
            'windowsVirtualKeyCode': 18,
        },
    }
    assert InputCommands.key_down(Keys.ALT, 1) == keydown_command

    keyup_command = {
        'method': 'Input.dispatchKeyEvent',
        'params': {
            'type': 'keyUp',
            'key': key,
            'code': 'AltLeft',
            'windowsVirtualKeyCode': code,
            'modifiers': 0
        },
        'id': 2
    }
    assert InputCommands.key_up(Keys.ALT, 2) == keyup_command
