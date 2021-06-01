# SPDX-License-Identifier: MIT

import pytest

import iomux


@pytest.fixture()
def abc_io():
    io = iomux.BytesMux()
    io.a.write(b'aaa')
    io.b.write(b'bbb')
    io.c.write(b'ccc')
    io.c.write(b'ccc')
    io.b.write(b'bbb')
    io.a.write(b'aaa')
    return io


def test_all_entries(abc_io):
    assert [
        (name, io.getvalue()) for name, io in abc_io.entries()
    ] == [
        ('a', b'aaa'),
        ('b', b'bbb'),
        ('c', b'cccccc'),
        ('b', b'bbb'),
        ('a', b'aaa'),
    ]


@pytest.mark.parametrize(
    ('name', 'expected'),
    [
        ('a', [b'aaa', b'aaa']),
        ('b', [b'bbb', b'bbb']),
        ('c', [b'cccccc']),
    ]
)
def test_named_entries(abc_io, name, expected):
    assert [
        io.getvalue() for io in abc_io.entries(name)
    ] == expected


def test_getvalue_all(abc_io):
    assert abc_io.getvalue() == b'aaabbbccccccbbbaaa'


@pytest.mark.parametrize(
    ('name', 'expected'),
    [
        ('a', b'aaaaaa'),
        ('b', b'bbbbbb'),
        ('c', b'cccccc'),
    ]
)
def test_getvalue_name(abc_io, name, expected):
    assert abc_io.getvalue(name) == expected


def test_values(abc_io):
    assert list(abc_io.values()) == [
        ('a', b'aaa'),
        ('b', b'bbb'),
        ('c', b'cccccc'),
        ('b', b'bbb'),
        ('a', b'aaa'),
    ]
