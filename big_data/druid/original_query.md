## 完整查询模版

```json
{
  "queryType": "groupBy",
  "dataSource": "sample_datasource",
  "granularity": "day",
  "dimensions": ["country", "device"],
  "limitSpec": { "type": "default", "limit": 5000, "columns": ["country", "data_transfer"] },
  "filter": {
    "type": "and",
    "fields": [
      { "type": "selector", "dimension": "carrier", "value": "AT&T" },
      { "type": "or",
        "fields": [
          { "type": "selector", "dimension": "make", "value": "Apple" },
          { "type": "selector", "dimension": "make", "value": "Samsung" }
        ]
      }
    ]
  },
  "aggregations": [
    { "type": "longSum", "name": "total_usage", "fieldName": "user_count" },
    { "type": "doubleSum", "name": "data_transfer", "fieldName": "data_transfer" }
  ],
  "postAggregations": [
    { "type": "arithmetic",
      "name": "avg_usage",
      "fn": "/",
      "fields": [
        { "type": "fieldAccess", "fieldName": "data_transfer" },
        { "type": "fieldAccess", "fieldName": "total_usage" }
      ]
    }
  ],
  "intervals": [ "2012-01-01T00:00:00.000/2012-01-03T00:00:00.000" ],
  "having": {
    "type": "greaterThan",
    "aggregation": "total_usage",
    "value": 100
  }
}
```

## 查询类型

- [Scan](http://www.apache-druid.cn/Querying/scan.html) 操作被用来做不进行聚合的查询（非GroupBy和DISTINCT）
- [Timeseries](http://www.apache-druid.cn/Querying/timeseriesquery.html) 操作被用来查询GROUP BY `FLOOR(__time TO <unit>)` 或者 `TIME_FLOOR(__time, period)`, 不再有其他分组表达式，也没有HAVING或者LIMIT子句，没有嵌套，要么是没有ORDER BY、要么是有与GROUP BY表达式相同的ORDER BY。它还将Timeseries用于具有聚合函数但没有分组依据的"总计"查询。这种查询类型利用了Druid段是按时间排序的这一事实。不能输出`DIMENSION`信息。`Timeseries` 会给没有数据`bucket`补充0 ，如果不希望补0，可以在`context`指定`skipEmptyBuckets=true` 
- [TopN](http://www.apache-druid.cn/Querying/topn.html) 默认情况下用于按单个表达式分组、具有ORDER BY和LIMIT子句、没有HAVING子句和不嵌套的查询。但是，在某些情况下，TopN查询类型将提供近似的排名和结果；如果要避免这种情况，请将"useApproximateTopN"设置为"false"。TopN结果总是在内存中计算的。有关详细信息，请[参阅TopN文档](http://www.apache-druid.cn/Querying/topn.html)。
- [GroupBy](http://www.apache-druid.cn/Querying/groupby.html) 用于所有其他聚合，包括任何嵌套的聚合查询。Druid的GroupBy是一个传统的聚合引擎：它提供<font color='red'>精确的结果和排名</font>，并支持多种功能。GroupBy可以在内存中聚合，但如果没有足够的内存来完成查询，它可能会溢出到磁盘。如果您在GROUP BY子句中使用相同的表达式进行ORDER BY，或者根本没有ORDER BY，则结果将通过Broker从数据进程中流回。如果查询具有未出现在GROUP BY子句（如聚合函数）中的ORDER BY引用表达式，则Broker将在内存中具体化结果列表，最大值不超过LIMIT（如果有的话）。有关优化性能和内存使用的详细信息，请参阅[GroupBy文档](http://www.apache-druid.cn/Querying/groupby.html)。

## 时间过滤器

对于所有原生查询类型，只要有可能，`__time` 列上的过滤器将被转换为顶级查询的"interval"，这允许Druid使用其全局时间索引来快速调整必须扫描的数据集。请考虑以下（非详尽）时间过滤器列表，这些时间过滤器将被识别并转换为 "intervals"：

- `__time >= TIMESTAMP '2000-01-01 00:00:00'` (与绝对时间相比)
- `__time >= CURRENT_TIMESTAMP - INTERVAL '8' HOUR` (与相对时间相比)
- `FLOOR(__time TO DAY) = TIMESTAMP '2000-01-01 00:00:00'` (指定的一天)

## 查询过滤器

Filter是一个JSON对象，指示查询的计算中应该包含哪些数据行。它本质上相当于SQL中的WHERE子句。Apache Druid支持以下类型的过滤器。

**注意**

过滤器通常情况下应用于维度列，但是也可以使用在聚合后的指标上，例如，参见 [filtered-aggregator](http://www.apache-druid.cn/Querying/Aggregations.html#过滤聚合器) 和 [having-filter](http://www.apache-druid.cn/Querying/having.html)

### 选择过滤器

> `"filter": { "type": "selector", "dimension": <dimension_string>, "value": <dimension_value_string> }`
>
> 等价于 `WHERE <dimension_string> = '<dimension_value_string>'`
>
> 即 key = value 比较

### 列比较过滤器

> `"filter": { "type": "columnComparison", "dimensions": [<dimension_a>, <dimension_b>] }`
>
> 等价于`WHERE <dimension_a> = <dimension_b>`
>
> 即 columnA = columnB

### 正则表达式过滤器

> `"filter": { "type": "regex", "dimension": <dimension_string>, "pattern": <pattern_string> }`
>
> 类似于选择过滤器
>
> 匹配所有的java正则表达式

### 逻辑表达式过滤器

* **AND** 

  >  `"filter": { "type": "and", "fields": [<filter>, <filter>, ...] }`
  >
  > 其中，filter可以是上述任一种过滤器

* **OR** 

  >  `"filter": { "type": "or", "fields": [<filter>, <filter>, ...] }`
  >
  > 其中，filter可以是上述任一种过滤器

* **NOT** 

  >  `"filter": { "type": "not", "fields": [<filter>, <filter>, ...] }`
  >
  > 其中，filter可以是上述任一种过滤器

### 搜索过滤器

> 搜索过滤器可以使用在部分字符串上进行过滤匹配
>
> ```json
> {
>     "filter": {
>         "type": "search",
>         "dimension": "product",
>         "query": {
>           "type": "insensitive_contains",
>           "value": "foo"
>         }
>     }
> }
> ```

| 属性           | 描述                                                         | 是否必须 |
| -------------- | ------------------------------------------------------------ | -------- |
| `type`         | 该值始终为`search`                                           | 是       |
| `dimension`    | 要执行搜索的维度                                             | 是       |
| `query`        | 搜索类型的详细JSON对象。 详情可看下边                        | 是       |
| `extractionFn` | 对维度使用的 [提取函数](http://www.apache-druid.cn/Querying/dimensionspec.html) | 否       |

*Contains*

| 属性            | 描述                           | 是否必须          |
| --------------- | ------------------------------ | ----------------- |
| `type`          | 该值始终为`contains`           | 是                |
| `value`         | 要执行搜索的字符串值           | 是                |
| `caseSensitive` | 两个字符串比较时是否忽略大小写 | 否（默认为false） |

*Insensitive Contains*

| 属性    | 描述                             | 是否必须 |
| ------- | -------------------------------- | -------- |
| `type`  | 该值始终为`insensitive_contains` | 是       |
| `value` | 要执行搜索的字符串值             | 是       |

注意：一个"insensitive_contains"搜索等价于一个具有值为false或者未提供的"caseSensitive"的"contains"搜索

*Fragment*

| 属性            | 描述                           | 是否必须          |
| --------------- | ------------------------------ | ----------------- |
| `type`          | 该值始终为`fragment`           | 是                |
| `values`        | 要执行搜索的字符串值数组       | 是                |
| `caseSensitive` | 两个字符串比较时是否忽略大小写 | 否（默认为false） |

### In过滤器

> 执行条件为`In`的SQL
>
> ```json
> {
>     "type": "in",
>     "dimension": "outlaw",
>     "values": ["Good", "Bad", "Ugly"]
> }
> ```

### **Like过滤器**

Like过滤器被用于基本的通配符搜索，等价于SQL中的LIKE语句。 特定的符号支持"%"(匹配任意数量的字符)和"_"(匹配任意单个字符)

| 属性           | 类型                                                         | 描述                                                         | 是否必须 |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------- |
| `type`         | String                                                       | 该值始终为`fragment`                                         | 是       |
| `dimension`    | String                                                       | 需要过滤的维度                                               | 是       |
| `pattern`      | String                                                       | LIKE模式， 例如"foo%"或者"__bar"                             | 是       |
| `escape`       | String                                                       | 可以用来转义特殊字符的转义符号                               | 否       |
| `extractionFn` | [提取函数](http://www.apache-druid.cn/Querying/dimensionspec.html) | 对维度使用的 [提取函数](http://www.apache-druid.cn/Querying/dimensionspec.html) | 否       |

Like过滤器支持使用提取函数，详情可见 [带提取函数的过滤器](http://www.apache-druid.cn/Querying/filters.html#带提取函数的过滤器)

下边的Like过滤器表达了条件 `last_name LIKE "D%"`, 即： last_name以D开头

```json
{
    "type": "like",
    "dimension": "last_name",
    "pattern": "D%"
}
```

## Having

having语法用来通过对聚合后的值指定特定条件来决定从GroupBy的结果中返回符合条件的行，基本等价于SQL语法中的**HAVING**

#### 查询过滤器

所有的[Druid查询过滤器](http://www.apache-druid.cn/Querying/filters.html)都可以被用来使用在查询体的Having部分中。 一个查询过滤器的HavingSpec如下：

```json
{
    "queryType": "groupBy",
    "dataSource": "sample_datasource",
    ...
    "having":
    {
      "type" : "filter",
      "filter" : <any Druid query filter>
    }
}
```

#### 数值过滤器

最简单的having子句是数字过滤器。[数字过滤器](http://www.apache-druid.cn/Querying/having.html#:~:text=%E4%BD%BF%E7%94%A8%E8%BF%87%E6%BB%A4%E5%99%A8%E3%80%82-,%E6%95%B0%E5%80%BC%E8%BF%87%E6%BB%A4%E5%99%A8(Numeric%20Filters),-%E6%9C%80%E7%AE%80%E5%8D%95%E7%9A%84)可以用作过滤器的更复杂布尔表达式的基过滤器。

```json
{
    "queryType": "groupBy",
    "dataSource": "sample_datasource",
    ...
    "having":
    {
      "type": "greaterThan",
      "aggregation": "<aggregate_metric>",
      "value": <numeric_value>
    }
}
```

#### 维度选择过滤器

```json
{
    "queryType": "groupBy",
    "dataSource": "sample_datasource",
    ...
    "having":
    {
      "type": "dimSelector",
      "dimension": "<dimension>",
      "value": <dimension_value>
    }
}
```

#### 逻辑表达式过滤器

存在三种逻辑表达式分别是 `AND`,`OR`,`NOT`

```json
{
    "queryType": "groupBy",
    "dataSource": "sample_datasource",
    ...
    "having":
        {
            "type": "and",
            "havingSpecs": [
                {
                    "type": "greaterThan",
                    "aggregation": "<aggregate_metric>",
                    "value": <numeric_value>
                },
                {
                    "type": "lessThan",
                    "aggregation": "<aggregate_metric>",
                    "value": <numeric_value>
                }
            ]
        }
}
```

### 排序和限制

`limitSpec`字段提供了对GroupBy结果集进行排序和限制的功能。 如果是对一个维度进行聚合且根据一个指标进行排序， 我们强烈建议使用 [TopN查询](http://www.apache-druid.cn/Querying/topn.html) 来替代， 性能会大大的提高。 可选项有：**[DefaultLimitSpec](http://www.apache-druid.cn/Querying/limitspec.html#:~:text=%E5%8F%AF%E9%80%89%E9%A1%B9%E6%9C%89%EF%BC%9A-,DefaultLimitSpec,-%E9%BB%98%E8%AE%A4%E7%9A%84limitSpec)**、**[OrderByColumnSpec](http://www.apache-druid.cn/Querying/limitspec.html#:~:text=%E5%BD%BC%E6%AD%A4%E5%AF%B9%E9%BD%90%E3%80%82-,OrderByColumnSpec,-OrderbyColumnSpec%E6%A0%87%E6%98%8E%E5%A6%82%E4%BD%95)**

## 客户端API

在Druid SQL查询中，可以通过HTTP方式发送POST请求到 `/druid/v2/sql` 来执行SQL查询。该请求应该是一个带有 "query" 字段的JSON对象，例如： `{"query" : "SELECT COUNT(*) FROM data_source WHERE foo = 'bar'"}`

**Request**

| 属性           | 描述                                                         | 默认值   |
| -------------- | ------------------------------------------------------------ | -------- |
| `query`        | SQL                                                          | 必填，无 |
| `resultFormat` | 查询结果的格式，详情查看下边的response部分                   | object   |
| `header`       | 是否包含一个请求头，详情查看下边的response部分               | false    |
| `context`      | 包括 [连接上下文](http://www.apache-druid.cn/Querying/druidsql.html#连接上下文) 参数JSON对象 | {}(空)   |
| `parameters`   | 参数化查询的查询参数列表。列表中的每个参数都应该是一个JSON对象，比如 `{"type"："VARCHAR"，"value"："foo"}` 。`type` 应为SQL类型；有关支持的SQL类型的列表，请参见 [数据类型](http://www.apache-druid.cn/Querying/druidsql.html#数据类型) |          |

### resultFormat

> Druid SQL的HTTP POST API支持一个可变的结果格式，可以通过"resultFormat"参数来指定，例如：
>
> ```sql
> {
>   "query" : "SELECT COUNT(*) FROM data_source WHERE foo = 'bar' AND __time > TIMESTAMP '2000-01-01 00:00:00'",
>   "resultFormat" : "object"
> }
> ```

支持的结果格式为：

| 格式          | 描述                                                         | Content-Type     |
| ------------- | ------------------------------------------------------------ | ---------------- |
| `object`      | 默认值，JSON对象的JSON数组。每个对象的字段名都与SQL查询返回的列匹配，并且按与SQL查询相同的顺序提供。 | application/json |
| `array`       | JSON数组的JSON数组。每个内部数组按顺序都有与SQL查询返回的列匹配的元素。 | application/json |
| `objectLines` | 与"object"类似，但是JSON对象由换行符分隔，而不是包装在JSON数组中。如果您没有流式JSON解析器的现成访问权限，这可以使将整个响应集解析为流更加容易。为了能够检测到被截断的响应，此格式包含一个空行的尾部。 | text/plain       |
| `arrayLines`  | 与"array"类似，但是JSON数组由换行符分隔，而不是包装在JSON数组中。如果您没有流式JSON解析器的现成访问权限，这可以使将整个响应集解析为流更加容易。为了能够检测到被截断的响应，此格式包含一个空行的尾部。 | text/plain       |
| `csv`         | 逗号分隔的值，每行一行。单个字段值可以用双引号括起来进行转义。如果双引号出现在字段值中，则通过将它们替换为双引号（如`""this""`）来对其进行转义。为了能够检测到被截断的响应，此格式包含一个空行的尾部。 | text/csv         |

### Header

您还可以通过在请求中将"header"设置为true来请求头，例如：

```json
{
  "query" : "SELECT COUNT(*) FROM data_source WHERE foo = 'bar' AND __time > TIMESTAMP '2000-01-01 00:00:00'",
  "resultFormat" : "arrayLines",
  "header" : true
}
```

在这种情况下，返回的第一个结果将是头。对于 `csv`、`array` 和 `arrayline` 格式，标题将是列名列表。对于 `object` 和 `objectLines` 格式，头将是一个对象，其中键是列名，值为空。

在发送响应体之前发生的错误将以JSON格式报告，状态代码为HTTP 500，格式与 [原生Druid查询错误](http://www.apache-druid.cn/Querying/makeNativeQueries.html#查询错误) 相同。如果在发送响应体时发生错误，此时更改HTTP状态代码或报告JSON错误已经太迟，因此响应将简单地结束流，并且处理您的请求的Druid服务器将记录一个错误。

作为调用者，正确处理响应截断非常重要。这对于"object"和"array"格式很容易，因为的截断响应将是无效的JSON。对于面向行的格式，您应该检查它们都包含的尾部：结果集末尾的一个空行。如果通过JSON解析错误或缺少尾随的换行符检测到截断的响应，则应假定响应由于错误而未完全传递。

### context

| 参数                          | 描述                                                         | 默认值                                                       |
| ----------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `sqlQueryId`                  | 本次SQL查询的唯一标识符。对于HTTP客户端，它在 `X-Druid-SQL-Query-Id` 头中返回 | 自动生成                                                     |
| `sqlTimeZone`                 | 设置此连接的时区，这将影响时间函数和时间戳文本的行为。应该是时区名称，如"America/Los_Angeles"或偏移量，如"-08:00" | Broker配置中的 `druid.sql.planner.sqlTimeZone` , 默认为：UTC |
| `useApproximateCountDistinct` | 是否对 `COUNT(DISTINCT foo)` 使用近似基数算法                | Broker配置中的 `druid.sql.planner.useApproximateCountDistinct`， 默认为：true |
| `useApproximateTopN`          | 当SQL查询可以这样表示时，是否使用近似[TopN查询](http://www.apache-druid.cn/Querying/topn.html)。如果为false，则将使用精确的 [GroupBy查询](http://www.apache-druid.cn/Querying/groupby.html)。 | Broker配置中的 `druid.sql.planner.useApproximateTopN`， 默认为：true |



## 数据源类型

- [table](http://www.apache-druid.cn/Querying/datasource.html#table)

> 表数据源是最常见的类型，该类数据源可以在 [数据摄取](http://www.apache-druid.cn/DataIngestion/ingestion.html) 后获得。它们被分成若干段，分布在集群中，并且并行地进行查询。

- [lookup](http://www.apache-druid.cn/Querying/datasource.html#lookup)

> Lookup数据源对应于Druid的键值 [lookup](http://www.apache-druid.cn/Querying/lookups.html) 对象。在[Druid SQL](http://www.apache-druid.cn/Querying/druidsql.html) 中，它们驻留在 `lookup` schema中。它们会被预加载到所有服务器的内存中，因此可以快速访问它们。可以使用 [join运算符](http://www.apache-druid.cn/Querying/datasource.html#join) 将它们连接到常规表上。
>
> Lookup数据源是面向键值的，总是正好有两列：`k`（键）和 `v`（值），而且这两列始终是字符串

- [union](http://www.apache-druid.cn/Querying/datasource.html#union)

> Union数据源允许您将两个或多个表数据源视为单个数据源。联合的数据源不需要具有相同的结构。如果它们不完全匹配，那么存在于一个表中而不是另一个表中的列将被视为在**它们不存在的表中包含所有空值**。
>
> SQL不可用

- [inline](http://www.apache-druid.cn/Querying/datasource.html#inline)

> 可以查询嵌入在查询体本身中的一小波数据，SQL不支持

- [query](http://www.apache-druid.cn/Querying/datasource.html#query)

> 允许发出子查询

- [join](http://www.apache-druid.cn/Querying/datasource.html#join)

> Join数据源允许您对两个数据源执行SQL样式的联接。相互堆叠连接允许您任意连接多个数据源。

## [元数据表](http://www.apache-druid.cn/Querying/druidsql.html#:~:text=%E9%BB%98%E8%AE%A4%E4%B8%BA%EF%BC%9Atrue-,%E5%85%83%E6%95%B0%E6%8D%AE%E8%A1%A8,-Druid%20Broker%E4%BB%8E)

## <font color="red">注意事项：</font>

### 近似，非精确值

- 默认情况下，`COUNT(DISTINCT col)` 聚合函数使用 [HyperLogLog](http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf) 的变体，HyperLogLog是一种快速近似的DISTINCT计数算法。如果通过查询上下文或通过Broker配置将"useApproximateCountDistinct"设置为"false"，Druid SQL将切换到精确计数
- 对于具有ORDER BY和LIMIT的单列GROUP BY查询，可以采用使用了近似算法的TopN引擎执行查询。如果通过查询上下文或通过Broker配置将"useApproximateTopN"设置为"false"，Druid SQL将切换到精确的分组算法
- 标记为使用草图或近似（例如近似计数不同）的聚合函数不管配置如何,始终是近似的
- TopN是近似查询，因为每个数据进程将对其前K个结果进行排序，并且只将那些前K个结果返回给Broker。在Druid中K的默认值是 `max(1000, threshold)`。在实践中，这意味着，如果你要求查询前1000个数据，前900个数据的正确性将为100%，之后的结果排序将无法保证。通过增加阈值可以使TopNs更加精确。

### 不支持特性

- 原生数据源（table, lookup, subquery）与系统表的JOIN操作
- 左侧和右侧的表达式之间不相等的JOIN条件
- OVER子句，`LAG` 和 `LEAD` 等分析型函数
- OFFSET子句
- DDL和DML
- 在 [元数据表](http://www.apache-druid.cn/Querying/druidsql.html#元数据表) 上使用Druid特性的函数，比如 `TIME_PARSE` 和 `APPROX_QUANTILE_DS`

### 原生查询支持，但是SQL不支持

- [UNION数据源](http://www.apache-druid.cn/Querying/datasource.html#union)

- [INLINE数据源](http://www.apache-druid.cn/Querying/datasource.html#inline)
- [空间过滤器](http://www.apache-druid.cn/Querying/spatialfilter.html)
- [查询取消](http://www.apache-druid.cn/Querying/makeNativeQueries.html#查询取消)

### Order By

对于非聚合查询，**ORDER BY**只能按 `__time` 排序


