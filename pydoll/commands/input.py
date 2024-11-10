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
