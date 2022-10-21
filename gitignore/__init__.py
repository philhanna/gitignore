FILENAME = '.gitignore'
DEFAULT_KEY = 'DEFAULT'
DEFAULT_VALUES = [
    '*.swp'
]
EDITOR = 'vim'

from .gitignore_file import GitignoreFile

__all__ = [
    'FILENAME',
    'DEFAULT_KEY',
    'DEFAULT_VALUES',
    'EDITOR',
    'GitignoreFile',
]