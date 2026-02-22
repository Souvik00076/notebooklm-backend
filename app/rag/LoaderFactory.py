from typing import BinaryIO

from langchain_community.document_loaders import (
    PyPDFLoader, 
    Docx2txtLoader, 
    TextLoader,
    UnstructuredWordDocumentLoader
)
from langchain_community.document_loaders.base import BaseLoader

from app.rag.constants.enum import DocumentType
from app.rag.RagException import LoaderNotFoundException

from pathlib import Path


class LoaderFactory:
    _loaders = {
        DocumentType.PDF: PyPDFLoader,
        DocumentType.DOC: UnstructuredWordDocumentLoader,
        DocumentType.DOCX: Docx2txtLoader,
        DocumentType.TXT: TextLoader,
    }

    @classmethod
    def get_loader(cls, file_path: Path) -> BaseLoader:
        with open(file_path, "rb") as file:
            doc_type = cls._get_document_type(file)
        if doc_type is None:
            raise LoaderNotFoundException(
                f"No loader found for file: {file_path}")
        loader_class = cls._loaders[DocumentType(doc_type)]
        return loader_class(file_path)

    @staticmethod
    def _get_document_type(file: BinaryIO) -> str | None:
        """Detect document type based on magic bytes."""
        magic_bytes = file.read(8)
        file.seek(0)  # Reset file pointer

        # PDF: starts with %PDF
        if magic_bytes[:4] == b"%PDF":
            return DocumentType.PDF.value

        # DOC: starts with D0 CF 11 E0 (OLE2/CFB format - legacy Word format)
        if magic_bytes[:4] == b"\xD0\xCF\x11\xE0":
            return DocumentType.DOC.value

        # DOCX: starts with PK (ZIP format)
        if magic_bytes[:2] == b"PK":
            return DocumentType.DOCX.value

        # TXT: check if content is valid UTF-8 text
        try:
            content = file.read(1024)
            file.seek(0)  # Reset file pointer
            content.decode("utf-8")
            return DocumentType.TXT.value
        except UnicodeDecodeError:
            return None
