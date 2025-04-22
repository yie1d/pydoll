import copy


class RuntimeCommands:
    """
    A class for interacting with the JavaScript runtime using Chrome
    DevTools Protocol.

    This class provides methods to create commands for evaluating JavaScript
    expressions, calling functions on JavaScript objects, and retrieving
    object properties through CDP.

    Attributes:
        EVALUATE_TEMPLATE (dict): Template for the Runtime.evaluate command.
        CALL_FUNCTION_ON_TEMPLATE (dict): Template for the
            Runtime.callFunctionOn command.
        GET_PROPERTIES (dict): Template for the Runtime.getProperties command.
    """

    EVALUATE_TEMPLATE = {'method': 'Runtime.evaluate', 'params': {}}
    CALL_FUNCTION_ON_TEMPLATE = {
        'method': 'Runtime.callFunctionOn',
        'params': {},
    }
    GET_PROPERTIES = {
        'method': 'Runtime.getProperties',
        'params': {},
    }

    @classmethod
    def get_properties(cls, object_id: str) -> dict:
        """
        Generates a command to get the properties of a specific
        JavaScript object.

        Args:
            object_id (str): The object ID of the JavaScript object.

        Returns:
            dict: The CDP command to retrieve the object's properties.
        """
        command = copy.deepcopy(cls.GET_PROPERTIES)
        command['params']['objectId'] = object_id
        command['params']['ownProperties'] = True
        return command

    @classmethod
    def call_function_on(
        cls,
        object_id: str,
        function_declaration: str,
        return_by_value: bool = False,
    ) -> dict:
        """
        Generates a command to call a function on a specific
        JavaScript object.

        Args:
            object_id (str): The object ID of the JavaScript object to call
                the function on.
            function_declaration (str): The JavaScript function to execute
                on the object.
            return_by_value (bool, optional): Whether to return the result by
                value instead of as a remote object reference. Defaults to
                False.

        Returns:
            dict: The CDP command to call the function on the specified object.
        """
        command = copy.deepcopy(cls.CALL_FUNCTION_ON_TEMPLATE)
        command['params']['objectId'] = object_id
        command['params']['functionDeclaration'] = function_declaration
        command['params']['returnByValue'] = return_by_value
        return command

    @classmethod
    def evaluate_script(cls, expression: str) -> dict:
        """
        Generates a command to evaluate JavaScript code in the browser context.

        Args:
            expression (str): The JavaScript expression to evaluate.

        Returns:
            dict: The CDP command to evaluate the JavaScript expression.
        """
        command = copy.deepcopy(cls.EVALUATE_TEMPLATE)
        command['params'] = {
            'expression': expression,
            'returnByValue': False,
        }
        return command
