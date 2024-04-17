from typing import Any, Callable, NamedTuple


class LoxFunction(NamedTuple):
    arity: Callable[[], int]
    call: Callable[[Any, Any], Any]


class BreakException(Exception):
    pass


class RuntimeException(Exception):
    pass


class Visitable:
    def visit(self, vis):
        """Calls the "visit<ClassName> function on the `vis` argument"""
        funcName = f"visit{self.__class__.__name__}"
        func = getattr(vis, funcName, None)
        if func is None:
            raise Exception(
                f"Class {vis.__class__.__name__} is missing a function with name: {funcName}"
            )
        return func(self)
