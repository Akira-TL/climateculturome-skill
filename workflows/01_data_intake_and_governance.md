# 数据接入与治理流程

## 目标

确认“哪些数据能合法连接”。

## 必查字段

- dataset_id
- sample_id / site_code
- sampling_date
- sample_type / niche
- latitude / longitude（如需点位环境匹配）
- taxonomy key
- feature key

## 阻断条件

- 同名站点跨设计但日期不同，且无显式 linkage key；
- 缺真实坐标却要求点位气候匹配；
- 把缺失生态位当 0；
- 把 `<LOD` 当成真实 0；
- 样本级和组级表混用；
- 分组统计被误认为独立样本。

## 输出

- data asset inventory
- linkage table
- missingness report
- QC warnings
- capability matrix
