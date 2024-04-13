from typing import Optional, Dict, Any
from util import RuntimeException


class Undefined:
    pass


class Environment:
    data: Dict[str, Any]

    def __init__(self, parent=None):
        self.parent: Optional[Environment] = parent
        self.data = {}

    def define(self, name, value: Any = Undefined):
        if name in self.data:
            raise RuntimeException(f"Variable already defined: {name}")
        self.data[name] = value

    def assign(self, name, value):
        if name in self.data:
            self.data[name] = value
            return
        if self.parent:
            return self.parent.assign(name, value)

        raise RuntimeException(f"Assignment to undefined variable: {name}")

    def get(self, name):
        if name in self.data:
            value = self.data[name]
            if value == Undefined:
                raise RuntimeException(f"Variable initialized but not defined: {name}")
            return self.data[name]
        if self.parent:
            return self.parent.get(name)

        raise RuntimeException(f"Get to undefined variable: {name}")
