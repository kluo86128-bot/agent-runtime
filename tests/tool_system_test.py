import json

from app.tools.tool_registry import ToolRegistry
from app.tools.file_tools import (
    ReadFileTool,
    WriteFileTool,
    ListFilesTool,
)
from app.tools.schema import ToolResultSchema


def build_registry():

    registry = ToolRegistry()

    registry.register(ReadFileTool())
    registry.register(WriteFileTool())
    registry.register(ListFilesTool())

    return registry


def test_discover_tools():

    print("\n===== Test 1: Discover Tools =====")

    registry = build_registry()

    schemas = registry.get_tool_schema()

    for schema in schemas:
        print(
            json.dumps(
                schema,
                indent=4,
                ensure_ascii=False
            )
        )

    assert len(schemas) == 3

    assert all(
        {"name", "description", "parameters"} <= set(schema.keys())
        for schema in schemas
    )

    print("Discover Tools PASS")


def test_get_tool():

    print("\n===== Test 2: Get Tool =====")

    registry = build_registry()

    tool = registry.get_tool(
        "read_file"
    )

    print(tool)

    assert isinstance(tool, ReadFileTool)

    assert tool.name == "read_file"

    print("Get Tool PASS")


def test_get_missing_tool():

    print("\n===== Test 3: Get Missing Tool =====")

    registry = build_registry()

    result = registry.get_tool(
        "not_exist"
    )

    print(result)

    assert isinstance(result, ValueError)

    assert "Tool not found:not_exist" in str(result)

    print("Get Missing Tool PASS")


def test_execute_tool():

    print("\n===== Test 4: Execute Tool Success =====")

    registry = build_registry()

    tool = registry.get_tool(
        "write_file"
    )

    result = tool.execute(
        path="test_output/test.txt",
        content="hello agent"
    )

    print(result)

    assert isinstance(result, ToolResultSchema)

    assert result.success is True

    print("Execute Tool Success PASS")


def test_execute_tool_error():

    print("\n===== Test 5: Execute Tool Error =====")

    registry = build_registry()

    tool = registry.get_tool(
        "read_file"
    )

    result = tool.execute(
        path="not_exist.txt"
    )

    print(result)

    assert isinstance(result, ToolResultSchema)

    assert result.success is False

    assert result.error != ""

    print("Execute Tool Error PASS")


if __name__ == "__main__":

    test_discover_tools()

    test_get_tool()

    test_get_missing_tool()

    test_execute_tool()

    test_execute_tool_error()

    print("\n===== ALL PASS =====")
