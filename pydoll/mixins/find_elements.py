import asyncio

from pydoll import exceptions
from pydoll.commands.dom import DomCommands
from pydoll.commands.runtime import RuntimeCommands
from pydoll.constants import By


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
            node_description = await self._get_node_description(by, value)
            if node_description or (
                asyncio.get_event_loop().time() - start_time > timeout
            ):
                break
            await asyncio.sleep(0.5)

        if not node_description:
            if raise_exc:
                raise TimeoutError('Element not found')
            return None

        return create_web_element(
            node_description, self._connection_handler, by, value
        )

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
        node_description = await self._get_node_description(by, value)

        if not node_description:
            if raise_exc:
                raise exceptions.ElementNotFound('Element not found')
            return None

        return create_web_element(
            node_description, self._connection_handler, by, value
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
        nodes_description = await self._get_nodes_description(by, value)

        if not nodes_description:
            if raise_exc:
                raise exceptions.ElementNotFound('Element not found')
            return []

        return [
            create_web_element(node, self._connection_handler, by, value)
            for node in nodes_description
        ]

    async def _get_nodes_description(self, by: str, value: str):
        """
        Executes a command to find elements on the page and returns their
        descriptions.

        Args:
            by (str): The type of selector to use.
            value (str): The value of the selector to use.

        Returns:
            list: The descriptions of the found nodes or an empty list if
            not found.
        """
        if hasattr(self, '_node'):
            root_node_id = self._node['nodeId']
            object_id = self._node['objectId']
        else:
            root_node_id = await self._get_root_node_id()
            object_id = ''

        response = await self._execute_command(
            DomCommands.find_elements(
                by, value, node_id=root_node_id, object_id=object_id
            )
        )

        if not response.get('result', {}):
            return []

        if by == By.XPATH:
            if (
                not response.get('result', {})
                .get('result', {})
                .get('objectId')
            ):
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

        nodes_description = await self._describe_nodes_based_on_response(
            response, by
        )
        return nodes_description

    async def _get_node_description(self, by: str, value: str):
        """
        Executes a command to find an element on the page and returns its
        description.

        Args:
            by (str): The type of selector to use.
            value (str): The value of the selector to use.

        Returns:
            dict: The description of the found node or None if not found.
        """
        if hasattr(self, '_node'):
            root_node_id = self._node['nodeId']
            object_id = self._node['objectId']
        else:
            root_node_id = await self._get_root_node_id()
            object_id = ''

        response = await self._execute_command(
            DomCommands.find_element(
                by, value, node_id=root_node_id, object_id=object_id
            )
        )

        if not response.get('result', {}):
            return None

        if by == By.XPATH:
            if (
                not response.get('result', {})
                .get('result', {})
                .get('objectId')
            ):
                return None

        node_description = await self._describe_node_based_on_response(
            response, by
        )
        return node_description

    async def _get_root_node_id(self):
        """
        Retrieves the root node ID of the current page's DOM.

        Returns:
            int: The unique ID of the root node in the current DOM.
        """
        response = await self._execute_command(DomCommands.dom_document())
        return response['result']['root']['nodeId']

    async def _describe_nodes_based_on_response(self, response: dict, by: str):
        """
        Describes nodes based on the response from finding the elements.

        Args:
            response (dict): The response containing the result of finding
            the nodes.
            by (str): The selector type used to find the nodes.

        Returns:
            list: A list of detailed descriptions of the nodes.
        """
        nodes_description = []
        if by == By.XPATH:
            for object_id in response:
                try:
                    node_description = await self._describe_node(
                        object_id=object_id
                    )
                except KeyError:
                    continue

                node_id = await self._get_node_id_by_object_id(object_id)
                node_description.update({
                    'nodeId': node_id,
                    'objectId': object_id,
                })
                nodes_description.append(node_description)
        else:
            for node_id in response['result']['nodeIds']:
                node_description = await self._describe_node(node_id=node_id)
                object_id = await self._get_object_id_by_node_id(node_id)
                node_description.update({
                    'nodeId': node_id,
                    'objectId': object_id,
                })
                nodes_description.append(node_description)
        return nodes_description

    async def _describe_node_based_on_response(self, response: dict, by: str):
        """
        Describes a node based on the response from finding the element.

        Args:
            response (dict): The response containing the result of finding
            the node.
            by (str): The selector type used to find the node.

        Returns:
            dict: A detailed description of the node.
        """
        if by == By.XPATH:
            object_id = response['result']['result']['objectId']
            node_description = await self._describe_node(object_id=object_id)
            node_id = await self._get_node_id_by_object_id(object_id)
            node_description.update({'nodeId': node_id, 'objectId': object_id})
        else:
            target_node_id = response['result']['nodeId']
            if target_node_id == 0:
                return None
            node_description = await self._describe_node(
                node_id=target_node_id
            )
            object_id = await self._get_object_id_by_node_id(target_node_id)
            node_description['objectId'] = object_id

        return node_description

    async def _describe_node(
        self, node_id: int = None, object_id: str = ''
    ) -> dict:
        """
        Provides a detailed description of a specific node within the DOM.

        Args:
            node_id (int): The unique ID of the node to describe.

        Returns:
            dict: A dictionary containing the detailed description of the node.
        """
        response = await self._execute_command(
            DomCommands.describe_node(node_id=node_id, object_id=object_id)
        )
        return response['result']['node']

    async def _get_object_id_by_node_id(self, node_id: int):
        """
        Retrieves the object ID of a node based on its node ID.

        Args:
            node_id (int): The unique ID of the node in the DOM.

        Returns:
            str: The object ID of the node.
        """
        response = await self._execute_command(
            DomCommands.resolve_node(node_id)
        )
        return response['result']['object']['objectId']

    async def _get_node_id_by_object_id(self, object_id: str):
        """
        Retrieves the node ID of a node based on its object ID.

        Args:
            object_id (str): The unique ID of the node in the DOM.

        Returns:
            int: The node ID of the node.
        """
        response = await self._execute_command(
            DomCommands.request_node(object_id)
        )
        return response['result']['nodeId']

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
