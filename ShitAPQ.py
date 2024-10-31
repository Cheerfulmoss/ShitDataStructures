from ShitPQ import ShitPQ, PQEntry, InsertType


class ShitAPQ(ShitPQ):
    def _locator(self, priority: int) -> PQEntry | None:
        for entry in self._data:
            if entry.get_priority() == priority:
                return entry
        return None

    def update_priority(self, priority: int, new_priority: int) -> None:
        entry = self._locator(priority)
        if entry is None:
            raise ValueError(
                f"Priority not present in {self.__class__.__name__}. "
                f"{priority=}")
        entry.set_priority(new_priority)


if __name__ == "__main__":
    from random import shuffle
    sapq = ShitAPQ()
    ins = ["A", "B", "C", "D", "E"]
    shuffle(ins)
    for thing in ins:
        sapq.fifo_insert(thing)
        print(sapq)
        print(sapq.peek_priority(), sapq.peek_value())

    sapq.update_priority(2, 10)
    print(sapq)

