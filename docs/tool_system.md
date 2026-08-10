# Tool System 设计文档

> 本文档描述本项目的 Tool（工具）系统设计，包括系统目标、工具调用流程、模块职责、核心接口定义与版本边界。
> 文中标注「规划中」的内容为设计目标，当前代码尚未实现；其余内容与 `app/tools/` 下代码保持一致。

## 1. 系统目标

提供 Agent 可发现、可描述、可调用的工具集合。

## 2. 工具调用流程

> 以下流程为设计目标。当前版本 Agent 直接通过 `ToolRegistry` 获取工具并调用（见 `app/agents/simple_agent.py`），尚未接入 LLM。

1. Agent 获取 Tool Schema，并将其发送给 LLM
2. LLM 返回要调用的工具名以及参数
3. Agent 根据 LLM 返回的工具名和参数获取要调用的工具
4. Agent 将参数传入工具调用函数并执行
5. Agent 获取工具调用结果反馈给 LLM
6. LLM 继续推理

```text
Agent
  |
  v
Tool Registry
  |
  +------------+------------+
  v                         v
Tool Schema            Tool Instance
  |                         |
  v                         v
Parameter Schema         BaseTool
                           |
                           v
                        FileTool
                           |
                           v
                     Tool.run()
                           |
                           v
                   Tool Result Schema
```

## 3. 模块职责

### ToolRegistry

Tool 系统的统一管理入口，对应代码 `app/tools/tool_registry.py`。

负责：

- 注册 Tool（`register`）
- 根据名称获取 Tool（`get_tool`）
- 获取已注册 Tool 列表（`list_tools`）
- 导出 Tool 名称与描述

不负责 Tool 的具体业务执行逻辑。

### BaseTool

所有 Tool 的统一抽象接口，对应代码 `app/tools/base.py`。

定义：

- `name`：工具名称
- `description`：工具描述
- `run()`：工具执行入口（抽象方法，由子类实现）

### FileTool

`BaseTool` 的具体实现，提供文件系统相关能力，对应代码 `app/tools/file_tools.py`。当前以三个独立类提供：

| 类名              | 工具名         | 功能                   |
| ----------------- | -------------- | ---------------------- |
| `ReadFileTool`  | `read_file`  | 读取指定路径的文本文件 |
| `WriteFileTool` | `write_file` | 向指定路径写入文本内容 |
| `ListFilesTool` | `list_files` | 列出指定目录下的文件   |

### ToolSchema

定义 Tool 对外暴露的标准能力描述，主要供 LLM / Agent Runtime 理解 Tool：

- name
- description
- parameters

### ParameterSchema

定义 Tool 输入参数的结构，包括：

- 参数名称
- 参数类型
- 参数描述
- 是否必填

### ToolResultSchema

统一 Tool 执行结果格式，包含：

- name
- success
- result
- error

## 4. 核心接口定义

### 已注册工具

全局单例 `tool_registry`（`app/tools/tool_registry.py`）在模块加载时注册了以下工具：

| 工具名         | 描述                         |
| -------------- | ---------------------------- |
| `read_file`  | read text from a file        |
| `write_file` | write text content to a file |
| `list_files` | List files in a directory    |

### tool_schema

预期格式示例：

```json
{
  "name": "read_file",
  "description": "读取指定路径的文本文件",
  "parameters": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "需要读取的文件路径"
      }
    },
    "required": ["path"]
  }
}
```

### tool_result_schema

预期格式示例：

```json
{
  "name": "str",
  "success": "bool",
  "result": "Any",
  "error": "str | None"
}
```

## 5. 版本边界

支持：

- Tool 注册
- Tool 发现
- Schema 生成
- Tool 执行

不支持：

- 自动规划
- 多工具自主选择
- 多轮 Agent Loop
- Tool 权限控制
- Tool 超时与重试
