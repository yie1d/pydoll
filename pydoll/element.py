import asyncio

from pydoll.commands.dom import DomCommands
from pydoll.commands.input import InputCommands
from pydoll.connection import ConnectionHandler
from pydoll.constants import By

class WebElement:
    def __init__(self, node: dict, connection_handler: ConnectionHandler, method: str = None):
        """
        Initializes the WebElement instance.

        Args:
            node (dict): The node description from the browser.
            connection_handler (ConnectionHandler): The connection handler instance.
        """
        self._node = node
        self._search_method = method
        self._connection_handler = connection_handler
        self._attributes = {}
        self._def_attributes()

    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self._attributes.items())
        return f'{self.__class__.__name__}({attrs})'

    def _def_attributes(self):
        attr = self._node['attributes']
        for i in range(0, len(attr), 2):
            key = attr[i]
            key = key if key != 'class' else 'class_name'
            value = attr[i + 1]
            self._attributes[key] = value

    @property
    def class_name(self) -> str:
        """
        Retrieves the class name of the
        element.

        Returns:
            str: The class name of the
            element.

        """
        return self._attributes.get('class')

    @property
    def id(self) -> str:
        """
        Retrieves the id of the element.

        Returns:
            str: The id of the element.
        """
        return self._attributes.get('id')

    @property
    def tag_name(self) -> str:
        """
        Retrieves the tag name of the element.

        Returns:
            str: The tag name of the element.
        """
        return self._node.get('nodeName')

    @property
    def text(self) -> str:
        """
        Retrieves the text of the element.

        Returns:
            str: The text of the element.
        """
        return self._node.get('nodeValue')

    @property
    async def bounds(self) -> list:
        """
        Asynchronously retrieves the bounding box of the element.

        Returns:
            dict: The bounding box of the element.
        """
        if self._search_method == By.XPATH:
            response = await self._connection_handler.execute_command(
                DomCommands.box_model_by_object_id(self._node['objectId'])
            )
        else:
            response = await self._connection_handler.execute_command(
                DomCommands.box_model(self._node['nodeId'])
            )
        return response['result']['model']['content']

    def get_attribute(self, name: str) -> str:
        """
        Retrieves the attribute value of the element.

        Args:
            name (str): The name of the attribute.

        Returns:
            str: The value of the attribute.
        """
        return self._attributes.get(name)

    async def click(self, x_offset: int = 0, y_offset: int = 0):
        element_bounds = await self.bounds
        position_to_click = self._calculate_center(element_bounds)
        position_to_click = (
            position_to_click[0] + x_offset,
            position_to_click[1] + y_offset,
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
        await self._connection_handler.execute_command(
            InputCommands.insert_text(text)
        )

    @staticmethod
    def _calculate_center(bounds: list) -> tuple:
        x_values = [bounds[i] for i in range(0, len(bounds), 2)]
        y_values = [bounds[i] for i in range(1, len(bounds), 2)]
        x_center = sum(x_values) / len(x_values)
        y_center = sum(y_values) / len(y_values)
        return x_center, y_center
