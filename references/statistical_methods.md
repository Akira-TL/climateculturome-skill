# 统计方法适用性

| 方法 | 最低输入 | 主要注意 |
|---|---|---|
| Alpha diversity | sample-level feature matrix | 测序深度、稀释/估计方法 |
| Beta diversity | sample-level matrix | 距离度量 |
| PERMANOVA | distance matrix + metadata | 同时做 PERMDISP，受限置换 |
| ANCOM-BC | count/feature data + metadata | compositionality, covariates |
| FEAST/SourceTracker | sample-level feature table | source definition, controls |
| Network | sample-level table | compositionality, sparsity |
| RDA/db-RDA/CCA | microbiome + environment | collinearity, sample size |
| Mixed model | sample-level response | random effects / repeated structure |
| SEM | sufficient n + justified graph | 不能靠路径图制造因果 |

没有最低输入时，方法自动禁用。
