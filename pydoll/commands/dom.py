from typing import Literal

from pydoll.constants import By
import json

class DomCommands:
    """
    A class to define commands for interacting with the Document Object Model (DOM)
    using the Chrome DevTools Protocol (CDP). The commands allow for various
    operations on DOM nodes, such as enabling the DOM domain, retrieving the
    DOM document, describing nodes, and querying elements.

    Attributes:
        SelectorType (Literal): A type definition for supported selector types.
    """

    SelectorType = Literal[By.CSS, By.XPATH, By.CLASS_NAME, By.ID, By.TAG_NAME]

    ENABLE = {'method': 'DOM.enable'}
    DOM_DOCUMENT = {'method': 'DOM.getDocument'}
    DESCRIBE_NODE_TEMPLATE = {'method': 'DOM.describeNode', 'params': {}}
    FIND_ELEMENT_TEMPLATE = {'method': 'DOM.querySelector', 'params': {}}
    FIND_ELEMENT_XPATH_TEMPLATE = {'method': 'Runtime.evaluate', 'params': {}}
    BOX_MODEL_TEMPLATE = {'method': 'DOM.getBoxModel', 'params': {}}

    @classmethod
    def dom_document(cls) -> dict:
        """
        Generates the command to get the root DOM node of the current page.

        This command utilizes the CDP to retrieve the DOM document
        of the page being inspected.

        Returns:
            dict: The command to be sent to the browser.
        """
        return cls.DOM_DOCUMENT

    @classmethod
    def describe_node(cls, node_id: int) -> dict:
        """
        Generates the command to describe a specific DOM node.

        Args:
            node_id (int): The ID of the node to describe.

        This command leverages the CDP to provide details about the
        specified DOM node.

        Returns:
            dict: The command to be sent to the browser.
        """
        command = cls.DESCRIBE_NODE_TEMPLATE.copy()
        command['params']['nodeId'] = node_id
        return command

    @classmethod
    def box_model(cls, node_id: int) -> dict:
        """
        Generates the command to get the box model of a specific DOM node.

        Args:
            node_id (int): The ID of the node to get the box model for.

        This command retrieves box model information using the CDP.

        Returns:
            dict: The command to be sent to the browser.
        """
        command = cls.BOX_MODEL_TEMPLATE.copy()
        command['params']['nodeId'] = node_id
        return command

    @classmethod
    def enable_dom_events(cls) -> dict:
        """
        Generates the command to enable the DOM domain.

        This command activates the DOM domain for interaction
        using the CDP.

        Returns:
            dict: The command to be sent to the browser.
        """
        return cls.ENABLE

    @classmethod
    def find_element(cls, dom_id: int, by: SelectorType, value: str) -> dict:
        """
        Generates a command to find a DOM element based on the specified criteria.

        Args:
            dom_id (int): The ID of the DOM node within which to search.
            by (SelectorType): The method to use for finding the element.
            value (str): The value to use in conjunction with the method.

        This command uses the CDP to locate elements in the DOM, allowing
        for querying with various selector types.

        Returns:
            dict: The command to be sent to the browser.
        """
        match by:
            case By.CSS:
                command = cls.FIND_ELEMENT_TEMPLATE.copy()
                command['params'] = {'selector': value}
                command['params']['nodeId'] = dom_id
            case By.XPATH:
                command = cls.FIND_ELEMENT_XPATH_TEMPLATE.copy()
                xpath_script = f"""
                    (function() {{
                        const result = document.evaluate("{value}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                        return result.singleNodeValue;
                    }})()
                """
                xpath_script = json.dumps(xpath_script)
                command['params'] = {
                    'expression': xpath_script,
                    'returnByValue': True,
                }
            case By.CLASS_NAME:
                command = cls.FIND_ELEMENT_TEMPLATE.copy()
                command['params'] = {'selector': f'.{value}'}
                command['params']['nodeId'] = dom_id
            case By.ID:
                command = cls.FIND_ELEMENT_TEMPLATE.copy()
                command['params'] = {'selector': f'#{value}'}
                command['params']['nodeId'] = dom_id
            case By.TAG_NAME:
                command = cls.FIND_ELEMENT_TEMPLATE.copy()
                command['params'] = {'selector': value}
                command['params']['nodeId'] = dom_id
            case _:
                raise ValueError(
                    "Unsupported selector type. Use 'css', 'xpath', 'class_name', or 'id'."
                )

        return command
