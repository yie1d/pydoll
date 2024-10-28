class InputCommands:
    CLICK_ELEMENT_TEMPLATE = {
        'method': 'Input.dispatchMouseEvent',
        'params': {},
    }
    KEY_PRESS_TEMPLATE = {'method': 'Input.dispatchKeyEvent', 'params': {}}

    @classmethod
    def mouse_press(cls, x: int, y: int) -> dict:
        """
        Generates the command to click on a specific element.

        Args:
            dom_id (int): The ID of the element to click.
            x (int): The x-coordinate of the click.
            y (int): The y-coordinate of the click.

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
        Generates the command to release the mouse button.

        Args:
            x (int): The x-coordinate of the release.
            y (int): The y-coordinate of the release.

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
        Generates the command to press a key on the keyboard.

        Args:
            char (str): The character to press.

        Returns:
            dict: The command to be sent to the browser.
        """
        command = cls.KEY_PRESS_TEMPLATE.copy()
        command['params'] = {
            'type': 'char',
            'text': char,
        }
        return command
