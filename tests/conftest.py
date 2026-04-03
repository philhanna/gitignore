import pytest
from gitignore.config import Config


@pytest.fixture
def sample_config():
    return Config(
        editor="vim",
        file_types={
            "go": [".vscode/"],
            "py": ["*.pyc", "__pycache__", "venv/"],
            "java": ["build/", "*.class"],
        },
    )
