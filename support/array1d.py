"""This is a 1-indexed strongly typed List-like object.

It aims to mimic EnergyPlus's Array1D / EPVector class
"""

import collections.abc
from typing import Union


class _IndexComponent:
    def __getitem__(self, key):
        if isinstance(key, int):
            if key == 0:
                raise IndexError("This is a 1-indexed Array1D, index 0 is refused.")
            if key > 0:
                return key - 1
            else:
                return key


class Array1D(collections.abc.MutableSequence):
    """This is a 1-indexed strongly typed List-like object."""

    def __enforce_type(self, val):
        if type(val) == self.__type:
            return val
        else:
            return self.__type(val)

    def __init__(self, T: type, init: list = None) -> None:
        self.__type = T
        self._index_comp = _IndexComponent()
        self._lst = []
        self.__allocated = False
        if init is not None:  # and isinstance(init, list)?
            for x in init:
                self._lst.append(self.__enforce_type(x))
            self._allocated = True

    def __call__(self, *index: Union[int, slice, tuple]):
        if len(index) == 1:
            return self.__getitem__(index[0])
        elif len(index) == 2:
            return self.__getitem__(slice(index[0], index[1]))

    def __iter__(self):
        return (x for x in self._lst)

    def __getitem__(self, key: Union[int, slice]) -> any:
        if isinstance(key, slice):
            # Get the start, stop, and step from the slice
            # First, increment stop. We want that to be inclusive instead of exclusive
            s = slice(key.start, key.stop + 1, key.step)
            # And we have to take len() + 1 as well
            return Array1D(
                T=self.__type, init=[self._lst[self._index_comp[ii]] for ii in range(*s.indices(len(self) + 1))]
            )

        return self._lst[self._index_comp[key]]

    def __setitem__(self, index: int, val: any) -> None:
        self._lst[self._index_comp[index]] = self.__enforce_type(val)

    def __delitem__(self, index: int) -> None:
        del self._lst[self._index_comp[index]]

    def __len__(self) -> int:
        return len(self._lst)

    def __eq__(self, other) -> bool:
        if isinstance(other, Array1D):
            return self._lst == other._lst
        return self._lst == other

    def append(self, val: any) -> None:
        self._lst.append(self.__enforce_type(val))

    def insert(self, index: int, val: any) -> None:
        self._lst.insert(self._index_comp[index], self.__enforce_type(val))

    def __repr__(self) -> str:
        return f"{self._lst}"

    def allocated(self):
        return self.__allocated and len(self._lst) > 0

    def clear(self):
        self.__allocated = False
        self._lst = []

    def deallocate(self):
        self.clear()

    def allocate(self, n):
        self.__allocated = True
        self._lst = [self.__type()] * n

    def dimension(self, n, val):
        self.__allocated = True
        self._lst = [self.__enforce_type(val)] * n

    def resize(self, n, val: any = None):
        self.__allocated = True
        if val is None:
            val = self.__type()

        if n > len(self._lst):
            self._lst += [self.__enforce_type(val)] * n
        else:
            self._lst = self._lst[:n]

    def assign(self, val: any):
        self._lst = [self.__enforce_type(val)] * len(self._lst)
