from typing import Any
from ShitArray import ShitArray
from ShitDynamicArray import ShitDynamicArray
import time


class ShitHashTable:
    def __init__(self, depth: int, seed: int = 8, size: int = 1000) -> None:
        self._window_size = 8
        self._window = 2 ** self._window_size - 1
        self._depth = depth
        self._elements = 0
        self._seed = 2 ** seed
        self._power = seed

        self._max = size
        self._size = size
        self._special_seed = (time.perf_counter_ns() ** 2) & (2 ** 32 - 1)

        self._data = ShitArray(self._max)
        self._accessed_buffer = ShitDynamicArray()

    def __str__(self) -> str:
        ret_str = ShitDynamicArray()
        stack = ShitDynamicArray([self])

        while stack:
            current = stack.pop()

            if not current._depth:
                elem_count = 0
                data = current.get_data()
                if not data:
                    continue

                for elem in data:
                    if isinstance(elem, ShitDynamicArray) and len(elem):
                        elem_count += 1
                        ret_str.append(", ".join(map(
                            lambda x: f"{repr(x[0])}: {repr(x[1])}", elem)))
                    if elem_count == len(current):
                        break
            else:
                elem_count = 0
                data = current.get_data()
                if not data:
                    continue

                for elem in data:
                    if isinstance(elem, ShitHashTable):
                        elem_count += 1
                        stack.append(elem)
                    if elem_count == len(current):
                        break
        return "{" + " | ".join(ret_str) + "}"

    def __len__(self) -> int:
        return self._elements

    def __contains__(self, key: Any) -> bool:
        return self.contains(key)

    def __getitem__(self, key: Any) -> Any:
        return self.get(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        self.put(key, value)

    def hash(self, element: Any) -> int:
        x = (hash(hash(f"{self._special_seed}") * hash(element) *
                  hash(id(self))) % self._max)
        return x

    def get_data(self):
        return self._data

    def put(self, key: Any, element: Any) -> None:
        self._accessed_buffer = ShitDynamicArray()
        shit_map = self

        while True:
            index = shit_map.hash(key)
            value = shit_map.get_data()[index]

            if value is None:
                self._accessed_buffer.append(shit_map)
                if not shit_map._depth:
                    shit_map.get_data()[index] = (
                        ShitDynamicArray([(key, element)]))
                    break
                shit_map.get_data()[index] = (
                    ShitHashTable(shit_map._depth - 1,
                                  seed=shit_map._power,
                                  size=shit_map._size)
                )
                shit_map = shit_map.get_data()[index]
            elif shit_map._depth:
                self._accessed_buffer.append(shit_map)
                shit_map = shit_map.get_data()[index]
            else:
                for item in shit_map.get_data()[index]:
                    if item[0] == key:
                        raise ValueError("Duplicate keys cannot exist.")
                shit_map.get_data()[index].append((key, element))
                self._accessed_buffer.append(shit_map)
                break

        for hmap in self._accessed_buffer:
            hmap._elements += 1
        self._accessed_buffer = ShitDynamicArray()

    def resolve_key(self, key: Any) -> list[tuple[Any, Any]] | None:
        self._accessed_buffer = ShitDynamicArray()
        shit_map = self
        result = None

        while True:
            self._accessed_buffer.append(shit_map)
            index = shit_map.hash(key)
            result = shit_map.get_data()[index]

            if result is None:
                self._accessed_buffer = ShitDynamicArray()
                return None
            elif type(result) is ShitDynamicArray:
                return result
            shit_map = result

    def get(self, key: Any) -> Any | None:
        res = self.resolve_key(key)
        if res is None:
            return res

        for item in res:
            if item[0] == key:
                return item[1]
        return None

    def contains(self, key: Any) -> bool:
        res = self.resolve_key(key)
        if res is None:
            return False

        for item in res:
            if item[0] == key:
                return True
        return False

    def remove(self, key: Any) -> Any | None:
        res = self.resolve_key(key)
        value = None
        if res is None:
            return res

        for i, item in enumerate(res):
            if item[0] == key:
                value = res.pop(i)[1]
                break

        if value is None:
            self._accessed_buffer = ShitDynamicArray()

        for hmap in self._accessed_buffer:
            hmap._elements -= 1

        self._accessed_buffer = ShitDynamicArray()
        return value

    def clear(self) -> None:
        self._data = ShitArray(self._max)
        self._elements = 0
        self._accessed_buffer = ShitDynamicArray()


def visualize_shit_hash_table(table: ShitHashTable):
    stack = []
    idx = 0
    stack.append((table, None))

    graph = Digraph("ShitHashTable")
    graph.attr(fontsize="25")
    graph.attr(rankdir="TB", size="15,15!")
    graph.attr(nodesep="1", ranksep="1")

    while stack:
        item, parent = stack.pop()
        idx += 1
        node_id = f"node{idx}"
        label = (f"Shit Hash Table:\n"
                 f"- Depth: {item._depth}\n"
                 f"- Size: {len(item)}\n"
                 f"- Special Seed: {item._special_seed}")

        graph.node(node_id, label=label, shape="box")

        if parent:
            graph.edge(parent, node_id)

        for i, sub in enumerate(item.get_data()):
            if isinstance(sub, ShitHashTable):
                stack.append( (sub, node_id) )
            elif isinstance(sub, ShitDynamicArray) and len(sub):
                parent_child_id = f"{node_id}_dynamic_array_{i}"
                label = (
                    f"Shit Dynamic Array {i}\n"
                    f"- Size: {len(sub)}"
                )
                graph.node(parent_child_id, label=label, shape="box")
                graph.edge(node_id, parent_child_id)

                for j, (k, v) in enumerate(sub):
                    child_id = f"{parent_child_id}_child{j}"
                    elem_str = f"{repr(k)}: {repr(v)}"
                    graph.node(child_id, label=elem_str, shape="ellipse")
                    graph.edge(parent_child_id, child_id)
    return graph


if __name__ == "__main__":
    from graphviz import Digraph
    ha = ShitHashTable(2, size=10)
    print(f"{ha._depth=}")
    print("Wait...")
    for i in range(500):
        ha.put(i, chr(i % 256))

    graph = visualize_shit_hash_table(ha)

    print("Wait bitch")
    print(ha)
    print(len(ha), len(list(filter(lambda x: x is not None, ha._data))))
    graph.render("Shit_hash_table", format="svg", cleanup=True)

