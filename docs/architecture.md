# Agent Runtime Architecture

## 1. System Goal

构建一个轻量级 AI Agent Runtime，
支持：

- 任务管理
- 工具调用
- 异步任务执行
- 状态追踪
- 执行过程记录
- 异常定位

## 2. Architecture

User

↓

FastAPI

↓

Task Service

↓

+-------------------------+

SQLite

Redis Queue

Redis State

+-------------------------+

↓

Redis Base

↓

Worker

↓

Agent Runtime

↓

LLM Service

↓

Tool System

↓

Trace / Logging

## 3. Component Responsibility

| Component     | Responsibility       |
| ------------- | -------------------- |
| FastAPI       | API入口，请求处理    |
| Task Service  | 管理任务生命周期     |
| SQLite        | 持久化任务和执行数据 |
| Redis Queue   | 异步任务调度         |
| Redis State   | 保存实时运行状态     |
| Redis Base    | 初始化redis连接      |
| Worker        | 后台执行任务         |
| Agent Runtime | Agent流程控制        |
| LLM Service   | 管理大模型 API        |
| Tool System   | 提供外部能力         |
| Config        | 管理系统配置         |
| Logging       | 系统日志记录         |
| Trace         | Agent执行轨迹记录    |
