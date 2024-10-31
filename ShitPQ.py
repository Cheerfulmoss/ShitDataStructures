from shitHeap import ShitHeap
from enum import Enum
from typing import Any


class InsertType(Enum):
    FIFO = 0
    LIFO = 1
    NONE = 2


class PQEntry:
    def __init__(self, priority: int, value: Any) -> None:
        self._priority = priority
        self.value = value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PQEntry):
            return False
        return self._priority == other._priority

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, PQEntry):
            return False
        return self._priority < other._priority

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, PQEntry):
            return False
        return not (self == other or self < other)

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, PQEntry):
            return False
        return self == other and self < other

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, PQEntry):
            return False
        return self == other and self > other

    def __str__(self) -> str:
        return f"({self._priority}: {self.value})"

    def get_priority(self) -> int:
        return self._priority

    def set_priority(self, priority: int) -> None:
        self._priority = priority


class ShitPQ:
    def __init__(self, lst: list[tuple[int, Any]] = None) -> None:

        if lst is None:
            form_list = lst
            self._priority = 0
        else:
            form_list = [PQEntry(priority, value) for priority, value in lst]
            self._priority = max(form_list).get_priority()

        self._data = ShitHeap(min_heap=True, lst=form_list)

        self._insert_type: None | InsertType = None

    def __str__(self) -> str:
        ret = "["
        for i, ent in enumerate(self._data):
            ret += str(ent)
            if i < self._data.get_size() - 1:
                ret += ", "
        return ret + "]"

    def __len__(self) -> int:
        return self._data.get_size()

    def __bool__(self) -> bool:
        return bool(self._data)

    def _check_insert(self, ins_type: InsertType) -> None:
        if self._insert_type is None:
            self._insert_type = ins_type
            return
        if self._insert_type != ins_type:
            raise ValueError("Cannot mix insertion methods.")

    def _insert(self, priority: int, value: Any) -> None:
        self._data.push(PQEntry(priority, value))

    def set_insertion(self, ins_type: InsertType) -> None:
        self._insert_type = ins_type
        if ((self._insert_type == InsertType.FIFO and not self._data.get_type())
                or (self._insert_type == InsertType.LIFO
                    and self._data.get_type())):
            self._data.invert()

    def insert(self, priority: int, value: Any) -> None:
        self._check_insert(InsertType.NONE)

        self._insert(priority, value)

    def fifo_insert(self, value: Any) -> None:
        self._check_insert(InsertType.FIFO)

        if not self._data.get_type():
            self._data.invert()

        self._priority += 1
        self._insert(self._priority, value)

    def lifo_insert(self, value: Any) -> None:
        self._check_insert(InsertType.LIFO)

        if self._data.get_type():
            self._data.invert()

        self._priority += 1
        self._insert(self._priority, value)

    def pop(self) -> Any:
        if self._data.get_size() == 0:
            return None

        entry = self._data.pop()
        if not self._data.get_type():
            self._priority = entry.get_priority()
        return entry.value

    def peek_value(self) -> Any | None:
        if self._data.get_size() == 0:
            return None
        return self._data.get_data()[0].value

    def peek_priority(self) -> int | None:
        if self._data.get_size() == 0:
            return None
        return self._data.get_data()[0].get_priority()


if __name__ == "__main__":
    from random import shuffle

    sapq = ShitPQ()
    ins = ["A", "B", "C", "D", "E"]
    shuffle(ins)
    sapq.set_insertion(InsertType.FIFO)
    for thing in ins:
        sapq.fifo_insert(thing)
        print(sapq)
        print(sapq.peek_priority(), sapq.peek_value())

    print(list(map(str, sapq._data.get_data())))
    print(sapq._priority)
