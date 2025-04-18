# 5. 客户端与服务端

## 服务端特性
- 基于 Uvicorn 的异步服务
- 支持 SQLite 后端存储
- 配置项：
  ```python
  app = MdbAPI(
      db_path="metricdb.db",  # 数据库路径
      cache_size=1000        # 内存缓存条目数
  )
  ```

## 客户端类型
- 本地客户端：直连数据库引擎
- 远程客户端：通过 HTTP/WebSocket 通信

## 使用示例
```python
from metricdb.client import MdbClient

# 创建远程客户端
client = MdbClient.remote("http://localhost:8000")

# 查询数据
entries = client.query_metric_entry(
    key="temperature",
    start_time=1619996400,
    end_time=1620000000
)
```