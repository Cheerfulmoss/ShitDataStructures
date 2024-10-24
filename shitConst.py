from typing import Any


class ShitConst:
    def __init__(self, value: Any) -> None:
        self._value = value
        self.__hidden = value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return repr(self._value)

    def __setitem__(self, key, value) -> None:
        raise ValueError("Modification not allowed")

    def __setattr__(self, key, value) -> None:
        if hasattr(self, key):
            raise AttributeError("Modification not allowed")
        super().__setattr__(key, value)

    def __delattr__(self, item) -> None:
        raise AttributeError("Deletion not allowed")

    def get(self) -> Any:
        if self._value != self.__hidden:
            self._value = self.__hidden

        return self._value


if __name__ == "__main__":
    x = ShitConst(10)
    print(x.get())