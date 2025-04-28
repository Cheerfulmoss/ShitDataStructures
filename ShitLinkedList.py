from typing import Any


class ShitLL:
    def __init__(self) -> None:
        self._indices: list[int] = []
        self._node: LLNode | None = None

    def __len__(self) -> int:
        return len(self._indices)

    def __getitem__(self, index: int | None) -> Any:
        if not self._node:
            raise ValueError("Empty ShitLL")

        self._node = self._node.move(index)
        return self._node.get_data()

    def __str__(self) -> str:
        result = []
        next = self._node.move(None)
        while next:
            self._node = next
            result.append(str(self._node))
            next = self._node.get_next()
        return "[" + ", ".join(result) + "]"

    def append(self, data: Any) -> None:
        if not self._node:
            self._node = LLNode(self._indices, 0, data)
            return

        self._node = self._node.append(data)

    def insert(self, index: int, data: Any) -> None:
        if not self._node:
            self._node = LLNode(self._indices, 0, data)
            return

        self._node = self._node.insert(index, data)


class LLNode:
    def __init__(self, indices: list[int], index: int, data: Any) -> None:
        self._index: int = index
        self._data: Any = data
        self._indices = indices
        self._next: LLNode | None = None
        self._prev: LLNode | None = None
        self._indices.insert(self._index, self._index)

    def __len__(self) -> int:
        return len(self._indices)

    def __str__(self) -> str:
        return f"i: {self._index} -> {self._data}"

    def set_prev(self, prev: "LLNode") -> None:
        self._prev = prev

    def set_next(self, next: "LLNode") -> None:
        self._next = next

    def get_prev(self) -> "LLNode":
        return self._prev

    def get_next(self) -> "LLNode":
        return self._next

    def append(self, data: Any) -> "LLNode":
        offset = len(self._indices) - self._index - 1
        self = self.move(offset)

        new_node = LLNode(self._indices, self._index + 1, data)
        self.set_next(new_node)
        self.get_next().set_prev(self)
        return self.get_next()

    def insert(self, index: int, data: Any) -> "LLNode":
        self = self.move(index)

        # Setup new node.
        new_node = LLNode(self._indices, self._index, data)
        new_node.set_prev(self.get_prev())
        new_node.set_next(self)

        self.get_prev().set_next(new_node)
        self.set_prev(new_node)

        next = self
        while next is not None:
            self = next
            self._index += 1
            self._indices[self._index] = self._index
            next = self.get_next()

        return new_node

    def move(self, index: int | None) -> "LLNode":
        if index is None:
            if not self._index:
                return self
            return self._prev.move(-(self._index - 1))

        abs_index = self._index + index
        if 0 > abs_index >= len(self._indices):
            raise IndexError("Index out of range")

        if index > 0:
            return self._next.move(index - 1)
        if index < 0:
            return self._prev.move(index + 1)
        return self

    def get_data(self) -> Any:
        return self._data


if __name__ == "__main__":
    shit_l = ShitLL()
    real_l = []

    # len
    print(len(real_l) == len(shit_l))

    # Append
    real_l.append(1)
    shit_l.append(1)
    print(len(real_l) == len(shit_l))

    # Check append
    print(shit_l[0] == real_l[0])

    # Append many
    for i in range(10):
        shit_l.append(i)
        real_l.append(i)

    print(len(shit_l) == len(real_l))
    print(shit_l[0] == real_l[10])
    print(shit_l[-2] == real_l[8])
    shit_l[None]
    print(shit_l._node._index == 0)
    print(shit_l)
    print(real_l)
    shit_l[None]

    # Insert
    shit_l.insert(1, 10)
    real_l.insert(1, 10)
    shit_l[None]
    print(shit_l[1] == real_l[1])

    print(shit_l, shit_l._indices)
