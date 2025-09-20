# 问题2：元数据架构设计与数据血缘追踪

## 学习目标
- 按照 DAMA-DMBOK 标准设计全面的元数据架构
- 实现数据血缘追踪系统用于影响分析
- 构建自动化元数据收集与文档化流程
- 为企业数据资产创建数据字典和业务术语表

## 背景
随着组织数据生态系统的扩展，追踪数据从来源到消费的流动对于治理、合规和运营效率变得至关重要。你需要设计并实现一个元数据管理系统，既能捕获技术和业务元数据，又能清晰展示数据血缘。

## 场景
你的组织数据经过多个转换阶段处理：
1. **源系统** → 原始数据采集
2. **数据湖** → 数据暂存与预处理
3. **数据仓库** → 业务转换
4. **分析层** → 报表与仪表盘

你的任务是构建一个元数据管理框架，追踪数据在整个管道中的流动、转换和依赖关系。

## 任务要求

### A部分：元数据架构设计（30分）
设计一个全面的元数据架构，包括：
- **技术元数据**：表结构、字段属性、数据类型、约束条件
- **业务元数据**：业务定义、数据负责人、业务规则
- **操作元数据**：作业调度、数据新鲜度、处理统计信息
- **质量元数据**：数据质量规则、校验结果、质量评分

### B部分：数据血缘实现（40分）
构建一个血缘追踪系统，能够：
- 映射跨转换层的源到目标关系
- 跟踪关键业务字段的字段级血缘
- 识别上下游依赖关系
- 支持变更管理的影响分析
- 生成血缘图和依赖矩阵

### C部分：自动化元数据收集（30分）
实现自动化流程，能够：
- 从数据库系统和文件中发现架构
- 从ETL/转换脚本中提取元数据
- 从文档中填充业务术语表
- 进行元数据校验和质量检查
- 在元数据仓库间同步更新

## 交付物
1. `metadata_schema.json` - 完整的元数据架构定义
2. `lineage_tracker.py` - 数据血缘追踪实现
3. `metadata_collector.py` - 自动化元数据收集系统
4. `business_glossary.json` - 业务术语及定义
5. `lineage_graph.html` - 交互式血缘可视化
6. `impact_analysis.py` - 变更管理影响分析工具

## 示例数据管道
你将使用如下真实数据管道：

```
Sales_DB.orders → staging.raw_orders → warehouse.fact_sales → dashboard.sales_report
     ↓               ↓                     ↓                    ↓
Customer_API → staging.raw_customers → warehouse.dim_customer → dashboard.customer_analysis
     ↓
Product_Feed → staging.raw_products → warehouse.dim_product
```

## 技术规范

### 元数据架构结构
```json
{
  "asset_id": "唯一标识符",
  "asset_type": "table|view|file|report",
  "technical_metadata": {
    "schema": {},
    "location": "",
    "format": "",
    "size": 0
  },
  "business_metadata": {
    "owner": "",
    "steward": "",
    "definition": "",
    "business_rules": []
  },
  "lineage": {
    "upstream_assets": [],
    "downstream_assets": [],
    "transformations": []
  }
}
```

### 血缘追踪功能
- **字段级血缘**：追踪字段转换和衍生过程
- **转换逻辑**：捕获 SQL、Python 或其他转换代码
- **依赖映射**：构建完整依赖关系图
- **影响分析**：识别变更影响的下游资产

## 评估标准
- **架构设计**（25%）：完整性与元数据标准符合度
- **血缘准确性**（30%）：数据流和依赖关系映射正确
- **自动化质量**（25%）：自动收集流程的有效性
- **可用性**（20%）：文档和可视化工具的清晰度

## 入门指南
```bash
# 激活虚拟环境
source ../../venv/bin/activate

# 安装额外依赖包
pip install networkx matplotlib plotly

# 生成示例管道数据
python generate_pipeline_data.py

# 运行元数据收集
python metadata_collector.py

# 生成血缘可视化
python lineage_tracker.py
```

## 业务背景
本练习模拟真实元数据管理挑战：
- **合规监管**：追踪数据来源以满足审计要求
- **变更影响**：理解系统变更对下游的影响
- **数据发现**：帮助用户查找和理解可用数据
- **质量监控**：在管道中追踪数据质量

## 高级功能（加分项）
- 与 Apache Atlas 等元数据管理工具集成
- 支持流式数据管道的实时血缘更新
- 用机器学习自动提取业务术语
- 提供元数据查询和更新的 API 接口

## 预计时间
- A部分：60分钟
- B部分：90分钟
- C部分：60分钟
- **总计：3.5小时**

## 参考资源
- [DAMA-DMBOK 元数据管理](https://dama.org/)
- [Apache Atlas 文档](https://atlas.apache.org/)
- [数据血缘最佳实践](https://www.dataversity.net/)
- [元数据管理模式](https://martinfowler.com/)