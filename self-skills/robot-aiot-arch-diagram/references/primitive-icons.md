# Icons（基元）

面向 IT/云图表的单色 24×24 图标库。每个图标使用 `currentColor`，从父级 SVG 继承墨色，自动适配编辑风皮肤或任何用户 onboarding 的品牌调色板。

## 用法

在下方索引或 `assets/icons/manifest.json`（字段：name、file、category、viewBox、keywords、description、source）中按名称找到图标。把 `assets/icons/<name>.svg` 的内容复制进图表。默认尺寸 24×24；用 `<g transform="translate(x,y) scale(s)">` 包裹来定位和缩放。在父级分组/SVG 上设置 `color`、`fill` 或 `stroke` 控制颜色。

通用图标是描边风格（1.5px 细线，与 skill 其余部分一致）；品牌轮廓是填充风格。同一张图中不要无必要地混用两种风格。

## 索引

机器可读 manifest：`assets/icons/manifest.json`；SVG 源：`assets/icons/<name>.svg`。87 个图标，12 个分类。

### Compute（计算）

| name | description | source |
|---|---|---|
| `laptop` | 用户笔记本或工作站。 | Tabler Icons / `device-laptop` (MIT) |
| `phone` | 手机或平板客户端。 | Tabler Icons / `device-mobile` (MIT) |
| `desktop` | 台式电脑。 | Tabler Icons / `device-desktop` (MIT) |
| `server` | 物理服务器或 VM 宿主机。 | Tabler Icons / `server` (MIT) |
| `container` | 容器镜像或运行实例。 | Tabler Icons / `package` (MIT) |
| `vm` | 虚拟机。 | Tabler Icons / `cube` (MIT) |


### People（人员）

| name | description | source |
|---|---|---|
| `user` | 最终用户或单个参与者。 | Tabler Icons / `user` (MIT) |
| `users` | 群组/用户群/团队。 | Tabler Icons / `users` (MIT) |
| `admin` | 特权用户/管理员。 | Tabler Icons / `user-shield` (MIT) |
| `robot` | 机器人、agent 或自动化流程。 | Tabler Icons / `robot` (MIT) |


### Network（网络）

| name | description | source |
|---|---|---|
| `cloud` | 云厂商或云边界。 | Tabler Icons / `cloud` (MIT) |
| `internet` | 公共互联网。 | Tabler Icons / `world` (MIT) |
| `cdn` | CDN 或边缘缓存。 | Tabler Icons / `world-www` (MIT) |
| `firewall` | 防火墙或边界管控。 | Tabler Icons / `wall` (MIT) |
| `vpn` | VPN 或加密隧道。 | Tabler Icons / `shield-lock` (MIT) |
| `load-balancer` | 负载均衡/流量分发。 | Tabler Icons / `arrows-split` (MIT) |
| `gateway` | API 网关或入口。 | Tabler Icons / `door-enter` (MIT) |
| `dns` | DNS/域名解析。 | Tabler Icons / `tag` (MIT) |


### Data（数据）

| name | description | source |
|---|---|---|
| `database` | 关系型或文档数据库。 | Tabler Icons / `database` (MIT) |
| `file` | 通用文件。 | Tabler Icons / `file` (MIT) |
| `log` | 日志文件/事件流。 | Tabler Icons / `file-text` (MIT) |
| `queue` | 消息队列/FIFO。 | Tabler Icons / `stack-2` (MIT) |
| `cache` | 缓存层。 | Tabler Icons / `bolt` (MIT) |
| `bucket` | 对象存储/S3 bucket。 | Tabler Icons / `bucket` (MIT) |
| `backup` | 备份或快照。 | Tabler Icons / `device-floppy` (MIT) |
| `search` | 搜索索引/查询。 | Tabler Icons / `search` (MIT) |


### Kubernetes

| name | description | source |
|---|---|---|
| `pod` | Pod（最小可部署单元）。 | Tabler Icons / `hexagon` (MIT) |
| `node` | 集群节点。 | Tabler Icons / `topology-star` (MIT) |
| `service` | K8s service/虚拟端点。 | Tabler Icons / `world-cog` (MIT) |
| `deployment` | Deployment 发布。 | Tabler Icons / `rocket` (MIT) |
| `ingress` | Ingress 控制器/入站路由。 | Tabler Icons / `arrow-right-rhombus` (MIT) |
| `volume` | 持久卷。 | Tabler Icons / `device-sd-card` (MIT) |


### Action（动作）

| name | description | source |
|---|---|---|
| `api` | API 面/端点。 | Tabler Icons / `braces` (MIT) |
| `request` | 出站请求。 | Tabler Icons / `arrow-right` (MIT) |
| `response` | 入站响应。 | Tabler Icons / `arrow-left` (MIT) |
| `sync` | 同步/调谐循环。 | Tabler Icons / `refresh` (MIT) |
| `lock` | 已锁定/已认证。 | Tabler Icons / `lock` (MIT) |
| `key` | 密钥/secret。 | Tabler Icons / `key` (MIT) |
| `alert` | 告警/寻呼。 | Tabler Icons / `alert-triangle` (MIT) |


### DevOps

| name | description | source |
|---|---|---|
| `git-branch` | 分支/分叉点。 | Tabler Icons / `git-branch` (MIT) |
| `terminal` | Shell/CLI。 | Tabler Icons / `terminal` (MIT) |
| `pipeline` | CI/CD 流水线。 | Tabler Icons / `git-merge` (MIT) |
| `bug` | 缺陷。 | Tabler Icons / `bug` (MIT) |
| `monitoring` | 指标/可观测性。 | Tabler Icons / `chart-line` (MIT) |
| `test` | 测试/实验。 | Tabler Icons / `test-pipe` (MIT) |


### Brand（品牌）

| name | description | source |
|---|---|---|
| `docker` | Docker 引擎/镜像。 | Tabler Icons / `brand-docker` (MIT) |
| `terraform` | Terraform IaC。 | Tabler Icons / `brand-terraform` (MIT) |
| `aws` | Amazon Web Services。 | Tabler Icons / `brand-aws` (MIT) |
| `azure` | Microsoft Azure。 | Tabler Icons / `brand-azure` (MIT) |
| `github` | GitHub。 | Tabler Icons / `brand-github` (MIT) |
| `kubernetes` | Kubernetes。 | Simple Icons / `kubernetes` (CC0) |
| `gcp` | Google Cloud。 | Simple Icons / `googlecloud` (CC0) |
| `postgres` | PostgreSQL。 | Simple Icons / `postgresql` (CC0) |
| `redis` | Redis。 | log-z/logos / `redis` (MIT) |
| `nginx` | Nginx。 | Simple Icons / `nginx` (CC0) |
| `gitea` | Gitea 自托管 git。 | Simple Icons / `gitea` (CC0) |
| `keycloak` | Keycloak 身份/SSO。 | Simple Icons / `keycloak` (CC0) |
| `active-directory` | Active Directory/LDAP 身份目录。 | Tabler Icons / `address-book` (MIT) |
| `minio` | MinIO S3 兼容对象存储。 | Simple Icons / `minio` (CC0) |
| `mysql` | MySQL。 | log-z/logos / `mysql` (MIT) |
| `oracle` | Oracle Database。 | Simple Icons / `oracle` (CC0) |
| `sqlserver` | Microsoft SQL Server。 | Simple Icons / `microsoftsqlserver` (CC0) |
| `sqlite` | SQLite 嵌入式数据库。 | Simple Icons / `sqlite` (CC0) |
| `hive` | Apache Hive 数据仓库。 | Simple Icons / `apachehive` (CC0) |
| `starrocks` | StarRocks MPP 分析型数据库。 | log-z/logos / `starrocks` (MIT) |


### Data stack（数据栈）

| name | description | source |
|---|---|---|
| `nifi` | Apache NiFi 数据流。 | Simple Icons / `apachenifi` (CC0) |
| `airflow` | Apache Airflow 调度器/DAG 执行器。 | Simple Icons / `apacheairflow` (CC0) |
| `hop` | Apache Hop 数据编排/ETL。 | Direct fetch / `hop.apache.org` — 使用前核实许可 |
| `pentaho` | Pentaho PDI (Kettle) ETL 与数据集成。 | Direct fetch / `cdn.worldvectorlogo.com` — 使用前核实许可 |
| `dagster` | Dagster 数据编排平台。 | Direct fetch / `cdn.prod.website-files.com` — 使用前核实许可 |
| `trino` | Trino 分布式 SQL 查询引擎。 | Simple Icons / `trino` (CC0) |
| `superset` | Apache Superset BI/仪表盘。 | Simple Icons / `apachesuperset` (CC0) |
| `redash` | Redash 开源 BI 与仪表盘。 | Simple Icons / `redash` (CC0) |
| `tableau` | Tableau 数据可视化。 | Simple Icons / `tableau` (CC0) |
| `powerbi` | Microsoft Power BI。 | Simple Icons / `powerbi` (CC0) |
| `jupyter` | Jupyter/JupyterLab notebooks。 | Simple Icons / `jupyter` (CC0) |


### Language（语言）

| name | description | source |
|---|---|---|
| `python` | Python。 | Simple Icons / `python` (CC0) |
| `r` | R 统计语言。 | Simple Icons / `r` (CC0) |
| `sql` | SQL/通用关系查询。 | Tabler Icons / `sql` (MIT) |


### Statistical tools（统计工具）

| name | description | source |
|---|---|---|
| `spss` | IBM SPSS Statistics。 | Devicon / `spss-plain` (MIT) |
| `sas` | SAS 分析平台。 | Direct fetch / `upload.wikimedia.org` — 使用前核实许可 |
| `stata` | Stata 统计软件。 | Direct fetch / `icon.icepanel.io` — 使用前核实许可 |
| `rstudio` | RStudio/Posit IDE（R 与 Python）。 | Devicon / `rstudio-plain` (MIT) |
| `qgis` | QGIS 开源 GIS 平台。 | Simple Icons / `qgis` (CC0) |


### File formats（文件格式）

| name | description | source |
|---|---|---|
| `excel` | Microsoft Excel 电子表格。 | Tabler Icons / `file-type-xls` (MIT) |
| `csv` | 逗号分隔值文件。 | Tabler Icons / `file-type-csv` (MIT) |
| `txt` | 纯文本文件。 | Tabler Icons / `file-type-txt` (MIT) |

---

## 许可署名

- **Tabler Icons** — MIT — https://github.com/tabler/tabler-icons
- **Simple Icons** — CC0 — https://github.com/simple-icons/simple-icons
- **Devicon** — MIT — https://github.com/devicons/devicon
- **log-z/logos** — MIT — https://github.com/log-z/logos

以上库的许可均允许再分发（含本仓库 MIT 许可源码中的再分发）。品牌 logo 保留各自商标权；本图标集仅用于文档与示意用途。
