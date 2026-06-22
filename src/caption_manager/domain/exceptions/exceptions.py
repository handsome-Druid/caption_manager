from .base import ProjectException

class NotFileError(ProjectException):
    """Raised when a given path is not a file."""
    pass

class NotDirectoryError(ProjectException):
    """Raised when a given path is not a directory."""
    pass

class EmptyFileError(ProjectException):
    """Raised when a file is empty."""
    pass