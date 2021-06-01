# SPDX-License-Identifier: MIT

from __future__ import annotations

import io
import typing


if typing.TYPE_CHECKING:
    from typing import Any, ClassVar, Iterator, List, Optional, Tuple, Type


T = typing.TypeVar('T', bound=io.IOBase)


class IOMux(typing.Generic[T]):
    _io_cls: ClassVar[Type[T]]

    class Proxy():
        def __init__(self, owner: IOMux, name: str) -> None:
            self._owner = owner
            self._name = name

        @property
        def _io(self) -> T:
            if not self._owner._io or self._owner._io[-1][0] != self._name:
                self._owner._io.append((self._name, self._owner._io_cls()))
            return self._owner._io[-1][1]

        def __getattr__(self, name: str) -> Any:
            return getattr(self._io, name)

    def __init_subclass__(cls, io_cls: Type[T]) -> None:
        cls._io_cls = io_cls

    def __init__(self):
        assert self._io_cls
        self._io: List[Tuple[str, T]] = []

    def __getattr__(self, name: str) -> Proxy:
        return self.Proxy(self, name)

    @typing.overload
    def entries(self) -> Iterator[Tuple[str, T]]: ...

    @typing.overload
    def entries(self, name: str) -> Iterator[T]: ...

    def entries(self, name: Optional[str] = None):
        if name is None:
            yield from self._io
        for io_name, io_obj in self._io:
            if io_name == name:
                yield io_obj


class BytesMux(IOMux, io_cls=io.BytesIO):
    def getvalue(self, name: Optional[str] = None) -> bytes:
        if name:
            return b''.join(io_obj.getvalue() for io_obj in self.entries(name))
        return b''.join(
            io_obj.getvalue()
            for io_name, io_obj in self.entries()
        )

    def values(self) -> Iterator[Tuple[str, bytes]]:
        for io_name, io_obj in self._io:
            yield io_name, io_obj.getvalue()


class StringMux(IOMux, io_cls=io.StringIO):
    def getvalue(self, name: Optional[str] = None) -> str:
        if name:
            return ''.join(io_obj.getvalue() for io_obj in self.entries(name))
        return ''.join(
            io_obj.getvalue()
            for io_name, io_obj in self.entries()
        )

    def values(self) -> Iterator[Tuple[str, str]]:
        for io_name, io_obj in self._io:
            yield io_name, io_obj.getvalue()
