from .caption_reader import CaptionReaderServicePort
from .auto_remove import AutoRemoveServicePort
from .custom_remove import CustomRemoveServicePort
from .add_prefix import AddPrefixServicePort
from .folder_resolver import FolderResolverServicePort

__all__ = [
    "CaptionReaderServicePort",
    "AutoRemoveServicePort",
    "CustomRemoveServicePort",
    "AddPrefixServicePort",
    "FolderResolverServicePort",
]