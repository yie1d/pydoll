import copy


class RuntimeCommands:
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
        """Generates the command to get the properties of a specific object."""
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
        """Generates the command to call a function on a specific object."""
        command = copy.deepcopy(cls.CALL_FUNCTION_ON_TEMPLATE)
        command['params']['objectId'] = object_id
        command['params']['functionDeclaration'] = function_declaration
        command['params']['returnByValue'] = return_by_value
        return command

    @classmethod
    def evaluate_script(cls, expression: str) -> dict:
        """Generates the command to evaluate JavaScript code."""
        command = copy.deepcopy(cls.EVALUATE_TEMPLATE)
        command['params'] = {
            'expression': expression,
            'returnByValue': False,
        }
        return command
