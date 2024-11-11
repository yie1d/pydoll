import copy
from typing import Literal

from pydoll.commands.runtime import RuntimeCommands
from pydoll.constants import By


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

    SelectorType = Literal[By.CSS, By.XPATH, By.CLASS_NAME, By.ID, By.TAG_NAME]

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
    def scroll_into_view(
        cls, node_id: int = None, object_id: str = ''
    ) -> dict:
        """Generates the command to scroll a specific DOM node into view."""
        return cls._create_command(
            cls.SCROLL_INTO_VIEW_IF_NEEDED,
            node_id=node_id,
            object_id=object_id,
        )

    @classmethod
    def get_outer_html(cls, node_id: int) -> dict:
        """Generates the command to get the outer HTML"""
        return cls._create_command(cls.GET_OUTER_HTML, node_id=node_id)

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
        return cls._create_command(
            cls.REQUEST_NODE_TEMPLATE, object_id=object_id
        )

    @classmethod
    def describe_node(cls, node_id: int = None, object_id: str = '') -> dict:
        """Generates the command to describe a specific DOM node."""
        return cls._create_command(
            cls.DESCRIBE_NODE_TEMPLATE, node_id=node_id, object_id=object_id
        )

    @classmethod
    def box_model(cls, node_id: int = None, object_id: str = '') -> dict:
        """
        Generates the command to get the box model of a specific DOM node.
        """
        return cls._create_command(
            cls.BOX_MODEL_TEMPLATE, node_id=node_id, object_id=object_id
        )

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
        node_id: int = None,
        object_id: str = '',
    ) -> dict:
        """Generates a command to find a DOM element based on the specified
        criteria."""
        match by:
            case By.CSS:
                return cls._find_element_by_selector(value, node_id)
            case By.XPATH:
                return cls._find_element_by_xpath(value, object_id)
            case By.CLASS_NAME:
                return cls._find_element_by_selector(f'.{value}', node_id)
            case By.ID:
                return cls._find_element_by_selector(f'#{value}', node_id)
            case By.TAG_NAME:
                return cls._find_element_by_selector(value, node_id)
            case _:
                raise ValueError(
                    "Unsupported selector type. Use 'css', 'xpath', "
                    "'class_name', or 'id'."
                )

    @classmethod
    def find_elements(
        cls,
        by: SelectorType,
        value: str,
        node_id: int = None,
        object_id: str = '',
    ) -> dict:
        """Generates a command to find multiple DOM elements based on the
        specified criteria."""
        match by:
            case By.CSS:
                return cls._find_elements_by_selector(value, node_id)
            case By.XPATH:
                return cls._find_elements_by_xpath(value, object_id)
            case By.CLASS_NAME:
                return cls._find_elements_by_selector(f'.{value}', node_id)
            case By.ID:
                return cls._find_elements_by_selector(f'#{value}', node_id)
            case By.TAG_NAME:
                return cls._find_elements_by_selector(value, node_id)
            case _:
                raise ValueError(
                    "Unsupported selector type. Use 'css', 'xpath', "
                    "'class_name', or 'id'."
                )

    @classmethod
    def resolve_node(cls, node_id: int) -> dict:
        """Generates the command to resolve a specific DOM node."""
        return cls._create_command(cls.RESOLVE_NODE_TEMPLATE, node_id=node_id)

    @classmethod
    def _create_command(
        cls,
        template: dict,
        node_id: int = None,
        object_id: str = None,
        **params,
    ) -> dict:
        """Creates a command from a template with optional parameters."""
        command = copy.deepcopy(template)
        command['params'].update({
            k: v for k, v in params.items() if v is not None
        })
        if node_id is not None:
            command['params']['nodeId'] = node_id
        if object_id:
            command['params']['objectId'] = object_id
        return command

    @classmethod
    def _find_element_by_selector(
        cls, selector: str, node_id: int = None
    ) -> dict:
        """Creates a command to find a DOM element by CSS selector."""
        command = cls._create_command(
            cls.FIND_ELEMENT_TEMPLATE, node_id=node_id
        )
        command['params']['selector'] = selector
        return command

    @classmethod
    def _find_element_by_xpath(cls, xpath: str, object_id: str) -> dict:
        """Creates a command to find a DOM element by XPath."""
        escaped_value = xpath.replace('"', '\\"')
        if object_id:
            command = cls._create_command(
                RuntimeCommands.CALL_FUNCTION_ON_TEMPLATE, object_id=object_id
            )
            command['params']['functionDeclaration'] = (
                'function() {'
                'return document.evaluate('
                f'"{escaped_value}", document, null, '
                'XPathResult.FIRST_ORDERED_NODE_TYPE, null'
                ').singleNodeValue;'
                '}'
            )
        else:
            command = cls._create_command(RuntimeCommands.EVALUATE_TEMPLATE)
            command['params']['expression'] = (
                'var element = document.evaluate('
                f'"{escaped_value}", document, null, '
                'XPathResult.FIRST_ORDERED_NODE_TYPE, null'
                ').singleNodeValue;'
                'element;'
            )
        return command

    @classmethod
    def _find_elements_by_selector(
        cls, selector: str, node_id: int = None
    ) -> dict:
        """Creates a command to find multiple DOM elements by CSS selector."""
        command = cls._create_command(
            cls.FIND_ALL_ELEMENTS_TEMPLATE, node_id=node_id
        )
        command['params']['selector'] = selector
        return command

    @classmethod
    def _find_elements_by_xpath(cls, xpath: str, object_id: str) -> dict:
        """Creates a command to find multiple DOM elements by XPath."""
        escaped_value = xpath.replace('"', '\\"')
        if object_id:
            command = cls._create_command(
                RuntimeCommands.CALL_FUNCTION_ON_TEMPLATE, object_id=object_id
            )
            command['params']['functionDeclaration'] = (
                'function() {'
                'var elements = document.evaluate('
                f'"{escaped_value}", document, null, '
                'XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null'
                ');'
                'var results = [];'
                'for (var i = 0; i < elements.snapshotLength; i++) {'
                'results.push(elements.snapshotItem(i));'
                '}'
                'return results;'
                '}'
            )
        else:
            command = cls._create_command(RuntimeCommands.EVALUATE_TEMPLATE)
            command['params']['expression'] = (
                'var elements = document.evaluate('
                f'"{escaped_value}", document, null, '
                'XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null'
                ');'
                'var results = [];'
                'for (var i = 0; i < elements.snapshotLength; i++) {'
                'results.push(elements.snapshotItem(i));'
                '}'
                'results;'
            )
        return command
