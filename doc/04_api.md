# 4. API 设计

## 接口规范
| 资源   | HTTP 方法 | 路径格式                 | 功能         |
|--------|-----------|--------------------------|--------------|
| 元数据 | GET       | /metric/info/{key}       | 查询指标定义 |
|        | POST      | /metric/info/{key}       | 更新指标定义 |
| 时序数据| GET       | /metric/entry/{key}      | 查询数据记录 |
|        | POST      | /metric/entry/{key}      | 添加数据记录 |

## WebSocket 支持
- `/metric/info`: 实时元数据更新通道
- `/metric/entry`: 流式数据写入接口

## 查询参数
```python
class QueryParams:
    start_time: int    # 起始时间戳
    end_time: int      # 结束时间戳
    test: Optional[str] # 测试过滤
    dut: List[str]     # 设备过滤
```

