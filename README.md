# iomux

[![checks](https://github.com/FFY00/python-iomux/actions/workflows/checks.yml/badge.svg)](https://github.com/FFY00/python-iomux/actions/workflows/checks.yml)
[![tests](https://github.com/FFY00/python-iomux/actions/workflows/tests.yml/badge.svg)](https://github.com/FFY00/python-iomux/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/FFY00/python-iomux/branch/main/graph/badge.svg?token=b8Sp012QO7)](https://codecov.io/gh/FFY00/python-iomux)

IO buffer multiplexer.


```python
import sys

from contextlib import redirect_stdout, redirect_stderr

import iomux


capture = iomux.StringMux()

with redirect_stdout(capture.out), redirect_stderr(capture.err):
    print('aaa')
    print('bbb', file=sys.stderr)
    print('aaa')
    print('bbb', file=sys.stderr)

assert capture.getvalue() == 'aaa\nbbb\naaa\nbbb\n'
assert capture.getvalue('out') == 'aaa\naaa\n'
assert capture.getvalue('err') == 'bbb\nbbb\n'
assert list(capture.values()) == [
    ('out', 'aaa\n'),
    ('err', 'bbb\n'),
    ('out', 'aaa\n'),
    ('err', 'bbb\n'),
]
```
