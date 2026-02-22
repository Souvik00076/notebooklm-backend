import uuid


from pathlib import Path
from .LoaderFactory import LoaderFactory
from .SplitterFactory import SplitterFactory
from .constants.enum import SplitterType


class RagFacade:

    @staticmethod
    def ingest(file_path: Path):
        loader = LoaderFactory.get_loader(file_path)
        documents = loader.load()

        parent_splitter = SplitterFactory.get_splitter(
            SplitterType.RECURSIVE_CHARACTER,
            {"chunk_size": 2000, "chunk_overlap": 200}
        )
        child_splitter = SplitterFactory.get_splitter(
            SplitterType.RECURSIVE_CHARACTER,
            {"chunk_size": 500, "chunk_overlap": 50}
        )

        parent_chunks = parent_splitter.split_documents(documents)

        child_chunks = []
        for parent_chunk in parent_chunks:
            parent_id = str(uuid.uuid4())
            parent_chunk.metadata["id"] = parent_id

            children = child_splitter.split_documents([parent_chunk])
            for child in children:
                child.metadata["parent_id"] = parent_id

            child_chunks.extend(children)
        print(parent_chunks)
        print(child_chunks)

    @staticmethod
    def retrieve():
        pass
