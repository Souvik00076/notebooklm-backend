from typing import TypedDict, Callable


class SplitterConfig(TypedDict, total=False):
    chunk_size: int
    chunk_overlap: int
    separator: str
    keep_separator: bool
    length_function: Callable[[str], int]
