from pydoll.common.keyboard import Keyboard


class InputCommands:
    """
    A class to define input commands for simulating user interactions
    with the browser using the Chrome DevTools Protocol (CDP).
    The commands allow for simulating mouse clicks and keyboard presses.
    """

    CLICK_ELEMENT_TEMPLATE = {
        'method': 'Input.dispatchMouseEvent',
        'params': {},
    }
    KEY_PRESS_TEMPLATE = {'method': 'Input.dispatchKeyEvent', 'params': {}}
    INSERT_TEXT_TEMPLATE = {'method': 'Input.insertText', 'params': {}}
    KEYBOARD = Keyboard()

    @classmethod
    def mouse_press(cls, x: int, y: int) -> dict:
        """
        Generates the command to simulate pressing the mouse button on a
        specific location.

        Args:
            x (int): The x-coordinate of the mouse press.
            y (int): The y-coordinate of the mouse press.

        This command utilizes the CDP to simulate a mouse press event at
        the specified coordinates.

        Returns:
            dict: The command to be sent to the browser.
        """
        command = cls.CLICK_ELEMENT_TEMPLATE.copy()
        command['params'] = {
            'type': 'mousePressed',
            'button': 'left',
            'x': x,
            'y': y,
            'clickCount': 1,
            'modifiers': 0,
        }
        return command

    @classmethod
    def mouse_release(cls, x: int, y: int) -> dict:
        """
        Generates the command to simulate releasing the mouse button.

        Args:
            x (int): The x-coordinate of the mouse release.
            y (int): The y-coordinate of the mouse release.

        This command uses the CDP to simulate a mouse release event at
        the specified coordinates.

        Returns:
            dict: The command to be sent to the browser.
        """
        command = cls.CLICK_ELEMENT_TEMPLATE.copy()
        command['params'] = {
            'type': 'mouseReleased',
            'button': 'left',
            'x': x,
            'y': y,
            'clickCount': 1,
            'modifiers': 0,
        }
        return command

    @classmethod
    def key_press(cls, char: str) -> dict:
        """
        Generates the command to simulate pressing a key on the keyboard.

        Args:
            char (str): The character to be pressed.

        This command utilizes the CDP to simulate a keyboard event for
        the specified character.

        Returns:
            dict: The command to be sent to the browser.
        """
        command = cls.KEY_PRESS_TEMPLATE.copy()
        command['params'] = {
            'type': 'char',
            'text': char,
        }
        return command

    @classmethod
    def insert_text(cls, text: str) -> dict:
        """
        Generates the command to insert text into an input field.

        Args:
            text (str): The text to be inserted.

        This command uses the CDP to simulate typing text into an input field.

        Returns:
            dict: The command to be sent to the browser.
        """
        command = cls.INSERT_TEXT_TEMPLATE.copy()
        command['params'] = {
            'text': text,
        }
        return command

    @classmethod
    def key_down(cls, key: list | tuple, command_id: int) -> dict:
        """
        Generates the command to simulate pressing a key on the keyboard.

        This method creates a command following the Chrome DevTools
            Protocol (CDP)
        to simulate a "keyDown" event, which represents pressing a key.

        Args:
            key (list | tuple): The key and code of the key to be pressed.
            command_id (int): The id of the command to be sent.

        Returns:
            dict: A dictionary containing the command to be sent to
                the browser.
        """
        key, key_code = key
        if key in cls.KEYBOARD.MODIFIER_KEYS:
            cls.KEYBOARD.modifiers.add(key)

        modifiers = sum(
            cls.KEYBOARD.MODIFIER_KEYS[k] for k in cls.KEYBOARD.modifiers
        )

        special_key = cls.KEYBOARD.get_special_key(key, modifiers, key_code)
        vk_code = cls.KEYBOARD.SHIFT_SPECIAL.get(special_key, key_code)
        special_code = cls.KEYBOARD.get_special_code(key)

        key_down = {
            'type': 'keyDown',
            'key': key,
            'code': special_code,
            'windowsVirtualKeyCode': vk_code,
            'modifiers': modifiers,
            'text': special_key,
        }

        command = cls.KEY_PRESS_TEMPLATE.copy()
        command['id'] = command_id
        command['params'] = key_down
        return command

    @classmethod
    def key_up(cls, key: list | tuple, command_id) -> dict:
        """
        Generates the command to simulate releasing a key on the keyboard.

        This method creates a command following the Chrome DevTools
            Protocol (CDP)
        to simulate a "keyUp" event, which represents releasing a key.

        Args:
            key (list | tuple): The character of the key to be released.
            command_id (int): The id of the command to be sent.

        Returns:
            dict: A dictionary containing the command to be sent to
                the browser.
        """
        key, key_code = key
        if key in cls.KEYBOARD.MODIFIER_KEYS:
            cls.KEYBOARD.modifiers.discard(key)

        modifiers = sum(
            cls.KEYBOARD.MODIFIER_KEYS[k] for k in cls.KEYBOARD.modifiers
        )

        special_key = cls.KEYBOARD.SHIFT_MAP.get(key, key)
        vk_code = cls.KEYBOARD.SHIFT_SPECIAL.get(special_key, key_code)
        special_code = cls.KEYBOARD.get_special_code(key)

        key_up = {
            'type': 'keyUp',
            'key': key,
            'code': special_code,
            'windowsVirtualKeyCode': vk_code,
            'modifiers': modifiers,
        }

        command = cls.KEY_PRESS_TEMPLATE.copy()
        command['id'] = command_id
        command['params'] = key_up
        return command
