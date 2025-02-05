import copy
from typing import Literal

from pydoll.commands.runtime import RuntimeCommands
from pydoll.constants import By, Scripts


class DomCommands:
    """
    A class to define commands for interacting with the Document
    Object Model (DOM) using the Chrome DevTools Protocol (CDP).
    The commands allow for various operations on DOM nodes,
    such as enabling the DOM domain, retrieving the
    DOM document, describing nodes, and querying elements.

    Attributes:
        SelectorType (Literal): A type definition for supported selector types.
    """

    SelectorType = Literal[
        By.CSS_SELECTOR, By.XPATH, By.CLASS_NAME, By.ID, By.TAG_NAME
    ]

    ENABLE = {'method': 'DOM.enable'}
    DOM_DOCUMENT = {'method': 'DOM.getDocument'}
    DESCRIBE_NODE_TEMPLATE = {'method': 'DOM.describeNode', 'params': {}}
    FIND_ELEMENT_TEMPLATE = {'method': 'DOM.querySelector', 'params': {}}
    FIND_ALL_ELEMENTS_TEMPLATE = {
        'method': 'DOM.querySelectorAll',
        'params': {},
    }
    BOX_MODEL_TEMPLATE = {'method': 'DOM.getBoxModel', 'params': {}}
    RESOLVE_NODE_TEMPLATE = {'method': 'DOM.resolveNode', 'params': {}}
    REQUEST_NODE_TEMPLATE = {'method': 'DOM.requestNode', 'params': {}}
    GET_OUTER_HTML = {
        'method': 'DOM.getOuterHTML',
        'params': {},
    }
    SCROLL_INTO_VIEW_IF_NEEDED = {
        'method': 'DOM.scrollIntoViewIfNeeded',
        'params': {},
    }

    @classmethod
    def scroll_into_view(cls, object_id: str) -> dict:
        """Generates the command to scroll a specific DOM node into view."""
        command = copy.deepcopy(cls.SCROLL_INTO_VIEW_IF_NEEDED)
        command['params']['objectId'] = object_id
        return command

    @classmethod
    def get_outer_html(cls, object_id: int) -> dict:
        """Generates the command to get the outer HTML"""
        command = copy.deepcopy(cls.GET_OUTER_HTML)
        command['params']['objectId'] = object_id
        return command

    @classmethod
    def dom_document(cls) -> dict:
        """
        Generates the command to get the root DOM node of the current page.
        """
        return cls.DOM_DOCUMENT

    @classmethod
    def request_node(cls, object_id: str) -> dict:
        """Generates the command to request a specific DOM node by its object
        ID."""
        command = copy.deepcopy(cls.REQUEST_NODE_TEMPLATE)
        command['params']['objectId'] = object_id
        return command

    @classmethod
    def describe_node(cls, object_id: str) -> dict:
        """Generates the command to describe a specific DOM node."""
        command = copy.deepcopy(cls.DESCRIBE_NODE_TEMPLATE)
        command['params']['objectId'] = object_id
        return command

    @classmethod
    def box_model(cls, object_id: str) -> dict:
        """
        Generates the command to get the box model of a specific DOM node.
        """
        command = copy.deepcopy(cls.BOX_MODEL_TEMPLATE)
        command['params']['objectId'] = object_id
        return command

    @classmethod
    def enable_dom_events(cls) -> dict:
        """Generates the command to enable the DOM domain."""
        return cls.ENABLE

    @classmethod
    def get_current_url(cls) -> dict:
        """Generates the command to get the current URL of the page."""
        return RuntimeCommands.evaluate_script('window.location.href')

    @classmethod
    def find_element(
        cls,
        by: SelectorType,
        value: str,
        object_id: str = '',
    ) -> dict:
        """Generates a command to find a DOM element based on the specified
        criteria."""
        escaped_value = value.replace('"', '\\"')
        match by:
            case By.CLASS_NAME:
                selector = f'.{escaped_value}'
            case By.ID:
                selector = f'#{escaped_value}'
            case _:
                selector = escaped_value
        if object_id and not by == By.XPATH:
            script = Scripts.RELATIVE_QUERY_SELECTOR.replace(
                '{selector}', selector
            )
            command = RuntimeCommands.call_function_on(
                object_id,
                script,
                return_by_value=False,
            )
        elif by == By.XPATH:
            command = cls._find_element_by_xpath(value, object_id)
        else:
            command = RuntimeCommands.evaluate_script(
                Scripts.QUERY_SELECTOR.replace('{selector}', selector)
            )
        return command

    @classmethod
    def find_elements(
        cls,
        by: SelectorType,
        value: str,
        object_id: str = '',
    ) -> dict:
        """Generates a command to find multiple DOM elements based on the
        specified criteria."""
        escaped_value = value.replace('"', '\\"')
        match by:
            case By.CLASS_NAME:
                selector = f'.{escaped_value}'
            case By.ID:
                selector = f'#{escaped_value}'
            case _:
                selector = escaped_value
        if object_id and not by == By.XPATH:
            script = Scripts.RELATIVE_QUERY_SELECTOR_ALL.replace(
                '{selector}', escaped_value
            )
            command = RuntimeCommands.call_function_on(
                object_id,
                script,
                return_by_value=False,
            )
        elif by == By.XPATH:
            command = cls._find_elements_by_xpath(value, object_id)
        else:
            command = RuntimeCommands.evaluate_script(
                Scripts.QUERY_SELECTOR_ALL.replace('{selector}', selector)
            )
        return command

    @classmethod
    def _find_element_by_xpath(cls, xpath: str, object_id: str) -> dict:
        """Creates a command to find a DOM element by XPath."""
        escaped_value = xpath.replace('"', '\\"')
        if object_id:
            escaped_value = cls._ensure_relative_xpath(escaped_value)
            script = Scripts.FIND_RELATIVE_XPATH_ELEMENT.replace(
                '{escaped_value}', escaped_value
            )
            command = RuntimeCommands.call_function_on(
                object_id,
                script,
                return_by_value=False,
            )
        else:
            script = Scripts.FIND_XPATH_ELEMENT.replace(
                '{escaped_value}', escaped_value
            )
            command = RuntimeCommands.evaluate_script(script)
        return command

    @classmethod
    def _find_elements_by_xpath(cls, xpath: str, object_id: str) -> dict:
        """Creates a command to find multiple DOM elements by XPath."""
        escaped_value = xpath.replace('"', '\\"')
        if object_id:
            escaped_value = cls._ensure_relative_xpath(escaped_value)
            script = Scripts.FIND_RELATIVE_XPATH_ELEMENTS.replace(
                '{escaped_value}', escaped_value
            )
            command = RuntimeCommands.call_function_on(
                object_id,
                script,
                return_by_value=False,
            )
        else:
            script = Scripts.FIND_XPATH_ELEMENTS.replace(
                '{escaped_value}', escaped_value
            )
            command = RuntimeCommands.evaluate_script(script)
        return command

    @staticmethod
    def _ensure_relative_xpath(xpath: str) -> str:
        """Ensures that the XPath expression is relative."""
        return f'.{xpath}' if not xpath.startswith('.') else xpath
