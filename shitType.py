from typing import Any


class ShitType:
    def __init__(self, value):
        self._set = False
        self._type = type(value)
        self._value = value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return repr(self._value)

    def get(self) -> Any:
        return self._value

    def set(self, value: Any) -> None:
        self.__setattr__("_value", value)

    def __setattr__(self, key: str, value: Any) -> None:
        if not hasattr(self, "_set") or (not self._set and key == "_set"):
            return super().__setattr__(key, value)

        if (hasattr(self, "_type") and key == "_value"
                and isinstance(value, self._type)):
            return super().__setattr__(key, value)
        elif not hasattr(self, "_type"):
            self._set = True
            return super().__setattr__(key, value)

        if key == "_value":
            raise ValueError(f"Value must be of type {self._type.__name__}")
        raise AttributeError(f"Cannot modify {key}")


if __name__ == "__main__":
    y = ShitType("Hello!")