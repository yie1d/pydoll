import asyncio

from pydoll import exceptions
from pydoll.commands.dom import DomCommands
from pydoll.commands.runtime import RuntimeCommands


def create_web_element(*args, **kwargs):
    """
    Creates a WebElement instance to avoid circular imports.
    """
    from pydoll.element import WebElement  # noqa: PLC0415

    return WebElement(*args, **kwargs)


class FindElementsMixin:
    async def wait_element(
        self,
        by: DomCommands.SelectorType,
        value: str,
        timeout: int = 10,
        raise_exc: bool = True,
    ):
        """
        Waits for an element to be present in the DOM.

        Args:
            by (SelectorType): The type of selector to use.
            value (str): The value of the selector.
            timeout (int, optional): Time in seconds to wait for the element.
            Defaults to 10.

        Returns:
            Element: The element found in the DOM.

        Raises:
            TimeoutError: If the element is not found within the timeout.
        """
        start_time = asyncio.get_event_loop().time()
        while True:
            try:
                element = await self.find_element(by, value, raise_exc=False)
                if element:
                    return element
            except exceptions.ElementNotFound:
                pass

            if asyncio.get_event_loop().time() - start_time > timeout:
                if raise_exc:
                    raise TimeoutError('Element not found')
                return None

            await asyncio.sleep(0.5)

    async def find_element(
        self, by: DomCommands.SelectorType, value: str, raise_exc: bool = True
    ):
        """
        Finds an element on the current page using the specified selector.

        Args:
            by (SelectorType): The type of selector to use.
            value (str): The value of the selector to use.

        Returns:
            dict: The response from the browser.

        Raises:
            ElementNotFound: If the element is not found and raise_exc is True.
        """
        if hasattr(self, '_object_id'):
            command = DomCommands.find_element(by, value, self._object_id)
        else:
            command = DomCommands.find_element(by, value)

        response = await self._execute_command(command)

        if not response.get('result', {}).get('result', {}).get('objectId'):
            if raise_exc:
                raise exceptions.ElementNotFound('Element not found')
            return None

        object_id = response['result']['result']['objectId']
        node_description = await self._describe_node(object_id=object_id)
        attributes = node_description.get('attributes', [])

        tag_name = node_description.get('nodeName', '').lower()
        attributes.extend(['tag_name', tag_name])

        return create_web_element(
            object_id, self._connection_handler, by, value, attributes
        )

    async def find_elements(
        self, by: DomCommands.SelectorType, value: str, raise_exc: bool = True
    ):
        """
        Finds all elements on the current page using the specified selector.

        Args:
            by (SelectorType): The type of selector to use.
            value (str): The value of the selector to use.

        Returns:
            list: A list of elements found on the page.

        Raises:
            ElementNotFound: If no elements are found and raise_exc is True.
        """
        if hasattr(self, '_object_id'):
            command = DomCommands.find_elements(by, value, self._object_id)
        else:
            command = DomCommands.find_elements(by, value)

        response = await self._execute_command(command)

        if not response.get('result', {}).get('result', {}).get('objectId'):
            if raise_exc:
                raise exceptions.ElementNotFound('Element not found')
            return []

        object_id = response['result']['result']['objectId']
        query_response = await self._execute_command(
            RuntimeCommands.get_properties(object_id=object_id)
        )
        response = []
        for query in query_response['result']['result']:
            query_value = query.get('value', {})
            if query_value and query_value['type'] == 'object':
                response.append(query_value['objectId'])

        elements = []
        for object_id in response:
            try:
                node_description = await self._describe_node(
                    object_id=object_id
                )
            except KeyError:
                continue

            attributes = node_description.get('attributes', [])
            tag_name = node_description.get('nodeName', '').lower()
            attributes.extend(['tag_name', tag_name])

            elements.append(
                create_web_element(
                    object_id, self._connection_handler, by, value, attributes
                )
            )
        return elements

    async def _describe_node(self, object_id: str = '') -> dict:
        """
        Provides a detailed description of a specific node within the DOM.

        Args:
            node_id (int): The unique ID of the node to describe.

        Returns:
            dict: A dictionary containing the detailed description of the node.
        """
        response = await self._execute_command(
            DomCommands.describe_node(object_id=object_id)
        )
        return response['result']['node']

    async def _execute_command(self, command: dict) -> dict:
        """
        Executes a command on the page.

        Args:
            command (dict): The command to execute.

        Returns:
            dict: The result of the command execution.
        """
        return await self._connection_handler.execute_command(
            command, timeout=60
        )
