# 2. 项目结构
```
metricdb/
 ├── core/ # 核心数据类型
 │   ├── metric.py # 指标模型定义
 │   ├── time.py # 时间处理模块
 │   └── ...
 ├── api/
 │   ├── info/ # 元数据接口
 │   │   ├── http.py # HTTP 路由
 │   │   └── ws.py # WebSocket 路由
 │   └── entry/ # 时序数据接口
 ├── client/ # 客户端实现
 ├── server/ # 服务端入口
 └── test/ # 测试套件
     ├── test_api.py # 接口测试
     └── test_core_*.py # 核心模块测试
```

主要模块说明：
- **Core**: 定义基础数据类型和存储引擎
- **API**: 实现对外服务接口
- **Client**: 提供本地/远程访问客户端
- **Server**: 基于 FastAPI 的服务端实现

