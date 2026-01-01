import pytest
from server import list_tools

@pytest.mark.anyio(backends=["asyncio"])
async def test_list_tools_structure():
    tools = await list_tools()
    assert isinstance(tools, list)
    # Each tool should have at least a name and description
    for tool in tools:
        assert hasattr(tool, "name")
        assert hasattr(tool, "description")
        assert tool.name is not None
        assert tool.description is not None
