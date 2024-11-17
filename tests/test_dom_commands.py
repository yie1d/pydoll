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
    expected_command = {
        'method': 'Runtime.evaluate',
        'params': {
            'expression': f'document.querySelector("{expected_selector}")'
        },
    }
    mock_runtime_commands.evaluate_script.return_value = expected_command
    result = DomCommands.find_element(by, value)
    mock_runtime_commands.evaluate_script.assert_called_once_with(
        'document.querySelector("test-class");'
    )
    assert result == expected_command, (
        'O método find_element com CSS não retornou o comando esperado.'
    )


def test_find_element_xpath():
    by = By.XPATH
    value = "//div[@id='test']"
    expected_command = {
        'method': 'Runtime.evaluate',
        'params': {
            'expression': (
                '\n        var element = document.evaluate(\n'
                '            "//div[@id=\'test\']", document, null,\n'
                '            XPathResult.FIRST_ORDERED_NODE_TYPE, null\n'
                '        ).singleNodeValue;\n'
                '        element;\n    '
            )
        },
    }
    result = DomCommands.find_element(by, value)
    assert result == expected_command, (
        'O método find_element com XPATH não retornou o comando esperado.'
    )


def test_find_elements_class_name(mock_runtime_commands):
    by = By.CLASS_NAME
    value = 'test-class'
    expected_selector = '.test-class'
    expected_command = {
        'method': 'Runtime.evaluate',
        'params': {
            'expression': f'document.querySelectorAll("{expected_selector}")'
        },
    }

    mock_runtime_commands.evaluate_script.return_value = expected_command
    result = DomCommands.find_elements(by, value)
    mock_runtime_commands.evaluate_script.assert_called_once_with(
        'document.querySelectorAll(".test-class");'
    )
    assert result == expected_command, (
        'O método find_elements com CLASS_NAME não '
        'retornou o comando esperado.'
    )


def test_find_elements_xpath():
    by = By.XPATH
    value = "//div[@class='test']"
    expected_command = {
        'method': 'Runtime.evaluate',
        'params': {
            'expression': (
                '\n        var elements = document.evaluate(\n'
                '            "//div[@class=\'test\']", document, null,\n'
                '            XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null\n'
                '        );\n        var results = [];\n'
                '        for (var i = 0; i < elements.snapshotLength; i++) {\n'
                '            results.push(elements.snapshotItem(i));\n'
                '        }\n        results;\n    '
            )
        },
    }
    result = DomCommands.find_elements(by, value)
    assert result == expected_command, (
        'O método find_elements com XPATH não retornou o comando esperado.'
    )
