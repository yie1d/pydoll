import asyncio
from typing import TypeVar

from pydoll import exceptions
from pydoll.commands import (
    DomCommands,
    RuntimeCommands,
)
from pydoll.constants import By, Scripts
from pydoll.protocol.base import Command

T = TypeVar('T')


def create_web_element(*args, **kwargs):
    """
    Creates a WebElement instance while avoiding circular imports.
    
    This function serves as a factory method to instantiate WebElement objects
    by dynamically importing the WebElement class at runtime. This approach
    prevents circular import dependencies between modules.
    
    Args:
        *args: Positional arguments to pass to the WebElement constructor.
        **kwargs: Keyword arguments to pass to the WebElement constructor.
    
    Returns:
        WebElement: A new instance of the WebElement class.
    """
    from pydoll.elements.web_element import WebElement  # noqa: PLC0415

    return WebElement(*args, **kwargs)


class FindElementsMixin:
    """
    A mixin class that provides element finding and waiting capabilities.
    
    This mixin implements comprehensive DOM element location functionality using
    various selector strategies (CSS, XPath, etc.) and provides methods for
    finding single elements, multiple elements, and waiting for elements to
    appear in the DOM.
    
    Classes that incorporate this mixin gain powerful element discovery capabilities
    without having to implement the complex logic of element location themselves.
    The mixin handles the communication with the browser through CDP commands and
    transforms the browser's responses into WebElement instances.
    
    Primary functionality includes:
    1. Finding individual elements by various selectors
    2. Finding collections of elements matching a selector
    3. Waiting for elements to appear with configurable timeouts
    4. Support for relative searches within a parent element's context
    """

    async def wait_element(
        self,
        by: By,
        value: str,
        timeout: int = 10,
        raise_exc: bool = True,
    ):
        """
        Waits for an element to be present in the DOM within a specified timeout.
        
        Repeatedly attempts to find the element using the provided selector,
        with a short delay between attempts, until either:
        - The element is found (returns the element)
        - The timeout is exceeded (raises an exception or returns None)
        
        This method is essential for handling dynamic content that may not be
        immediately available after a page load or user interaction.
        
        Args:
            by: The selector strategy to use (CSS_SELECTOR, XPATH, ID, etc.).
                Constants are available in the By enum.
            value: The selector value to locate the element (e.g., "div.content").
            timeout: Maximum time in seconds to wait for the element to appear.
                Default is 10 seconds.
            raise_exc: Whether to raise a TimeoutError if the element is not found
                within the timeout period. If False, returns None instead.
                Default is True.
        
        Returns:
            WebElement or None: The found element as a WebElement instance,
                or None if the element is not found and raise_exc is False.
        
        Raises:
            TimeoutError: If the element is not found within the timeout
                period and raise_exc is True.
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

    async def find_element(self, by: By, value: str, raise_exc: bool = True):
        """
        Finds the first element matching the specified selector.
        
        Locates a single element in the DOM using the provided selector strategy
        and value. The search is performed either in the context of the entire
        document or relative to the current element (when used from a WebElement).
        
        Args:
            by: The selector strategy to use (CSS_SELECTOR, XPATH, ID, etc.).
                Constants are available in the By enum.
            value: The selector value to locate the element (e.g., "div.content").
            raise_exc: Whether to raise an ElementNotFound exception if the
                element is not found. If False, returns None instead.
                Default is True.
        
        Returns:
            WebElement or None: A WebElement instance representing the found element,
                or None if the element is not found and raise_exc is False.
        
        Raises:
            ElementNotFound: If the element is not found and raise_exc is True.
        """
        if hasattr(self, '_object_id'):
            command = self._get_find_element_command(by, value, self._object_id)
        else:
            command = self._get_find_element_command(by, value)

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

        return create_web_element(object_id, self._connection_handler, by, value, attributes)  # type: ignore

    async def find_elements(self, by: By, value: str, raise_exc: bool = True):
        """
        Finds all elements matching the specified selector.
        
        Locates multiple elements in the DOM using the provided selector strategy
        and value. The search is performed either in the context of the entire
        document or relative to the current element (when used from a WebElement).
        
        Args:
            by: The selector strategy to use (CSS_SELECTOR, XPATH, ID, etc.).
                Constants are available in the By enum.
            value: The selector value to locate the elements (e.g., "div.item").
            raise_exc: Whether to raise an ElementNotFound exception if no
                elements are found. If False, returns an empty list instead.
                Default is True.
        
        Returns:
            list[WebElement]: A list of WebElement instances representing all
                found elements. Returns an empty list if no elements are found
                and raise_exc is False.
        
        Raises:
            ElementNotFound: If no elements are found and raise_exc is True.
        """
        if hasattr(self, '_object_id'):
            command = self._get_find_elements_command(by, value, self._object_id)
        else:
            command = self._get_find_elements_command(by, value)

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
                node_description = await self._describe_node(object_id=object_id)
            except KeyError:
                continue

            attributes = node_description.get('attributes', [])
            tag_name = node_description.get('nodeName', '').lower()
            attributes.extend(['tag_name', tag_name])

            elements.append(
                create_web_element(object_id, self._connection_handler, by, value, attributes)  # type: ignore
            )
        return elements

    async def _describe_node(self, object_id: str = '') -> dict:
        """
        Retrieves detailed information about a DOM node.
        
        Uses the CDP DOM.describeNode command to get comprehensive information
        about a node, including its attributes, properties, and DOM structure.
        This method is used internally to gather the data needed to properly
        initialize WebElement instances.
        
        Args:
            object_id: The CDP object ID of the node to describe.
                If empty, describes the document node. Default is an empty string.
        
        Returns:
            dict: A dictionary containing the node's complete description,
                including attributes, node type, tag name, and other properties.
        """
        response = await self._execute_command(DomCommands.describe_node(object_id=object_id))
        return response['result']['node']

    async def _execute_command(self, command: Command[T]) -> T:
        """
        Executes a Chrome DevTools Protocol command.
        
        Sends a command to the browser via the connection handler and returns
        the response. This is an internal method used by other methods in this
        class to communicate with the browser.
        
        Args:
            command: The CDP command to execute, properly structured according
                to the protocol specification.
        
        Returns:
            T: The response from the browser after executing the command,
                with the type specified by the command's type parameter.
        """
        return await self._connection_handler.execute_command(command, timeout=60)  # type: ignore

    def _get_find_element_command(self, by: By, value: str, object_id: str = '') -> Command:
        """
        Creates the appropriate CDP command for finding a single element.
        
        Constructs a command object based on the selector type and context
        (global document or relative to another element). Handles special cases
        for different selector types like CLASS_NAME, ID, and XPATH.
        
        Args:
            by: The selector strategy to use (CSS_SELECTOR, XPATH, ID, etc.).
            value: The selector value to locate the element.
            object_id: The CDP object ID of the context element for relative searches.
                If empty, the search is performed in the global document context.
                Default is an empty string.
        
        Returns:
            Command: A properly structured CDP command object ready to be executed.
        """
        escaped_value = value.replace('"', '\\"')
        match by:
            case By.CLASS_NAME:
                selector = f'.{escaped_value}'
            case By.ID:
                selector = f'#{escaped_value}'
            case _:
                selector = escaped_value
        if object_id and not by == By.XPATH:
            script = Scripts.RELATIVE_QUERY_SELECTOR.replace('{selector}', selector)
            command = RuntimeCommands.call_function_on(
                object_id,
                script,
                return_by_value=False,
            )
        elif by == By.XPATH:
            command = self._get_find_element_by_xpath_command(value, object_id)
        else:
            command = RuntimeCommands.evaluate(
                expression=Scripts.QUERY_SELECTOR.replace('{selector}', selector)
            )
        return command

    def _get_find_elements_command(self, by: By, value: str, object_id: str = '') -> Command:
        """
        Creates the appropriate CDP command for finding multiple elements.
        
        Constructs a command object based on the selector type and context
        (global document or relative to another element). Handles special cases
        for different selector types like CLASS_NAME, ID, and XPATH.
        
        Args:
            by: The selector strategy to use (CSS_SELECTOR, XPATH, ID, etc.).
            value: The selector value to locate the elements.
            object_id: The CDP object ID of the context element for relative searches.
                If empty, the search is performed in the global document context.
                Default is an empty string.
        
        Returns:
            Command: A properly structured CDP command object ready to be executed.
        """
        escaped_value = value.replace('"', '\\"')
        match by:
            case By.CLASS_NAME:
                selector = f'.{escaped_value}'
            case By.ID:
                selector = f'#{escaped_value}'
            case _:
                selector = escaped_value
        if object_id and not by == By.XPATH:
            script = Scripts.RELATIVE_QUERY_SELECTOR_ALL.replace('{selector}', escaped_value)
            command = RuntimeCommands.call_function_on(
                object_id,
                script,
                return_by_value=False,
            )
        elif by == By.XPATH:
            command = self._get_find_elements_by_xpath_command(value, object_id)
        else:
            command = RuntimeCommands.evaluate(
                expression=Scripts.QUERY_SELECTOR_ALL.replace('{selector}', selector)
            )
        return command

    def _get_find_element_by_xpath_command(self, xpath: str, object_id: str) -> Command:
        """
        Creates a CDP command specifically for finding an element by XPath.
        
        XPath selectors require special handling compared to CSS selectors.
        This method constructs the appropriate command based on whether the
        search is global or relative to another element.
        
        Args:
            xpath: The XPath expression to locate the element.
            object_id: The CDP object ID of the context element for relative searches.
                If empty, the search is performed in the global document context.
        
        Returns:
            Command: A properly structured CDP command object for XPath element finding.
        """
        escaped_value = xpath.replace('"', '\\"')
        if object_id:
            escaped_value = self._ensure_relative_xpath(escaped_value)
            script = Scripts.FIND_RELATIVE_XPATH_ELEMENT.replace('{escaped_value}', escaped_value)
            command = RuntimeCommands.call_function_on(
                object_id,
                script,
                return_by_value=False,
            )
        else:
            script = Scripts.FIND_XPATH_ELEMENT.replace('{escaped_value}', escaped_value)
            command = RuntimeCommands.evaluate(expression=script)
        return command

    def _get_find_elements_by_xpath_command(self, xpath: str, object_id: str) -> Command:
        """
        Creates a CDP command specifically for finding multiple elements by XPath.
        
        XPath selectors require special handling compared to CSS selectors.
        This method constructs the appropriate command based on whether the
        search is global or relative to another element.
        
        Args:
            xpath: The XPath expression to locate the elements.
            object_id: The CDP object ID of the context element for relative searches.
                If empty, the search is performed in the global document context.
        
        Returns:
            Command: A properly structured CDP command object for XPath multiple element finding.
        """
        escaped_value = xpath.replace('"', '\\"')
        if object_id:
            escaped_value = self._ensure_relative_xpath(escaped_value)
            script = Scripts.FIND_RELATIVE_XPATH_ELEMENTS.replace('{escaped_value}', escaped_value)
            command = RuntimeCommands.call_function_on(
                object_id,
                script,
                return_by_value=False,
            )
        else:
            script = Scripts.FIND_XPATH_ELEMENTS.replace('{escaped_value}', escaped_value)
            command = RuntimeCommands.evaluate(expression=script)
        return command

    def _ensure_relative_xpath(self, xpath: str) -> str:
        """
        Ensures an XPath expression is properly formatted for relative searches.
        
        Prepends a dot (.) to the XPath expression if it doesn't already start
        with one, making it a relative XPath that searches from the context node
        rather than from the document root.
        
        Args:
            xpath: The original XPath expression.
        
        Returns:
            str: The XPath expression modified to be relative if needed.
        """
        return f'.{xpath}' if not xpath.startswith('.') else xpath
