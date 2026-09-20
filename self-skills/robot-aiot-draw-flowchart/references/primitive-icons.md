# Icons (primitive)

A monochrome 24×24 icon library for IT/cloud diagrams. Each icon uses `currentColor` so it inherits ink from its parent SVG and adapts to the editorial skin or any user-onboarded brand palette.

## Usage

Find the icon by name in the index below or in `assets/icons/manifest.json` (fields: name, file, category, viewBox, keywords, description, source). Copy the contents of `assets/icons/<name>.svg` into your diagram. Default size is 24×24; wrap in `<g transform="translate(x,y) scale(s)">` to position and resize. Set `color`, `fill`, or `stroke` on the parent group/SVG to control color.

Generic icons are stroked (1.5px, hairline, like the rest of the skill); brand silhouettes are filled. Don't mix the two styles in the same diagram unnecessarily.

## Index

Machine-readable manifest: `assets/icons/manifest.json`; SVG sources: `assets/icons/<name>.svg`. 87 icons, 12 categories.

### Compute

| name | description | source |
|---|---|---|
| `laptop` | User laptop or workstation. | Tabler Icons / `device-laptop` (MIT) |
| `phone` | Mobile phone or tablet client. | Tabler Icons / `device-mobile` (MIT) |
| `desktop` | Desktop computer. | Tabler Icons / `device-desktop` (MIT) |
| `server` | Physical server or VM host. | Tabler Icons / `server` (MIT) |
| `container` | Container image or running instance. | Tabler Icons / `package` (MIT) |
| `vm` | Virtual machine. | Tabler Icons / `cube` (MIT) |


### People

| name | description | source |
|---|---|---|
| `user` | End user or single actor. | Tabler Icons / `user` (MIT) |
| `users` | Group / cohort / team. | Tabler Icons / `users` (MIT) |
| `admin` | Privileged user / admin. | Tabler Icons / `user-shield` (MIT) |
| `robot` | Bot, agent, or automated process. | Tabler Icons / `robot` (MIT) |


### Network

| name | description | source |
|---|---|---|
| `cloud` | Cloud provider or boundary. | Tabler Icons / `cloud` (MIT) |
| `internet` | Public internet. | Tabler Icons / `world` (MIT) |
| `cdn` | CDN or edge cache. | Tabler Icons / `world-www` (MIT) |
| `firewall` | Firewall or perimeter control. | Tabler Icons / `wall` (MIT) |
| `vpn` | VPN or encrypted tunnel. | Tabler Icons / `shield-lock` (MIT) |
| `load-balancer` | Load balancer / traffic split. | Tabler Icons / `arrows-split` (MIT) |
| `gateway` | API gateway or ingress door. | Tabler Icons / `door-enter` (MIT) |
| `dns` | DNS / name resolution. | Tabler Icons / `tag` (MIT) |


### Data

| name | description | source |
|---|---|---|
| `database` | Relational or document database. | Tabler Icons / `database` (MIT) |
| `file` | Generic file. | Tabler Icons / `file` (MIT) |
| `log` | Log file / event stream. | Tabler Icons / `file-text` (MIT) |
| `queue` | Message queue / FIFO. | Tabler Icons / `stack-2` (MIT) |
| `cache` | Cache layer. | Tabler Icons / `bolt` (MIT) |
| `bucket` | Object storage / S3 bucket. | Tabler Icons / `bucket` (MIT) |
| `backup` | Backup or snapshot. | Tabler Icons / `device-floppy` (MIT) |
| `search` | Search index / query. | Tabler Icons / `search` (MIT) |


### Kubernetes

| name | description | source |
|---|---|---|
| `pod` | Pod (smallest deployable unit). | Tabler Icons / `hexagon` (MIT) |
| `node` | Cluster node. | Tabler Icons / `topology-star` (MIT) |
| `service` | K8s service / virtual endpoint. | Tabler Icons / `world-cog` (MIT) |
| `deployment` | Deployment rollout. | Tabler Icons / `rocket` (MIT) |
| `ingress` | Ingress controller / route in. | Tabler Icons / `arrow-right-rhombus` (MIT) |
| `volume` | Persistent volume. | Tabler Icons / `device-sd-card` (MIT) |


### Action

| name | description | source |
|---|---|---|
| `api` | API surface / endpoint. | Tabler Icons / `braces` (MIT) |
| `request` | Outbound request. | Tabler Icons / `arrow-right` (MIT) |
| `response` | Inbound response. | Tabler Icons / `arrow-left` (MIT) |
| `sync` | Sync / reconcile loop. | Tabler Icons / `refresh` (MIT) |
| `lock` | Locked / authenticated. | Tabler Icons / `lock` (MIT) |
| `key` | Key / secret. | Tabler Icons / `key` (MIT) |
| `alert` | Warning / paged alert. | Tabler Icons / `alert-triangle` (MIT) |


### DevOps

| name | description | source |
|---|---|---|
| `git-branch` | Branch / fork point. | Tabler Icons / `git-branch` (MIT) |
| `terminal` | Shell / CLI. | Tabler Icons / `terminal` (MIT) |
| `pipeline` | CI/CD pipeline. | Tabler Icons / `git-merge` (MIT) |
| `bug` | Bug / defect. | Tabler Icons / `bug` (MIT) |
| `monitoring` | Metrics / observability. | Tabler Icons / `chart-line` (MIT) |
| `test` | Test / experiment. | Tabler Icons / `test-pipe` (MIT) |


### Brand

| name | description | source |
|---|---|---|
| `docker` | Docker engine / image. | Tabler Icons / `brand-docker` (MIT) |
| `terraform` | Terraform IaC. | Tabler Icons / `brand-terraform` (MIT) |
| `aws` | Amazon Web Services. | Tabler Icons / `brand-aws` (MIT) |
| `azure` | Microsoft Azure. | Tabler Icons / `brand-azure` (MIT) |
| `github` | GitHub. | Tabler Icons / `brand-github` (MIT) |
| `kubernetes` | Kubernetes. | Simple Icons / `kubernetes` (CC0) |
| `gcp` | Google Cloud. | Simple Icons / `googlecloud` (CC0) |
| `postgres` | PostgreSQL. | Simple Icons / `postgresql` (CC0) |
| `redis` | Redis. | log-z/logos / `redis` (MIT) |
| `nginx` | Nginx. | Simple Icons / `nginx` (CC0) |
| `gitea` | Gitea self-hosted git. | Simple Icons / `gitea` (CC0) |
| `keycloak` | Keycloak identity / SSO. | Simple Icons / `keycloak` (CC0) |
| `active-directory` | Active Directory / LDAP identity directory. | Tabler Icons / `address-book` (MIT) |
| `minio` | MinIO S3-compatible object storage. | Simple Icons / `minio` (CC0) |
| `mysql` | MySQL. | log-z/logos / `mysql` (MIT) |
| `oracle` | Oracle Database. | Simple Icons / `oracle` (CC0) |
| `sqlserver` | Microsoft SQL Server. | Simple Icons / `microsoftsqlserver` (CC0) |
| `sqlite` | SQLite embedded database. | Simple Icons / `sqlite` (CC0) |
| `hive` | Apache Hive data warehouse. | Simple Icons / `apachehive` (CC0) |
| `starrocks` | StarRocks MPP analytical DB. | log-z/logos / `starrocks` (MIT) |


### Data stack

| name | description | source |
|---|---|---|
| `nifi` | Apache NiFi data flow. | Simple Icons / `apachenifi` (CC0) |
| `airflow` | Apache Airflow scheduler / DAG runner. | Simple Icons / `apacheairflow` (CC0) |
| `hop` | Apache Hop data orchestration / ETL. | Direct fetch / `hop.apache.org` — verify license before use |
| `pentaho` | Pentaho PDI (Kettle) ETL & data integration. | Direct fetch / `cdn.worldvectorlogo.com` — verify license before use |
| `dagster` | Dagster data orchestration platform. | Direct fetch / `cdn.prod.website-files.com` — verify license before use |
| `trino` | Trino distributed SQL query engine. | Simple Icons / `trino` (CC0) |
| `superset` | Apache Superset BI / dashboards. | Simple Icons / `apachesuperset` (CC0) |
| `redash` | Redash open-source BI & dashboards. | Simple Icons / `redash` (CC0) |
| `tableau` | Tableau data visualization. | Simple Icons / `tableau` (CC0) |
| `powerbi` | Microsoft Power BI. | Simple Icons / `powerbi` (CC0) |
| `jupyter` | Jupyter / JupyterLab notebooks. | Simple Icons / `jupyter` (CC0) |


### Language

| name | description | source |
|---|---|---|
| `python` | Python. | Simple Icons / `python` (CC0) |
| `r` | R statistical language. | Simple Icons / `r` (CC0) |
| `sql` | SQL / generic relational query. | Tabler Icons / `sql` (MIT) |


### Statistical tools

| name | description | source |
|---|---|---|
| `spss` | IBM SPSS Statistics. | Devicon / `spss-plain` (MIT) |
| `sas` | SAS analytics platform. | Direct fetch / `upload.wikimedia.org` — verify license before use |
| `stata` | Stata statistical software. | Direct fetch / `icon.icepanel.io` — verify license before use |
| `rstudio` | RStudio / Posit IDE for R and Python. | Devicon / `rstudio-plain` (MIT) |
| `qgis` | QGIS open-source GIS platform. | Simple Icons / `qgis` (CC0) |


### File formats

| name | description | source |
|---|---|---|
| `excel` | Microsoft Excel spreadsheet. | Tabler Icons / `file-type-xls` (MIT) |
| `csv` | Comma-separated values file. | Tabler Icons / `file-type-csv` (MIT) |
| `txt` | Plain text file. | Tabler Icons / `file-type-txt` (MIT) |

---

## License attribution

- **Tabler Icons** — MIT — https://github.com/tabler/tabler-icons
- **Simple Icons** — CC0 — https://github.com/simple-icons/simple-icons
- **Devicon** — MIT — https://github.com/devicons/devicon
- **log-z/logos** — MIT — https://github.com/log-z/logos

All libraries' licenses permit redistribution, including in this repository's MIT-licensed source. Brand logos retain their respective trademarks; this set is for documentation and illustrative use only.
