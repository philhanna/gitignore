import pytest
from gitignore.config import Config


@pytest.fixture
def sample_config():
    return Config(
        editor="vim",
        file_types={
            "go": ["*.swp", ".vscode/"],
            "py": ["*.swp", "*.pyc", "__pycache__", "venv/"],
            "java": ["*.swp", "build/", "*.class"],
        },
    )
