from math import ceil


class ShitHeap:
    def __init__(self, min_heap: bool, lst: list[any] = None):
        self._data = []
        self._size = 0
        self._capacity = 0
        self._min_heap = min_heap

        if lst is not None:
            self._size = len(lst)
            self._capacity = self._size
            self._data = [*lst]
            self.heapify()

    def __add__(self, other: any) -> "ShitHeap":
        if type(other) is not ShitHeap:
            raise ValueError(f"Cannot add {type(other)} with {type(self)}")
        new_data = self.get_data() + other.get_data()
        return ShitHeap(self.get_type() or other.get_type(), new_data)

    def __mul__(self, other: any) -> "ShitHeap":
        if type(other) is not int:
            raise ValueError(f"Cannot add {type(other)} with {type(self)}")
        new_data = self.get_data() * other
        return ShitHeap(self.get_type(), new_data)

    def __iadd__(self, other) -> "ShitHeap":
        if type(other) is not ShitHeap:
            raise ValueError(f"Cannot add {type(other)} with {type(self)}")
        self.extend(other)
        return self

    def __invert__(self) -> "ShitHeap":
        return ShitHeap(not self.get_type(), self.get_data())

    def __str__(self) -> str:
        tmp_heap = ShitHeap(self._min_heap, self._data)
        ret_str = "\\\\"
        length = tmp_heap.get_size()
        for i in range(length):
            ret_str += str(tmp_heap.pop())
            if i < length - 1:
                ret_str += ", "
        return ret_str + "//"

    def __len__(self) -> int:
        return self._size

    def __resize__(self) -> None:
        if self._size < self._capacity:
            return

        new_capacity = ceil((self._capacity + 1) * 1.5)
        new_data = [None] * new_capacity

        for i in range(self._size):
            new_data[i] = self._data[i]

        self._data = new_data
        self._capacity = new_capacity

    def push(self, element: any) -> None:
        self.__resize__()
        self._data[self._size] = element
        self._up_heap(self._size)
        self._size += 1

    def pop(self) -> any:
        value = self._data[0]

        self._size -= 1
        self._data[0] = self._data[self._size]
        self._data[self._size] = None
        self._down_heap(0)
        return value

    def extend(self, other, other_len: int = None) -> any:
        type_other = type(other)
        if type_other not in [list, ShitHeap]:
            raise ValueError(f"Cannot extend {type(self)} with {type(other)}")
        if type_other is ShitHeap:
            new_data = self.get_data() + other.get_data()
            self._size = self.get_size() + other.get_size()
            self._capacity = self.get_capacity() + other.get_capacity()
        else:
            new_data = self.get_data() + [*other]
            self._size += (other_len or 0)
            self._capacity += (other_len or 0)

        self._data = new_data
        self.heapify()

    def heapify(self) -> None:
        start_index = self._size // 2 - 1
        for i in range(start_index, -1, -1):
            self._down_heap(i)

    def clear(self) -> None:
        self._data = []
        self._size = 0
        self._capacity = 0

    def invert(self) -> None:
        self._min_heap = not self._min_heap
        self.heapify()

    def get_sorted(self, reverse: bool = False) -> list[any]:
        ret_data = [None] * self.get_size()

        extract_cpy = ShitHeap(reverse ^ self.get_type(), self.get_data())
        for i in range(extract_cpy.get_size()):
            ret_data[i] = extract_cpy.pop()

        return ret_data

    def get_size(self) -> int:
        return self._size

    def get_capacity(self) -> int:
        return self._capacity

    def get_data(self) -> list[any]:
        return [*self._data]

    def get_type(self) -> bool:
        return self._min_heap

    def _up_heap(self, index: int) -> None:
        parent = (index - 1) // 2
        while parent >= 0:
            if self.compare(self._data[index], self._data[parent]):
                self._swap(index, parent, self._data)

                index = parent
                parent = (index - 1) // 2
                continue
            return

    def _in_heap(self, index: int) -> bool:
        return index < self._size

    def _down_heap(self, index: int) -> None:
        while True:
            children = [2 * index + 1, 2 * index + 2]
            left_child = self._in_heap(children[0])
            right_child = self._in_heap(children[1])

            if not left_child and not right_child:
                return
            if not left_child:
                min_child = children[1]
            elif not right_child:
                min_child = children[0]
            else:
                min_child = (
                    children[0] if self.compare(self._data[children[0]],
                                                self._data[children[1]])
                    else children[1])

            if self.compare(self._data[min_child], self._data[index]):
                self._swap(min_child, index, self._data)

                index = min_child
            else:
                return

    @staticmethod
    def _swap(i: int, j: int, arr: list[any]) -> None:
        tmp = arr[i]
        arr[i] = arr[j]
        arr[j] = tmp

    def compare(self, x: any, y: any) -> bool:
        if self._min_heap:
            return x < y
        return x > y


if __name__ == "__main__":
    lst = list(reversed(list(range(7))))
    x = ShitHeap(min_heap=True, lst=lst)
    print(x.get_data())
