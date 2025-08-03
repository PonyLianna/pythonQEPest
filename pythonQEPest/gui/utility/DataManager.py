from pythonQEPest.gui.utility.DataManagerMeta import DataManagerMeta


class DataManager(metaclass=DataManagerMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_data = []
        self._result_data = []

    # def __call__(self, *args, **kwargs) -> list:
    #     return self.file_data

    # def __bool__(self):
    #     return bool(self.file_data)

    @property
    def file_data(self):
        return self._file_data

    @property
    def result_data(self):
        return self._result_data

    def clear(self, lst):
        lst.clear()
        return self

    def add(self, lst, entry):
        if not entry in lst:
            lst.append(entry)
        return self

    def update(self, lst, index, new_entry):
        if 0 <= index < len(lst):
            lst[index] = new_entry
        return self

    def remove_by_id(self, lst, id: str | int):
        return [row for row in lst if row[0] != id]

    def remove_by_ids(self, lst, ids: list[str, int]):
        return [row for row in lst if row[0] not in ids]

    def clear_file(self):
        return self.clear(self.file_data)

    def add_file(self, entry):
        return self.add(self.file_data, entry)

    def update_file(self, index, new_entry):
        return self.update(self.file_data, index, new_entry)

    def remove_file_by_id(self, id: str | int):
        self._file_data = self.remove_by_id(self.file_data, id)
        return self

    def remove_file_by_ids(self, ids: list[str, int]):
        self._file_data = self.remove_by_ids(self.file_data, ids)
        return self

    def clear_result(self):
        return self.clear(self.result_data)

    def add_result(self, entry):
        return self.add(self.result_data, entry)

    def update_result(self, index, new_entry):
        return self.update(self.result_data, index, new_entry)

    def remove_result_by_id(self, id: str | int):
        self._result_data = self.remove_by_id(self.result_data, id)
        return self

    def remove_result_by_ids(self, ids: list[str, int]):
        self._result_data = self.remove_by_ids(self.result_data, ids)
        return self
