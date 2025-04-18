# 3. 核心模块

## 基础类型
- `Time`: 统一时间戳处理（纳秒精度）
- `MetricKey`: 指标唯一标识符（字符串类型）
- `TestId/DutId`: 测试/设备标识符

## 核心模型
```python
class TMetricInfo:
    key: str           # 指标键
    desc: str          # 指标描述
    unit: str          # 计量单位
    create_time: int   # 创建时间戳

class TMetricEntry:
    time: int          # 记录时间
    value: float       # 指标数值
    test: Optional[str] # 关联测试ID
    dut: Set[str]      # 关联设备集合
```

## 存储引擎
`MetricDB`类提供：

- 内存索引的元数据管理
- 基于时间分片的存储优化
- 自动化的数据持久化

