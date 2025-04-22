# global imports
from pydoll.commands.browser import BrowserCommands
from pydoll.commands.dom import DomCommands
from pydoll.commands.fetch import FetchCommands
from pydoll.commands.input import InputCommands
from pydoll.commands.network import NetworkCommands
from pydoll.commands.page import PageCommands
from pydoll.commands.runtime import RuntimeCommands
from pydoll.commands.storage import StorageCommands
from pydoll.commands.target import TargetCommands

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
