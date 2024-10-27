class Options:
    def __init__(self):
        self._arguments = []
        self._binary_location = ''

    @property
    def arguments(self) -> list:
        return self._arguments

    @property
    def binary_location(self) -> str:
        return self._binary_location

    @binary_location.setter
    def binary_location(self, location: str):
        self._binary_location = location

    def add_argument(self, argument: str):
        if argument not in self.arguments:
            self.arguments.append(argument)
        else:
            raise ValueError(f'Argument already exists: {argument}')
