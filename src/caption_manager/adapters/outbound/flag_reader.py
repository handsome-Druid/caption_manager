import sys
from pathlib import Path
from logging import getLogger

from caption_manager.domain.exceptions import NotFileError, EmptyFileError

logger = getLogger(__name__)

class FlagReaderImpl:

    def read(self, file: str):
        if not file.endswith('.txt'):
            file += '.txt'
        file_path = (
            Path(sys.argv[0]).parent / Path(file).resolve()
            if "__compiled__" in globals() else
            Path(__file__).parents[4] / Path(file).resolve()
        )
        if not file_path.is_file():
            raise NotFileError(f"{file_path} is not a valid file.")

        with open(file_path, mode='r', encoding='utf-8') as f:
            content = f.read()
        cleaned_items = filter(None, map(str.strip, content.replace('\n', ',').split(',')))
        cleaned_items = list(cleaned_items)
        if not cleaned_items:
            raise EmptyFileError(f"No valid flags found in {file_path}.")
        return cleaned_items