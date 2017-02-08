import os

import pytest

from rt.path import Path


# TODO: do something with this garbage!!!?


@pytest.mark.parametrize(
    "path_parts",
    [
        ("a", "b", "c", "d"),
        ("whatever", "man"),
        ("",),
        (Path("a"), Path("b"), "c")

    ]
)
def test_path_initialize(path_parts):
    path_got = Path(*path_parts)
    path_exp = os.path.join(
        *(os.path.normpath(str(path_part)) for path_part in path_parts)
    )
    assert str(path_got) == str(path_exp)
    assert repr(path_got) == repr(path_exp)


@pytest.mark.parametrize(
    "initial_path, append_path",
    [
        ("a", "b"),
        ("whatever", "man"),
        (Path("a"), "b"),
        (Path("a"), Path("b")),
        ("a", Path("b")),
        ("a", "")
    ]
)
def test_path_append(initial_path, append_path):
    path_got = Path(initial_path)
    path_got.append(append_path)
    path_exp = os.path.join(
        os.path.normpath(str(initial_path)),
        os.path.normpath(str(append_path))
    )
    assert str(path_got) == str(path_exp)
    assert repr(path_got) == repr(path_exp)


@pytest.mark.parametrize(
    "initial_path, extend_path",
    [
        ("a", ("b",)),
        ("whatever", ("garbage", "man",)),
        (Path("a"), ("b", "c", "e")),
        (Path("a"), (Path("b"), "e",)),
        ("a", (Path("b"), Path("b"),)),
        ("a", ("",))
    ]
)
def test_path_append(initial_path, extend_path):
    path_got = Path(initial_path)
    path_got.extend(extend_path)
    path_exp = os.path.join(
        os.path.normpath(str(initial_path)),
        *(os.path.normpath(str(part)) for part in extend_path)
    )
    assert str(path_got) == str(path_exp)
    assert repr(path_got) == repr(path_exp)
