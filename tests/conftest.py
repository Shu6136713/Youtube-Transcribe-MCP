"""
Pytest configuration file to ensure proper module imports.
This file adds the project root to the Python path so that
test files can import modules from the parent directory.
"""
import sys
from pathlib import Path
import pytest

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure anyio to only use asyncio backend
@pytest.fixture
def anyio_backend():
    return 'asyncio'
