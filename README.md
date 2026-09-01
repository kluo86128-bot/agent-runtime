# agent-starter

## 1. 这是什么

这是一个基于FastAPI,redis,rq,SQLite构建的轻量级Agent Runtime.

## 2. 项目目标

该项目用于学习和实现 Agent 后端运行机制，包括任务管理、异步调度、实时状态追踪、工具调用、执行轨迹记录和异常定位。

当前版本主要提供 Agent Runtime 基础设施，后续将继续接入 LLM、Tool Calling、ReAct 和工作流编排。

## 3. 系统架构

```text
                    User
                      |
                      v
                 FastAPI API
                      |
                      v
                Task Service
              /       |        \
             v        v         v
         SQLite   Redis State  Redis Queue
                                  |
                                  v
                               RQ Worker
                                  |
                                  v
                              Agent Job
                                  |
                                  v
                                Agent
                             /         \
                            v           v
                       LLM Service   Trace System
                            |                |
                            v                v
                       Tool System         SQLite
```

## 4. 项目结构

```text
app/
├── agent/          # Agent 工作流
├── api/            # FastAPI 接口
├── config/         # 配置管理
├── db/             # SQLite 连接和 ORM 表
├── log/            # 系统日志
├── llm/            # 大模型api管理
├── redisbase/      # Redis 连接
├── redisqueue/     # RQ 队列
├── redisstate/     # 实时任务状态
├── taskservice/    # 任务生命周期管理
├── tool/           # 工具系统
├── trace/          # Agent执行记录
└── worker/         # 后台任务执行
```

## 5. 环境要求

- Python 3.10+（本项目基于 Python 3.13 开发验证）
- Redis 7.x
- Docker（用于快速启动 Redis，详见快速启动）

可选环境变量（定义于 `app/config/config.py`，均有默认值）：

| 环境变量   | 默认值    | 说明             |
| ---------- | --------- | ---------------- |
| REDIS_HOST | localhost | Redis 连接地址   |
| REDIS_PORT | 6379      | Redis 连接端口   |
| REDIS_DB   | 0         | Redis 数据库编号 |

## 6. 快速启动

> 以下步骤适用于 Windows 与 Linux，两者仅在创建虚拟环境的命令上不同。

1. 克隆项目

   ```bash
   git clone git@github-bot:kluo86128-bot/agent-runtime.git
   cd agent-runtime-starter
   ```
2. 创建虚拟环境

   Windows：

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Linux：

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. 安装依赖

   ```bash
   pip install -r requirements.txt
   ```
4. 启动 Redis

   ```bash
   docker run -d --name agent-redis -p 6379:6379 redis:7-alpine
   ```

   检查连接：

   ```bash
   docker exec -it agent-redis redis-cli ping
   ```

   预期：

   ```text
   PONG
   ```
5. 启动 API

   ```bash
   uvicorn app.main:app --reload
   ```

   访问：

   http://127.0.0.1:8000/docs
6. 启动 Worker

   在另一个终端中：

   ```bash
   rq worker agent-tasks
   ```

## 7. 设计原则

### API 与执行解耦

FastAPI 只负责接收请求和创建任务，实际 Agent 执行由独立 Worker 完成，避免长任务阻塞 HTTP 请求。

### 持久数据与实时状态分离

SQLite 保存长期任务事实和 Trace；Redis 保存任务当前运行状态和队列信息。

### Agent 与基础设施分离

Agent 只负责执行流程和调用工具，不直接处理 HTTP 请求、队列消费或数据库连接。

## 8. 测试

系统测试说明见：

`docs/system_test.md`

运行自动化测试：

```bash
pytest
```

## 9. 当前版本

### v1.3.1

已完成：

- Agent Runtime 基础架构
- 异步任务队列
- 实时状态管理
- SQLite 持久化
- Tool System
- Trace 和日志系统
- LLM Service

## 10. 未来计划

- [ ] Function Calling
- [ ] Agent Loop
- [ ] ReAct
- [ ] Memory
- [ ] LangGraph 工作流
- [ ] PostgreSQL 和生产级部署
