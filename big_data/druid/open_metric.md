1. 开启指标

   在不同节点进程的runtime.properties配置中增加以下内容

   ```properties
   druid.emitter=logging
   druid.emitter.logging.logLevel=info
   druid.monitoring.emissionPeriod=PT1M
   druid.monitoring.monitors=["org.apache.druid.client.cache.CacheMonitor","org.apache.druid.java.util.metrics.CpuAcctDeltaMonitor","org.apache.druid.java.util.metrics.JvmMonitor","org.apache.druid.java.util.metrics.JvmThreadsMonitor","org.apache.druid.server.metrics.EventReceiverFirehoseMonitor","org.apache.druid.server.metrics.QueryCountStatsMonitor"]
   ```

   其中不同节点`druid.monitoring.monitors`按照下面的监控配置

   broker

   ```sh
   "org.apache.druid.client.cache.CacheMonitor","org.apache.druid.java.util.metrics.CpuAcctDeltaMonitor","org.apache.druid.java.util.metrics.JvmMonitor","org.apache.druid.java.util.metrics.JvmThreadsMonitor","org.apache.druid.server.metrics.EventReceiverFirehoseMonitor","org.apache.druid.server.metrics.HistoricalMetricsMonitor","org.apache.druid.server.metrics.QueryCountStatsMonitor"
   ```

   coordinator

   ```sh
   "org.apache.druid.client.cache.CacheMonitor","org.apache.druid.java.util.metrics.CpuAcctDeltaMonitor","org.apache.druid.java.util.metrics.JvmMonitor","org.apache.druid.java.util.metrics.JvmThreadsMonitor","org.apache.druid.server.metrics.EventReceiverFirehoseMonitor","org.apache.druid.server.metrics.TaskCountStatsMonitor"
   ```

   historical

   ```sh
   "org.apache.druid.client.cache.CacheMonitor","org.apache.druid.java.util.metrics.CpuAcctDeltaMonitor","org.apache.druid.java.util.metrics.JvmMonitor","org.apache.druid.java.util.metrics.JvmThreadsMonitor","org.apache.druid.server.metrics.EventReceiverFirehoseMonitor","org.apache.druid.server.metrics.HistoricalMetricsMonitor","org.apache.druid.server.metrics.QueryCountStatsMonitor"
   ```

   middleManager

   ```sh
   "org.apache.druid.client.cache.CacheMonitor","org.apache.druid.java.util.metrics.CpuAcctDeltaMonitor","org.apache.druid.java.util.metrics.JvmMonitor","org.apache.druid.java.util.metrics.JvmThreadsMonitor","org.apache.druid.server.metrics.EventReceiverFirehoseMonitor"
   ```

   roter

   ```sh
   "org.apache.druid.client.cache.CacheMonitor","org.apache.druid.java.util.metrics.CpuAcctDeltaMonitor","org.apache.druid.java.util.metrics.JvmMonitor","org.apache.druid.java.util.metrics.JvmThreadsMonitor","org.apache.druid.server.metrics.EventReceiverFirehoseMonitor","org.apache.druid.server.metrics.QueryCountStatsMonitor"
   ```

2. 增加`/proc/self`目录，如果出现`Read-only file system`，需要增加软连接

   任一目录增加 ，如`/Users/saijie.gao`增加`/proc/self`

   ```sh
   mkdir	/Users/saijie.gao/proc/self
   sudo vim /etc/synthetic.conf
   #增加以下内容：
   	proc	/Users/saijie.gao/proc ## 中间的空格一定要是 tab，保存后重启
   ```

3. 重启`druid`

   指标日志记录位置位于`apache-druid-0.22.0/conf/druid/single-server/micro-quickstart/_common/log4j.xml`的 `baseDir`属性目录

4. 常用指标

   broker

   | 名称             | 描述                                                         | 展示维度                                         | 正常值 |
   | ---------------- | ------------------------------------------------------------ | ------------------------------------------------ | ------ |
   | query/time       | 完成查询所需的毫秒数。                                       | common                                           | < 1 S  |
   | query/bytes      | 查询响应中返回的字节数                                       | common                                           |        |
   | query/node/time  | 查询单个历史/实时进程所需的毫秒数。                          | ID、状态、服务器                                 | < 1 S  |
   | query/node/bytes | 查询单个历史/实时进程返回的字节数。                          | ID、状态、服务器                                 |        |
   | query/node/ttfb  | 第一个字节的时间。在 Broker 开始接收来自各个历史/实时进程的响应之前经过了毫秒。 | ID、状态、服务器                                 | < 1 S  |
   | query/count      | 总查询数                                                     | 此指标仅在包含 QueryCountStatsMonitor 模块时可用 |        |
   | sqlQuery/time    | 完成 SQL 查询所需的毫秒数                                    |                                                  | < 1 S  |

   Historical

   | 名称                       | 描述                                                     | 展示维度                                         | 正常值  |
   | -------------------------- | -------------------------------------------------------- | ------------------------------------------------ | ------- |
   | query/time                 | 完成查询所需的毫秒数                                     | common                                           | < 1 S   |
   | query/segment/time         | 查询单个段所用的毫秒数。包括从磁盘分页的时间             | ID、状态、服务器                                 |         |
   | query/wait/time            | 等待扫描段所花费的毫秒数                                 | ID、Segment                                      | < 1 S   |
   | segment/scan/pending       | 队列中等待扫描的段数。                                   |                                                  | 约等于0 |
   | query/segmentAndCache/time | 查询单个段或命中缓存所需的毫秒数（如果在历史进程中启用） | ID、Segment                                      | < 1 S   |
   | query/count                | 总查询数                                                 | 此指标仅在包含 QueryCountStatsMonitor 模块时可用 |         |
   | sqlQuery/time              | 完成 SQL 查询所需的毫秒数。                              |                                                  | < 1 S   |

   Real-time

   | 名称                      | 描述                       | 展示维度                                                     | 正常值   |
   | ------------------------- | -------------------------- | ------------------------------------------------------------ | -------- |
   | `query/time`              | 完成查询所需的毫秒数。     | 常见：dataSource、type、interval、hasFilters、duration、context、remoteAddress、id。聚合查询：numMetrics、numComplexMetrics。分组依据：numDimensions。TopN：阈值，维度。 | < 1s     |
   | `query/wait/time`         | 等待扫描段所花费的毫秒数。 | id，段。                                                     | 几百毫秒 |
   | `segment/scan/pending`    | 队列中等待扫描的段数。     |                                                              | 接近于 0 |
   | `query/count`             | 总查询数                   | 此指标仅在包含 QueryCountStatsMonitor 模块时可用。           |          |
   | `query/success/count`     | 成功处理的查询数           | 此指标仅在包含 QueryCountStatsMonitor 模块时可用。           |          |
   | `query/failed/count`      | 失败的查询数               | 此指标仅在包含 QueryCountStatsMonitor 模块时可用。           |          |
   | `query/interrupted/count` | 由于取消而中断的查询数。   | 此指标仅在包含 QueryCountStatsMonitor 模块时可用。           |          |
   | `query/timeout/count`     | 超时查询的数量。           | 此指标仅在包含 QueryCountStatsMonitor 模块时可用。           |          |

   cache

   | 名称                  | 描述                       | 正常值 |        |
   | --------------------- | -------------------------- | ------ | ------ |
   | `query/cache/delta/*` | 自上次发射以来的缓存指标。 |        | 不适用 |
   | `query/cache/total/*` | 总缓存指标。               |        | 不适用 |

   | 名称              | 描述                                                         | 方面 | 正常值           |
   | ----------------- | ------------------------------------------------------------ | ---- | ---------------- |
   | `*/numEntries`    | 缓存条目数。                                                 |      | 变化。           |
   | `*/sizeBytes`     | 缓存条目的大小（以字节为单位）。                             |      | 变化。           |
   | `*/hits`          | 缓存命中数。                                                 |      | 变化。           |
   | `*/misses`        | 缓存未命中数。                                               |      | 变化。           |
   | `*/evictions`     | 缓存驱逐的数量。                                             |      | 变化。           |
   | `*/hitRate`       | 缓存命中率。                                                 |      | ~40%             |
   | `*/averageByte`   | 平均缓存条目字节大小。                                       |      | 变化。           |
   | `*/timeouts`      | 缓存超时数。                                                 |      | 0                |
   | `*/errors`        | 缓存错误数。                                                 |      | 0                |
   | `*/put/ok`        | 成功缓存的新缓存条目数。                                     |      | 变化，但大于零。 |
   | `*/put/error`     | 由于错误而无法缓存的新缓存条目数。                           |      | 变化，但大于零。 |
   | `*/put/oversized` | 由于太大而被跳过的潜在新缓存条目的数量（基于`druid.{broker,historical,realtime}.cache.maxEntrySize`属性）。 |      | 变化。           |

   Memcached 指标

   Memcached 客户端指标按以下方式报告。这些指标直接来自客户端，而不是来自缓存检索层。

   | 公制                          | 描述                                                         | 方面   | 正常值 |
   | ----------------------------- | ------------------------------------------------------------ | ------ | ------ |
   | `query/cache/memcached/total` | 缓存 memcached 独有的指标（仅当`druid.cache.type=memcached`）作为它们的实际值 | 多变的 | 不适用 |
   | `query/cache/memcached/delta` | 缓存 memcached 独有的指标（仅当`druid.cache.type=memcached`）作为它们与先前事件发射的增量 | 多变的 | 不适用 |

   SQL 指标

   如果启用了 SQL，Broker 将为 SQL 发出以下指标。

   | 公制             | 描述                        | 方面                                                  | 正常值 |
   | ---------------- | --------------------------- | ----------------------------------------------------- | ------ |
   | `sqlQuery/time`  | 完成一条 SQL 所需的毫秒数。 | id、nativeQueryIds、dataSource、remoteAddress、成功。 | < 1s   |
   | `sqlQuery/bytes` | SQL 响应中返回的字节数。    | id、nativeQueryIds、dataSource、remoteAddress、成功。 |        |

   虚拟机

   这些指标仅在包含 JVMMonitor 模块时可用。

   | 公制                      | 描述                                                         | 方面                                             | 正常值                                                       |
   | ------------------------- | ------------------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------------------ |
   | `jvm/pool/committed`      | Committed pool.                                              | 池种类，池名称。                                 | 接近最大池                                                   |
   | `jvm/pool/init`           | Initial pool.                                                | 池种类，池名称。                                 | 变化。                                                       |
   | `jvm/pool/max`            | Max pool.                                                    | 池种类，池名称。                                 | 变化。                                                       |
   | `jvm/pool/used`           | Pool used.                                                   | 池种类，池名称。                                 | <最大池                                                      |
   | `jvm/bufferpool/count`    | Pool used.                                                   | 缓冲池名称。                                     | 变化。                                                       |
   | `jvm/bufferpool/used`     | Bufferpool used.。                                           | 缓冲池名称。                                     | 接近容量                                                     |
   | `jvm/bufferpool/capacity` | 缓冲池容量。                                                 | 缓冲池名称。                                     | 变化。                                                       |
   | `jvm/mem/init`            | Initial memory.                                              | 内存种类。                                       | 变化。                                                       |
   | `jvm/mem/max`             | Max memory.                                                  | 内存种类。                                       | 变化。                                                       |
   | `jvm/mem/used`            | Used memory                                                  | 内存种类。                                       | <最大内存                                                    |
   | `jvm/mem/committed`       | Committed memory.                                            | 内存种类。                                       | 接近最大内存                                                 |
   | `jvm/gc/count`            | Garbage collection count.                                    | gcName (cms/g1/parallel/etc.), gcGen (old/young) | 变化。                                                       |
   | `jvm/gc/cpu`              | 用于垃圾收集的 CPU 时间计数（以纳秒为单位）。注：`jvm/gc/cpu`表示多个 GC 周期的总时间；除以`jvm/gc/count`得到每个周期的平均 GC 时间 | gcName, gcGen                                    | 总和`jvm/gc/cpu`应在总和的 10-30% 范围内`jvm/cpu/total`，具体取决于所使用的 GC 算法（由 报告[`JvmCpuMonitor`](https://druid.apache.org/docs/latest/configuration/index.html#enabling-metrics)） |

   Coordinator

   这些指标适用于 Druid Coordinator，每次 Coordinator 运行协调逻辑时都会重置。

   | 公制                              | 描述                                                         | 方面         | 正常值   |
   | --------------------------------- | ------------------------------------------------------------ | ------------ | -------- |
   | `segment/assigned/count`          | 分配要加载到集群中的段数。                                   | 层。         | 变化。   |
   | `segment/moved/count`             | 在集群中移动的段数。                                         | 层。         | 变化。   |
   | `segment/dropped/count`           | 由于被遮盖而丢弃的段数。                                     | 层。         | 变化。   |
   | `segment/deleted/count`           | 由于规则而丢弃的段数。                                       | 层。         | 变化。   |
   | `segment/unneeded/count`          | 由于被标记为未使用而丢弃的段数。                             | 层。         | 变化。   |
   | `segment/cost/raw`                | 用于成本平衡。托管细分市场的原始成本。                       | 层。         | 变化。   |
   | `segment/cost/normalization`      | 用于成本平衡。托管段的规范化。                               | 层。         | 变化。   |
   | `segment/cost/normalized`         | 用于成本平衡。托管段的标准化成本。                           | 层。         | 变化。   |
   | `segment/loadQueue/size`          | 要加载的段的大小（以字节为单位）。                           | 服务器。     | 变化。   |
   | `segment/loadQueue/failed`        | 未能加载的段数。                                             | 服务器。     | 0        |
   | `segment/loadQueue/count`         | 要加载的段数。                                               | 服务器。     | 变化。   |
   | `segment/dropQueue/count`         | 要删除的段数。                                               | 服务器。     | 变化。   |
   | `segment/size`                    | 数据源中已使用段的总大小。仅为至少一个已使用段所属的数据源发出。 | 数据源。     | 变化。   |
   | `segment/count`                   | 属于数据源的已用段数。仅为至少一个已使用段所属的数据源发出。 | 数据源。     | < 最大值 |
   | `segment/overShadowed/count`      | 被遮盖的段数。                                               |              | 变化。   |
   | `segment/unavailable/count`       | 在集群中应该加载的段可用于查询之前，要加载的段（不包括副本）的数量。 | 数据源。     | 0        |
   | `segment/underReplicated/count`   | 在集群中应该加载的段可用于查询之前要加载的段（包括副本）的数量。 | 层，数据源。 | 0        |
   | `tier/historical/count`           | 每层可用的历史节点数。                                       | 层。         | 变化。   |
   | `tier/replication/factor`         | 在每个层中配置了最大复制因子。                               | 层。         | 变化。   |
   | `tier/required/capacity`          | 每层所需的总容量（以字节为单位）。                           | 层。         | 变化。   |
   | `tier/total/capacity`             | 每层可用的总容量（以字节为单位）。                           | 层。         | 变化。   |
   | `compact/task/count`              | 自动压缩运行中发出的任务数。                                 |              | 变化。   |
   | `compactTask/maxSlot/count`       | 自动压缩运行中可用于自动压缩任务的最大任务槽数。             |              | 变化。   |
   | `compactTask/availableSlot/count` | 自动压缩运行中可用于自动压缩任务的可用任务槽数。（这是最大槽减去任何当前正在运行的压缩任务） |              | 变化。   |
   | `segment/waitCompact/bytes`       | 此数据源等待自动压缩的总字节数（仅考虑符合自动压缩条件的间隔/段）。 | 数据源。     | 变化。   |
   | `segment/waitCompact/count`       | 此数据源的等待被自动压缩压缩的段总数（仅考虑符合自动压缩条件的间隔/段）。 | 数据源。     | 变化。   |
   | `interval/waitCompact/count`      | 此数据源等待自动压缩的时间间隔总数（仅考虑符合自动压缩条件的时间间隔/段）。 | 数据源。     | 变化。   |
   | `segment/compacted/bytes`         | 此数据源中已使用自动压缩配置中设置的规范压缩的总字节数。     | 数据源。     | 变化。   |
   | `segment/compacted/count`         | 此数据源的已使用自动压缩配置中设置的规范压缩的段总数。       | 数据源。     | 变化。   |
   | `interval/compacted/count`        | 此数据源的已使用自动压缩配置中设置的规范压缩的间隔总数。     | 数据源。     | 变化。   |
   | `segment/skipCompact/bytes`       | 自动压缩跳过（不符合自动压缩条件）的此数据源的总字节数。     | 数据源。     | 变化。   |
   | `segment/skipCompact/count`       | 自动压缩跳过（不符合自动压缩条件）的此数据源的段总数。       | 数据源。     | 变化。   |
   | `interval/skipCompact/count`      | 自动压缩跳过（不符合自动压缩条件）的此数据源的间隔总数。     | 数据源。     | 变化。   |
   | `coordinator/time`                | 以毫秒为单位的近似协调器职责运行时间。duty 维度是正在运行的 Duty 的字符串别名。 | 义务。       | 变化。   |
   | `coordinator/global/time`         | 整个协调周期的近似运行时间（以毫秒为单位）。该`dutyGroup`维度表示此运行的协调类型。即历史管理与索引 | `dutyGroup`  | 变化。   |
   | `metadata/kill/supervisor/count`  | 每次 Coordinator kill supervisor duty 运行时，从元数据存储中自动删除的已终止主管总数。`druid.coordinator.kill.supervisor.durationToRetain`该指标可以根据每个周期是否需要删除更多或更少的已终止主管来帮助调整配置。请注意，仅当`druid.coordinator.kill.supervisor.on`设置为 true 时才会发出此指标。 |              | 变化。   |
   | `metadata/kill/audit/count`       | 每次 Coordinator kill 审计任务运行时自动从元数据存储中删除的审计日志总数。`druid.coordinator.kill.audit.durationToRetain`该指标可以根据每个周期是否需要删除更多或更少的审计日志来帮助调整配置。请注意，仅当`druid.coordinator.kill.audit.on`设置为 true 时才会发出此指标。 |              | 变化。   |
   | `metadata/kill/compaction/count`  | 每次协调器终止压缩配置任务运行时，从元数据存储中自动删除的压缩配置总数。请注意，仅当`druid.coordinator.kill.compaction.on`设置为 true 时才会发出此指标。 |              | 变化。   |
   | `metadata/kill/rule/count`        | 每个协调器终止规则任务运行时从元数据存储中自动删除的规则总数。`druid.coordinator.kill.rule.durationToRetain`该指标可以根据每个周期是否需要删除更多或更少的规则来帮助调整配置。请注意，仅当`druid.coordinator.kill.rule.on`设置为 true 时才会发出此指标。 |              | 变化。   |
   | `metadata/kill/datasource/count`  | 每个 Coordinator kill datasource duty run 从元数据存储中自动删除的数据源元数据总数（注意：数据源元数据仅存在于从主管创建的数据源）。`druid.coordinator.kill.datasource.durationToRetain`该指标可以根据每个周期是否需要删除更多或更少的数据源元数据来帮助调整配置。请注意，仅当`druid.coordinator.kill.datasource.on`设置为 true 时才会发出此指标。 |              | 变化。   |

   如果在 Coordinator[动态配置](https://druid.apache.org/docs/latest/configuration/index.html#dynamic-configuration)`emitBalancingStats`中设置为，则类 的[日志条目](https://druid.apache.org/docs/latest/configuration/logging.html)将包含有关平衡决策的额外信息。`true``org.apache.druid.server.coordinator.duty.EmitClusterStatsAndMetrics`

5. 举个栗子

   ```sql
   select * from "aiolos_img_details" 
   where __time BETWEEN '2022-02-01' AND '2022-02-15'
   
   ##原生查询
   {
     "queryType": "scan",
     "dataSource": {
       "type": "table",
       "name": "aiolos_img_details"
     },
     "intervals": {
       "type": "intervals",
       "intervals": [
         "2022-02-01T00:00:00.000Z/2022-02-15T00:00:00.001Z"
       ]
     },
     "virtualColumns": [],
     "resultFormat": "compactedList",
     "batchSize": 20480,
     "limit": 101,
     "order": "none",
     "filter": null,
     "columns": [
       "__time",
       "action_type",
       "app_name",
       "app_version",
       "canvas_id",
       "country",
       "duration",
       "img_id",
       "img_living_days",
       "img_name",
       "img_piece",
       "img_ratio",
       "is_local",
       "is_rotated",
       "location",
       "muid",
       "platform",
       "schedule_date",
       "topic_id",
       "topic_img_num",
       "topic_name",
       "topic_price",
       "user_segment"
     ],
     "legacy": false,
     "context": {
       "sqlOuterLimit": 101,
       "sqlQueryId": "5c18179e-eade-4b18-aa75-155f2a800cc0"
     },
     "descending": false,
     "granularity": {
       "type": "all"
     }
   }
   
   ## QueryID
   007a4ed9-ad65-4993-978d-88b745388307
   ```

   这个SQL应该命中下面三个`Segment`

   ![image-20220222145359800](https://tva1.sinaimg.cn/large/e6c9d24ely1gzmam6ucmyj21u8088wh5.jpg)

   broker

   | 名称             | 描述                                                         | 结果                                             |
   | ---------------- | ------------------------------------------------------------ | ------------------------------------------------ |
   | query/time       | 完成查询所需的毫秒数。                                       | 17                                               |
   | `sqlQuery/bytes` | 查询响应中返回的字节数                                       | 5221                                             |
   | query/node/time  | 查询单个历史/实时进程所需的毫秒数。                          | 13                                               |
   | query/node/bytes | 查询单个历史/实时进程返回的字节数。                          | 4289                                             |
   | query/node/ttfb  | 第一个字节的时间。在 Broker 开始接收来自各个历史/实时进程的响应之前经过了毫秒。 | 10                                               |
   | query/count      | 总查询数                                                     | 此指标仅在包含 QueryCountStatsMonitor 模块时可用 |
   | sqlQuery/time    | 完成 SQL 查询所需的毫秒数                                    | 59                                               |

   <img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzm9nan8d1j20nu0so0wb.jpg" alt="image-20220222142024432" style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzm9nu73roj20qg0w2ado.jpg" alt="image-20220222142059207 " style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzm9okcqv0j20oa0u2tcb.jpg" alt="image-20220222142140965 " style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzm9pzv16bj20pu0mg76l.jpg" alt="image-20220222142303538 " style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzm9sr5y0xj20q20fswfy.jpg" alt="image-20220222142542539 " style="zoom:50%;" />

Historical

| 名称                       | 描述                                                     | 结果            |
| -------------------------- | -------------------------------------------------------- | --------------- |
| query/time                 | 完成查询所需的毫秒数                                     | 6               |
| query/segment/time         | 查询单个段所用的毫秒数。包括从磁盘分页的时间             | 3个segment均为0 |
| query/wait/time            | 等待扫描段所花费的毫秒数                                 | 3个segment均为0 |
| segment/scan/pending       | 队列中等待扫描的段数。                                   | 无              |
| query/segmentAndCache/time | 查询单个段或命中缓存所需的毫秒数（如果在历史进程中启用） | 1，0，0         |
| query/count                | 总查询数                                                 | 无              |
| sqlQuery/time              | 完成 SQL 查询所需的毫秒数。                              | 无              |

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzma450jyuj211t0u0n1c.jpg" alt="image-20220222143639222" style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzma4qvkjpj213m0ti78e.jpg" alt="image-20220222143714230" style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzma65jisij212v0u078j.jpg" alt="image-20220222143835318" style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzma6sgxe3j212u0tawil.jpg" alt="image-20220222143911827" style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzma7b7w11j212t0u0wiq.jpg" alt="image-20220222143941771" style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzma7v80sej212m0tgn1g.jpg" alt="image-20220222144013976" style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzma8dxlm5j212y0t0jvk.jpg" alt="image-20220222144044015" style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzma8y6vg3j212m0tcdjx.jpg" alt="image-20220222144116432" style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzma9h08wyj212o0sutcv.jpg" alt="image-20220222144146507" style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzmaao34v5j20u00uowi2.jpg" alt="image-20220222144255157" style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzmab6a3l4j20u00ugq6n.jpg" alt="image-20220222144324816" style="zoom:50%;" />

<img src="https://tva1.sinaimg.cn/large/e6c9d24ely1gzmablmyjaj20v10u0ads.jpg" alt="image-20220222144349295" style="zoom:50%;" />

