import typing as t

from fastapi import Depends


def _hello() -> str:
    print('hello', 1)
    return 'hello'


def hello_dep(hello: t.Annotated[str, Depends(_hello)]):
    print(hello, 2)
