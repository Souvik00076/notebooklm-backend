from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
    MarkdownTextSplitter,
    HTMLHeaderTextSplitter,
    RecursiveCharacterTextSplitter as CodeSplitter,
    TextSplitter,
)

from app.rag.constants.enum import SplitterType
from app.rag.constants.types import SplitterConfig


class SplitterFactory:
    _splitters = {
        SplitterType.CHARACTER: CharacterTextSplitter,
        SplitterType.RECURSIVE_CHARACTER: RecursiveCharacterTextSplitter,
        SplitterType.TOKEN: TokenTextSplitter,
        SplitterType.MARKDOWN: MarkdownTextSplitter,
        SplitterType.HTML: HTMLHeaderTextSplitter,
        SplitterType.CODE: CodeSplitter,
    }

    @classmethod
    def get_splitter(cls, splitter_type: SplitterType, config: SplitterConfig = {}) -> TextSplitter:
        if splitter_type not in cls._splitters:
            raise ValueError(f"Unknown splitter type: {splitter_type}")

        return cls._splitters[splitter_type](**config)
