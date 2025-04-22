# global imports
from pydoll.protocol.commands.browser_commands import BrowserCommands
from pydoll.protocol.commands.dom_commands import DomCommands
from pydoll.protocol.commands.fetch_commands import FetchCommands
from pydoll.protocol.commands.input_commands import InputCommands
from pydoll.protocol.commands.network_commands import NetworkCommands
from pydoll.protocol.commands.page_commands import PageCommands
from pydoll.protocol.commands.runtime_commands import RuntimeCommands
from pydoll.protocol.commands.storage_commands import StorageCommands
from pydoll.protocol.commands.target_commands import TargetCommands

__all__ = [
    'DomCommands',
    'FetchCommands',
    'InputCommands',
    'NetworkCommands',
    'PageCommands',
    'RuntimeCommands',
    'StorageCommands',
    'BrowserCommands',
    'TargetCommands',
]
