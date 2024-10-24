from ShitArray import ShitArray
from typing import Any, Iterable


class ShitDynamicArray:
    def __init__(self, lst: Iterable[Any] = None) -> None:
        self._data = ShitArray(0)
        self._size = 0

        if lst is None:
            return
        for elem in lst:
            self.append(elem)

    def __iter__(self) -> Any:
        for i in range(len(self)):
            yield self._data[i]

    def __bool__(self) -> bool:
        return len(self) != 0

    def __str__(self) -> str:
        ret_str = "["
        for i, elem in enumerate(self):
            ret_str += repr(elem)
            if i != len(self) - 1:
                ret_str += ", "
        return ret_str + "]"

    def __len__(self) -> int:
        return self._size

    def __resize__(self) -> None:
        if len(self._data) == 0:
            self._data = ShitArray(1)
            return

        if len(self._data) != len(self):
            return

        new_capacity = int(len(self._data) * 1.5) + 2
        new_data = ShitArray(new_capacity)
        for i, item in enumerate(self._data):
            new_data[i] = item

        self._data = new_data

    def __setitem__(self, index: int, value: Any) -> None:
        if index < 0 or index >= len(self):
            raise IndexError(f"Index out of range, {index=}, {len(self)=}")

        self._data[index] = value

    def __getitem__(self, index: int) -> Any:
        if index < 0 or index >= len(self):
            raise IndexError(f"Index out of range, {index=}, {len(self)=}")

        return self._data[index]

    def append(self, value: Any) -> None:
        self.__resize__()
        self._size += 1
        self[self._size - 1] = value

    def pop(self, index: int = None) -> Any:
        if index is None:
            index = len(self) - 1

        if index < 0 or index >= len(self):
            raise IndexError(f"Index out of range, {index=}, {len(self)=}")

        value = self[index]
        self[index] = None
        i = index
        for i in range(index + 1, len(self)):
            self[i - 1] = self[i]
        else:
            self[i] = None
        self._size -= 1
        return value

    def is_empty(self) -> bool:
        return len(self) == 0

if __name__ == "__main__":
    da = ShitDynamicArray()
    da.append(1)
    da.append(2)
    da.append(3)
    print(da)
    print(da.pop(0))
    print(da)
    print(da._data)