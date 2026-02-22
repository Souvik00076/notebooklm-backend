from enum import Enum


class DocumentType(Enum):
    PDF = "pdf"
    DOC = "doc"
    DOCX = "docx"
    TXT = "txt"


class SplitterType(Enum):
    CHARACTER = "character"
    RECURSIVE_CHARACTER = "recursive_character"
    TOKEN = "token"
    MARKDOWN = "markdown"
    HTML = "html"
    CODE = "code"
