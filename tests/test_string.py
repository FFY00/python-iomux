# SPDX-License-Identifier: MIT

import pytest

import iomux


@pytest.fixture()
def abc_io():
    io = iomux.StringMux()
    io.a.write('aaa')
    io.b.write('bbb')
    io.c.write('ccc')
    io.c.write('ccc')
    io.b.write('bbb')
    io.a.write('aaa')
    return io


def test_all_entries(abc_io):
    assert [
        (name, io.getvalue()) for name, io in abc_io.entries()
    ] == [
        ('a', 'aaa'),
        ('b', 'bbb'),
        ('c', 'cccccc'),
        ('b', 'bbb'),
        ('a', 'aaa'),
    ]


@pytest.mark.parametrize(
    ('name', 'expected'),
    [
        ('a', ['aaa', 'aaa']),
        ('b', ['bbb', 'bbb']),
        ('c', ['cccccc']),
    ]
)
def test_named_entries(abc_io, name, expected):
    assert [
        io.getvalue() for io in abc_io.entries(name)
    ] == expected


def test_getvalue_all(abc_io):
    assert abc_io.getvalue() == 'aaabbbccccccbbbaaa'


@pytest.mark.parametrize(
    ('name', 'expected'),
    [
        ('a', 'aaaaaa'),
        ('b', 'bbbbbb'),
        ('c', 'cccccc'),
    ]
)
def test_getvalue_name(abc_io, name, expected):
    assert abc_io.getvalue(name) == expected


def test_values(abc_io):
    assert list(abc_io.values()) == [
        ('a', 'aaa'),
        ('b', 'bbb'),
        ('c', 'cccccc'),
        ('b', 'bbb'),
        ('a', 'aaa'),
    ]
