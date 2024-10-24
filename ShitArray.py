from typing import Any


class ShitArray:
    def __init__(self, length: int) -> None:
        self._data = [None] * length
        self._length = length

    def __repr__(self) -> str:
        return f"ShitArray(length={self._length})"

    def __contains__(self, item: Any) -> bool:
        for stored in self:
            if item == stored:
                return True
        return False

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ShitArray):
            if len(self) != len(other):
                return False
            for i in range(self._length):
                if self[i] != other[i]:
                    return False
            return True
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, ShitArray):
            if len(self) != len(other):
                return False
            for i in range(self._length):
                if self[i] < other[i]:
                    return False
            return True
        return False

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, ShitArray):
            if len(self) != len(other):
                return False
            for i in range(self._length):
                if self[i] > other[i]:
                    return False
            return True
        return False

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __ge__(self, other: Any) -> bool:
        return self == other or self > other

    def __le__(self, other: Any) -> bool:
        return self == other or self < other

    def __iter__(self) -> Any:
        for pointer in range(self._length):
            yield self._data[pointer]

    def __str__(self) -> str:
        return str(self._data)

    def __len__(self) -> int:
        return self._length

    def __setitem__(self, index: int, value: Any) -> None:
        if type(index) is not int:
            raise ValueError("Index must be an integer")
        if index < 0 or index >= self._length:
            raise IndexError(f"Index out of range, {index=}, {len(self)=}")

        self._data[index] = value

    def __getitem__(self, index: int) -> Any:
        if type(index) is not int:
            raise ValueError("Index must be an integer")
        if index < 0 or index >= self._length:
            raise IndexError(f"Index out of range, {index=}, {len(self)=}")

        return self._data[index]


if __name__ == "__main__":
    ass = ShitArray(10)
    bum = ShitArray(10)
    ass[9] = "ass"
    bum[8] = "ass"
    print(ass == bum, ass, bum)
