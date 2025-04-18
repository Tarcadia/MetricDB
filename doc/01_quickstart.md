# 1. 快速开始

## 安装依赖
```bash
pip install -r requirements.txt
```

## 启动服务
```bash
python -m metricdb.server
```

## 使用示例
### 管理指标元数据
```bash
# 创建指标
curl -X POST http://localhost:8000/metric/info/temperature \
     -H "Content-Type: application/json" \
     -d '{"desc": "设备温度", "unit": "℃"}'

# 查询指标
curl http://localhost:8000/metric/info/temperature
```

### 写入指标数据
```bash
# 添加记录
curl -X POST http://localhost:8000/metric/entry/temperature \
     -H "Content-Type: application/json" \
     -d '{"time": 1620000000, "value": 25.5}'
```

### 查询时序数据

```bash
# 获取最近1小时数据
curl "http://localhost:8000/metric/entry/temperature?start_time=1619996400&end_time=1620000000"
```
