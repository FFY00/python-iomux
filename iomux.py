# SPDX-License-Identifier: MIT

from __future__ import annotations

import io
import typing


if typing.TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Iterator, List, Optional, Tuple, Type, Union


_T = typing.TypeVar('_T', bound=io.IOBase)
# same as _T but we need it becuase we use it in a different class
_V = typing.TypeVar('_V', bound=io.IOBase)


class IOMux(typing.Generic[_T]):
    class Proxy(typing.Generic[_V]):
        def __init__(self, owner: IOMux[_V], name: str) -> None:
            self._owner = owner
            self._name = name

        @property
        def _io(self) -> _V:
            if not self._owner._io or self._owner._io[-1][0] != self._name:
                self._owner._io.append((self._name, self._owner._io_cls()))
            return self._owner._io[-1][1]

        def __getattr__(self, name: str) -> Any:
            return getattr(self._io, name)

    def __init__(self) -> None:
        self._io_cls: Type[_T] = self.__orig_bases__[0].__args__[0]
        self._io: List[Tuple[str, _T]] = []

    def __getattr__(self, name: str) -> Any:
        return self.Proxy(self, name)

    @typing.overload
    def entries(self) -> Iterator[Tuple[str, _T]]: ...

    @typing.overload
    def entries(self, name: str) -> Iterator[_T]: ...

    def entries(self, name: Optional[str] = None) -> Union[Iterator[Tuple[str, _T]], Iterator[_T]]:
        if name is None:
            yield from self._io
        for io_name, io_obj in self._io:
            if io_name == name:
                yield io_obj


class BytesMux(IOMux[io.BytesIO]):
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


class StringMux(IOMux[io.StringIO]):
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
