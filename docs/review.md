api层：接受请求，调用task_service，但没有task_service的业务逻辑

task_service:生成任务id，数据库读写操作，任务进入Redis Queue，reids state状态更新。不涉及数据表的字段，不涉及对列的定义，不涉及redis的连接

SQLite:数据表名称，字段定义。数据库地址定义，数据库连接操作。

Redis Queue：调用redisbase初始化redis连接，redis队列定义

Redis State:调用redis初始化的连接，根据task_id更新，获取，删除状态，不涉及redis服务的地址，端口具体值设置。不涉及redis连接的初始化

Redis Base:redis客户端连接的初始化

worker:调用redis_status更新状态，调用agent执行agent工作流，调用SQLite更新数据库记录。不涉及agent的工作逻辑细节

Agent :agent业务逻辑，工具调用，redis state调用更新执行状态，

调用trace记录agent工作流执行记录和错误记录。

Tool :文件读工具，文件写工具看，内容总结工具。

config:记录redis的连接地址和连接端口。

问题：数据库地址配置应归类到配置模块统一管理。

问题：缺失系统日志模块。
