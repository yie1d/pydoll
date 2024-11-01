import asyncio
import random

from pydoll.commands.dom import DomCommands
from pydoll.commands.input import InputCommands
from pydoll.connection import ConnectionHandler


class WebElement:
    def __init__(self, node: dict, connection_handler: ConnectionHandler):
        """
        Initializes the WebElement instance.

        Args:
            node (dict): The node description from the browser.
            connection_handler (ConnectionHandler): The connection handler instance.
        """
        self._node = node
        self._connection_handler = connection_handler
        self._attributes = {}
        self._def_attributes()

    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self._attributes.items())
        return f'{self.__class__.__name__}({attrs})'

    @property
    async def bounds(self) -> list:
        """
        Asynchronously retrieves the bounding box of the element.

        Returns:
            dict: The bounding box of the element.
        """
        response = await self._connection_handler.execute_command(
            DomCommands.box_model(self._node['nodeId'])
        )
        return response['result']['model']['content']

    def _def_attributes(self):
        attr = self._node['attributes']
        for i in range(0, len(attr), 2):
            key = attr[i]
            key = key if key != 'class' else 'class_name'
            value = attr[i + 1]
            self._attributes[key] = value

            setattr(self, key, value)

    async def click(self, x_offset: int = 0, y_offset: int = 0):
        element_bounds = await self.bounds
        position_to_click = self._calculate_center(element_bounds)
        position_to_click = (
            position_to_click[0] + x_offset,
            position_to_click[1] + y_offset
        )
        press_command = InputCommands.mouse_press(*position_to_click)
        release_command = InputCommands.mouse_release(*position_to_click)
        await self._connection_handler.execute_command(press_command)
        await asyncio.sleep(0.1)
        await self._connection_handler.execute_command(release_command)

    async def send_keys(self, text: str):
        """
        Sends a sequence of keys to the element.

        Args:
            text (str): The text to send to the element.
        """
        for char in text:
            await self._connection_handler.execute_command(
                InputCommands.key_press(char)
            )
            await asyncio.sleep(0.1)

    @staticmethod
    def _calculate_center(bounds: list) -> tuple:
        x_values = [bounds[i] for i in range(0, len(bounds), 2)]
        y_values = [bounds[i] for i in range(1, len(bounds), 2)]
        x_center = sum(x_values) / len(x_values)
        y_center = sum(y_values) / len(y_values)
        return x_center, y_center
