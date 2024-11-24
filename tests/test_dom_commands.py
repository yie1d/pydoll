# tests/test_dom_commands.py

from pydoll.commands.dom import (
    DomCommands,
)
from pydoll.commands.runtime import RuntimeCommands
from pydoll.constants import By


def test_enable_dom_events():
    expected = {'method': 'DOM.enable'}
    result = DomCommands.enable_dom_events()
    assert result == expected, (
        'O método enable_dom_events não retornou o dicionário esperado.'
    )


def test_dom_document():
    expected = {'method': 'DOM.getDocument'}
    result = DomCommands.dom_document()
    assert result == expected, (
        'O método dom_document não retornou o dicionário esperado.'
    )


def test_scroll_into_view():
    object_id = '12345'
    expected = {
        'method': 'DOM.scrollIntoViewIfNeeded',
        'params': {'objectId': object_id},
    }
    result = DomCommands.scroll_into_view(object_id)
    assert result == expected, (
        'O método scroll_into_view não retornou o dicionário esperado.'
    )


def test_get_outer_html():
    object_id = 67890
    expected = {
        'method': 'DOM.getOuterHTML',
        'params': {'objectId': object_id},
    }
    result = DomCommands.get_outer_html(object_id)
    assert result == expected, (
        'O método get_outer_html não retornou o dicionário esperado.'
    )


def test_request_node():
    object_id = 'abcde'
    expected = {'method': 'DOM.requestNode', 'params': {'objectId': object_id}}
    result = DomCommands.request_node(object_id)
    assert result == expected, (
        'O método request_node não retornou o dicionário esperado.'
    )


def test_describe_node():
    object_id = 'fghij'
    expected = {
        'method': 'DOM.describeNode',
        'params': {'objectId': object_id},
    }
    result = DomCommands.describe_node(object_id)
    assert result == expected, (
        'O método describe_node não retornou o dicionário esperado.'
    )


def test_box_model():
    object_id = 'klmno'
    expected = {'method': 'DOM.getBoxModel', 'params': {'objectId': object_id}}
    result = DomCommands.box_model(object_id)
    assert result == expected, (
        'O método box_model não retornou o dicionário esperado.'
    )


def test_get_current_url(mock_runtime_commands):
    expected_command = RuntimeCommands.evaluate_script('window.location.href')
    mock_runtime_commands.evaluate_script.return_value = expected_command
    result = DomCommands.get_current_url()
    mock_runtime_commands.evaluate_script.assert_called_once_with(
        'window.location.href'
    )
    assert result == expected_command, (
        'O método get_current_url não retornou o comando esperado.'
    )


def test_find_element_css(mock_runtime_commands):
    by = By.CSS
    value = 'test-class'
    expected_selector = 'test-class'
    expected_expression = f'document.querySelector("{expected_selector}");'
    expected_command = {
        'method': 'Runtime.evaluate',
        'params': {
            'expression': expected_expression,
        },
    }
    mock_runtime_commands.evaluate_script.return_value = expected_command
    result = DomCommands.find_element(by, value)
    mock_runtime_commands.evaluate_script.assert_called_once_with(
        expected_expression
    )
    assert result == expected_command, (
        'O método find_element com CSS não retornou o comando esperado.'
    )


def test_find_element_xpath(mock_runtime_commands):
    by = By.XPATH
    value = "//div[@id='test']"
    expected_expression = (
        '\n        var element = document.evaluate(\n'
        '            "//div[@id=\'test\']", document, null,\n'
        '            XPathResult.FIRST_ORDERED_NODE_TYPE, null\n'
        '        ).singleNodeValue;\n'
        '        element;\n    '
    )
    expected_command = {
        'method': 'Runtime.evaluate',
        'params': {
            'expression': expected_expression,
        },
    }
    mock_runtime_commands.evaluate_script.return_value = expected_command
    result = DomCommands.find_element(by, value)
    mock_runtime_commands.evaluate_script.assert_called_once_with(
        expected_expression
    )
    assert result == expected_command, (
        'O método find_element com XPATH não retornou o comando esperado.'
    )


def test_find_element_id(mock_runtime_commands):
    by = By.ID
    value = 'test-id'
    expected_selector = '#test-id'
    expected_expression = f'document.querySelector("{expected_selector}");'
    expected_command = {
        'method': 'Runtime.evaluate',
        'params': {
            'expression': expected_expression,
            'returnByValue': False,
        },
    }
    mock_runtime_commands.evaluate_script.return_value = expected_command
    result = DomCommands.find_element(by, value)
    mock_runtime_commands.evaluate_script.assert_called_once_with(
        expected_expression
    )
    assert result == expected_command, (
        'O método find_element com ID não retornou o comando esperado.'
    )


def test_find_element_class_name(mock_runtime_commands):
    by = By.CLASS_NAME
    value = 'test-class'
    expected_selector = '.test-class'
    expected_expression = f'document.querySelector("{expected_selector}");'
    expected_command = {
        'method': 'Runtime.evaluate',
        'params': {
            'expression': expected_expression,
            'returnByValue': False,
        },
    }
    mock_runtime_commands.evaluate_script.return_value = expected_command
    result = DomCommands.find_element(by, value)
    mock_runtime_commands.evaluate_script.assert_called_once_with(
        expected_expression
    )
    assert result == expected_command, (
        'O método find_element com CLASS_NAME não retornou o comando esperado.'
    )


def test_find_element_relative_css(mock_runtime_commands):
    by = By.CSS
    value = 'div[id="test"]'
    object_id = '12345'
    expected_expression = (
        '\n        function() {\n'
        '            return this.querySelector("div[id=\\"test\\"]");\n'
        '        }\n    '
    )
    expected_command = {
        'method': 'Runtime.callFunctionOn',
        'params': {
            'functionDeclaration': expected_expression,
            'objectId': object_id,
            'returnByValue': False,
        },
    }
    mock_runtime_commands.call_function_on.return_value = expected_command
    result = DomCommands.find_element(by, value, object_id)
    mock_runtime_commands.call_function_on.assert_called_once_with(
        object_id, expected_expression, return_by_value=False
    )

    assert result == expected_command, (
        'O método find_element relativo não retornou o comando esperado.'
    )


def test_find_element_relative_class_name(mock_runtime_commands):
    by = By.CLASS_NAME
    value = 'test-class'
    object_id = '12345'
    expected_selector = '.test-class'
    expected_expression = (
        f'\n        function() {{\n'
        f'            return this.querySelector("'
        f'{expected_selector}");\n'
        f'        }}\n    '
    )
    expected_command = {
        'method': 'Runtime.callFunctionOn',
        'params': {
            'functionDeclaration': expected_expression,
            'objectId': object_id,
            'returnByValue': False,
        },
    }
    mock_runtime_commands.call_function_on.return_value = expected_command
    result = DomCommands.find_element(by, value, object_id)
    mock_runtime_commands.call_function_on.assert_called_once_with(
        object_id, expected_expression, return_by_value=False
    )
    assert result == expected_command, (
        'O método find_element relativo não retornou o comando esperado.'
    )


def test_find_element_relative_id(mock_runtime_commands):
    by = By.ID
    value = 'test-id'
    object_id = '12345'
    expected_selector = '#test-id'
    expected_command = {
        'method': 'Runtime.callFunctionOn',
        'params': {
            'functionDeclaration': (
                f'function() {{ return this.querySelector("'
                f'{expected_selector}"); }}'
            ),
            'objectId': object_id,
            'returnByValue': False,
        },
    }
    mock_runtime_commands.call_function_on.return_value = expected_command
    result = DomCommands.find_element(by, value, object_id)
    mock_runtime_commands.call_function_on.assert_called_once_with(
        object_id,
        (
            f'\n        function() {{\n'
            f'            return this.querySelector("'
            f'{expected_selector}");\n'
            f'        }}\n    '
        ),
        return_by_value=False,
    )
    assert result == expected_command, (
        'O método find_element relativo não retornou o comando esperado.'
    )


def test_find_element_relative_xpath(mock_runtime_commands):
    by = By.XPATH
    value = '//div[@id="test"]'
    object_id = '12345'
    expected_command = {
        'method': 'Runtime.callFunctionOn',
        'params': {
            'functionDeclaration': (
                '\n        function() {\n'
                '            return document.evaluate(\n'
                '                ".//div[@id=\\"test\\"]", this, null,\n'
                '                XPathResult.FIRST_ORDERED_NODE_TYPE, null\n'
                '            ).singleNodeValue;\n'
                '        }\n    '
            ),
            'objectId': object_id,
            'returnByValue': False,
        },
    }
    mock_runtime_commands.call_function_on.return_value = expected_command
    result = DomCommands.find_element(by, value, object_id)
    mock_runtime_commands.call_function_on.assert_called_once_with(
        object_id,
        (
            '\n        function() {\n'
            '            return document.evaluate(\n'
            '                ".//div[@id=\\"test\\"]", this, null,\n'
            '                XPathResult.FIRST_ORDERED_NODE_TYPE, null\n'
            '            ).singleNodeValue;\n'
            '        }\n    '
        ),
        return_by_value=False,
    )
    assert result == expected_command, (
        'O método find_elements relativo não retornou o comando esperado.'
    )


def test_find_elements_class_name(mock_runtime_commands):
    by = By.CLASS_NAME
    value = 'test-class'
    expected_selector = '.test-class'
    expected_expression = f'document.querySelectorAll("{expected_selector}");'
    expected_command = {
        'method': 'Runtime.evaluate',
        'params': {
            'expression': expected_expression,
        },
    }

    mock_runtime_commands.evaluate_script.return_value = expected_command
    result = DomCommands.find_elements(by, value)
    mock_runtime_commands.evaluate_script.assert_called_once_with(
        expected_expression
    )
    assert result == expected_command, (
        'O método find_elements com CLASS_NAME não '
        'retornou o comando esperado.'
    )


def test_find_elements_xpath(mock_runtime_commands):
    by = By.XPATH
    value = "//div[@class='test']"
    expected_expression = (
        '\n        var elements = document.evaluate(\n'
        '            "//div[@class=\'test\']", document, null,\n'
        '            XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null\n'
        '        );\n        var results = [];\n'
        '        for (var i = 0; i < elements.snapshotLength; i++) {\n'
        '            results.push(elements.snapshotItem(i));\n'
        '        }\n        results;\n    '
    )
    expected_command = {
        'method': 'Runtime.evaluate',
        'params': {
            'expression': expected_expression,
        },
    }
    mock_runtime_commands.evaluate_script.return_value = expected_command
    result = DomCommands.find_elements(by, value)
    mock_runtime_commands.evaluate_script.assert_called_once_with(
        expected_expression
    )
    assert result == expected_command, (
        'O método find_elements com XPATH não retornou o comando esperado.'
    )


def test_find_elements_id(mock_runtime_commands):
    by = By.ID
    value = 'test-id'
    expected_selector = '#test-id'
    expected_command = {
        'method': 'Runtime.evaluate',
        'params': {
            'expression': f'document.querySelectorAll("{expected_selector}")'
        },
    }
    mock_runtime_commands.evaluate_script.return_value = expected_command
    result = DomCommands.find_elements(by, value)
    mock_runtime_commands.evaluate_script.assert_called_once_with(
        'document.querySelectorAll("#test-id");'
    )
    assert result == expected_command, (
        'O método find_elements com ID não retornou o comando esperado.'
    )


def test_find_elements_css(mock_runtime_commands):
    by = By.CSS
    value = 'test-class'
    expected_selector = 'test-class'
    expected_expression = f'document.querySelectorAll("{expected_selector}");'
    expected_command = {
        'method': 'Runtime.evaluate',
        'params': {
            'expression': expected_expression,
        },
    }
    mock_runtime_commands.evaluate_script.return_value = expected_command
    result = DomCommands.find_elements(by, value)
    mock_runtime_commands.evaluate_script.assert_called_once_with(
        expected_expression
    )
    assert result == expected_command, (
        'O método find_elements com CSS não retornou o comando esperado.'
    )


def test_find_elements_relative_xpath(mock_runtime_commands):
    by = By.XPATH
    value = '//div[@id="test"]'
    object_id = '12345'
    expected_expression = (
        '\n        function() {\n'
        '            var elements = document.evaluate(\n'
        '                ".//div[@id=\\"test\\"]", this, null,\n'
        '                XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null\n'
        '            );\n'
        '            var results = [];\n'
        '            for (var i = 0; i < elements.snapshotLength; i++) {\n'
        '                results.push(elements.snapshotItem(i));\n'
        '            }\n'
        '            return results;\n'
        '        }\n    '
    )
    expected_command = {
        'method': 'Runtime.callFunctionOn',
        'params': {
            'functionDeclaration': expected_expression,
            'objectId': object_id,
            'returnByValue': False,
        },
    }
    mock_runtime_commands.call_function_on.return_value = expected_command
    result = DomCommands.find_elements(by, value, object_id)
    mock_runtime_commands.call_function_on.assert_called_once_with(
        object_id, expected_expression, return_by_value=False
    )
    assert result == expected_command, (
        'O método find_elements relativo não retornou o comando esperado.'
    )


def test_find_elements_relative_css(mock_runtime_commands):
    by = By.CSS
    value = 'div[id="test"]'
    object_id = '12345'
    expected_expression = (
        '\n        function() {\n'
        '            return this.querySelectorAll("div[id=\\"test\\"]");\n'
        '        }\n    '
    )
    expected_command = {
        'method': 'Runtime.callFunctionOn',
        'params': {
            'functionDeclaration': expected_expression,
            'objectId': object_id,
            'returnByValue': False,
        },
    }
    mock_runtime_commands.call_function_on.return_value = expected_command
    result = DomCommands.find_elements(by, value, object_id)
    mock_runtime_commands.call_function_on.assert_called_once_with(
        object_id, expected_expression, return_by_value=False
    )
    assert result == expected_command, (
        'O método find_elements relativo não retornou o comando esperado.'
    )
