from typing import Literal

from pydoll.constants import By


class DomCommands:
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

        Returns:
            dict: The command to be sent to the browser.
        """
        return cls.ENABLE

    @classmethod
    def find_element(cls, dom_id: int, by: SelectorType, value: str) -> dict:
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
                command['params'] = {
                    'expression': xpath_script,
                    'returnByValue': False,
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
