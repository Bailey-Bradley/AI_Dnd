from collections.abc import Sequence

class ReadOnlyList(Sequence):
    def __init__(self, raw_list: list = []):
        self._list = raw_list

    def __getitem__(self, index):
        return self._list[index]

    def __len__(self):
        return len(self._list)