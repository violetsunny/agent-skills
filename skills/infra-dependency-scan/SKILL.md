---
name: infra-dependency-scan
description: Scan a Java/Spring Boot project for all external services, middleware, and third-party dependencies.
version: 2.0.0
author: workspace-cli-agent
---

# Infrastructure Dependency Scan

Systematically scan a Java/Spring Boot project to produce a complete inventory of external services, middleware, and third-party dependencies.

## When to Use
- User asks to "find all external dependencies", "scan middleware", "inventory services", "列出依赖", "列出中间件"
- Onboarding to a new project and need infrastructure map
- Pre-migration analysis (e.g., cloud migration, version upgrade)
- Security audit preparation

## Scan Procedure

**Key principle**: Read all config files and pom.xml FIRST, then grep code to confirm usage. This gives the high-level picture before diving in.

### Step 1: Config Files + pom.xml (parallel)

Read in one batch:
1. `glob(**/application*.yml)` and `glob(**/bootstrap*.yml)` — find all Spring config profiles
2. `read(pom.xml)` — identify all Maven dependencies
3. `glob(**/application*.properties)` and `glob(**/bootstrap*.properties)` — some projects use .properties

From configs, extract:
| Config Key Prefix | What It Reveals |
|---|---|
| `spring.datasource.*` | Database + pool type (check `.type` for Druid/HikariCP) |
| `spring.kafka.*` | Kafka brokers, topics, consumer groups |
| `spring.redis.*` / `spring.data.redis.*` | Redis |
| `spring.rabbitmq.*` | RabbitMQ |
| `spring.elasticsearch.*` | Elasticsearch |
| `spring.mongodb.*` | MongoDB |
| `spring.cloud.*` | Nacos, Consul, Eureka, Config Center |
| `minio.*` / `oss.*` / `s3.*` / `aws.*` / `obs.*` | Object storage |
| `spring.mail.*` | SMTP |
| `clickhouse.*` | ClickHouse (NOT under spring.datasource) |
| `mqtt.*` / `spring.mqtt.*` / `mz.mqtt.*` | MQTT broker |
| `config.sts.*` | Cloud STS token service (AWS/Alibaba OSS temp credentials) |
| `config.iam.*` | Cloud IAM auth (Huawei OBS, SberCloud) |
| `langchain4j.*` | LangChain4j AI framework (chat-model, embedding-model, base-url, api-key, model-name) |
| `milvus.*` | Milvus vector database (host, port, collection, index-type, metric-type) |
| `rag.*` | RAG pipeline config (splitting, retrieval, rerank, embedding, cache, hyde, query-expansion) |
| `bge.*` | BGE reranker service (local/remote embedding reranker API) |
| `tavily.*` | Tavily web search API (for RAG augmentation) |
| `spring.ai.*` | Spring AI framework (model configs, vector store settings) |
| Custom URL/host properties | External HTTP services |

From pom.xml, extract:
- Middleware client artifacts (spring-kafka, spring-boot-starter-data-redis, redisson, minio, aliyun-sdk-oss, aws-java-sdk-s3, etc.)
- HTTP client libraries (okhttp, httpclient, spring-cloud-starter-openfeign)
- Third-party SDKs (tencentcloud-sdk-java, aliyun-java-sdk-*, push-server, firebase-admin)
- AI/LLM framework artifacts (langchain4j, langchain4j-open-ai, langchain4j-milvus, langchain4j-elasticsearch, langchain4j-embeddings-*, spring-ai-starter-model-openai, spring-ai-starter-vector-store-*, spring-ai-advisors-*, spring-ai-*-document-reader)
- Vector DB client artifacts (milvus-sdk-java, langchain4j-milvus, langchain4j-chroma, langchain4j-pinecone, spring-ai-milvus-store)
- Build context: Spring Boot version, Java version

### Step 2: Code-Level Grep (parallel batch)

Run all greps in ONE parallel batch. Search in `src/main/java/`:

| What to Find | Grep Pattern |
|---|---|
| Feign clients | `@FeignClient` |
| RestTemplate usage | `RestTemplate` |
| Other HTTP clients | `OkHttpClient\|WebClient\|HttpUtils\|HttpUtil\|HttpClient\|@ForestClient\|openConnection` |
| Kafka consumers/producers | `@KafkaListener\|KafkaTemplate\|KafkaPrimary\|KafkaSecondary` |
| Redis usage | `RedisTemplate\|StringRedisTemplate\|@Cacheable\|Redisson` |
| RabbitMQ usage | `@RabbitListener\|RabbitTemplate\|AmqpTemplate\|StreamBridge` |
| Elasticsearch | `ElasticsearchRestTemplate\|@Document` |
| MongoDB | `MongoTemplate` |
| Object storage clients | `AmazonS3\|S3Client\|MinioClient\|OSSClient\|ObsClient` |
| Push services | `HmsInstanceId\|PushManager\|ApnsClient\|FirebaseMessaging` |
| Email services | `SesClient\|JavaMailSender\|MimeMessage` |
| In-memory cache | `Caffeine\|LoadingCache\|CacheBuilder` |
| TTS/语音 | `PollyClient\|SpeechSynthesizer\|TextToSpeech\|DifyClient` |
| OAuth providers | `AppleIdClient\|GoogleIdClient\|FacebookClient` |
| MQTT client | `MqttClient\|@MqttMessage` |
| Hardcoded URLs | `http://\|https://` in .java files |
| @Value URL/host injection | `@Value.*url\|@Value.*host\|@Value.*uri\|@Value.*endpoint` |
| LangChain4j usage | `dev.langchain4j\|@AiService\|AiServices.builder\|EmbeddingStore\|ContentRetriever\|QueryTransformer\|RetrievalAugmentor\|ChatMemoryProvider` |
| Spring AI usage | `org.springframework.ai\|@AiClient\|ChatModel\|EmbeddingModel\|VectorStore` |
| Vector DB clients | `MilvusEmbeddingStore\|ChromaEmbeddingStore\|PineconeEmbeddingStore\|MilvusClient\|PineconeClient` |
| Reranker services | `ScoringModel\|RerankModel\|BgeScoringModel\|CohereRerank` |
| AI conditional beans | `@ConditionalOnProperty.*rag\.\|@ConditionalOnProperty.*langchain4j\|@ConditionalOnProperty.*milvus\|@ConditionalOnProperty.*embedding` |

### Step 3: Cross-Reference & Validate

- pom.xml has `spring-kafka` but no `@KafkaListener`? May be unused or configured elsewhere
- pom.xml has `spring-cloud-starter-openfeign` but no `@FeignClient`? Check for `@ForestClient`
- `MqttMessageEntity` bean without MQTT client in pom.xml? It's just a DTO, not actual MQTT usage
- Check MEMORY.md or AGENTS.md for known project context

### Step 4: Check for Multi-Profile / Multi-Region Patterns

- Read ALL profile configs (sit/prod per region), not just default
- Look for `@Value("#{${...}}")` Map injection — region-based URI routing
- Check for custom `@Configuration` classes that define separate beans for different clusters (KafkaPrimaryConfig, KafkaSecondaryConfig, etc.)
- K8s YAMLs at project root (`sit_*.yml`, `prod_*.yml`) may contain env vars revealing infrastructure

### Step 5: Produce Output

**Always persist the report to a file** — the user expects a deliverable, not just inline display. Default path: `doc/infrastructure-dependencies.md` or as the user specifies.

Also save to `references/<project-name>-scan.md` under the skill directory for future reference.

## Output Format

```markdown
## 基础设施依赖清单: [Project Name]

> 扫描日期: YYYY-MM-DD | 项目路径: [path]

### 中间件 (Middleware)

| 名称 | 类型 | 配置 Key | 用途 |
|------|------|----------|------|
| MySQL | 数据库 | spring.datasource.url | 主数据存储 |
| Redis | 缓存 | spring.redis.host | 缓存/分布式锁 |
| Kafka | 消息队列 | spring.kafka.bootstrap-servers | 异步消息 |

### 外部 HTTP 服务 (External HTTP Services)

| 服务名 | 用途 | 配置 Key / URL | 调用方式 |
|--------|------|----------------|----------|

### 对象存储 (Object Storage)

| 类型 | 配置 Key | Bucket | 用途 |
|------|----------|--------|------|

### 其他第三方服务 (Other Third-Party Services)

| 服务 | 用途 | 依赖/配置 |
|------|------|-----------|

### AI/LLM 基础设施 (AI/LLM Infrastructure)

| 组件 | 类型 | 配置 Key / 依赖 | 提供商 | 用途 |
|------|------|-----------------|--------|------|
| DashScope (qwen-plus) | Chat Model | langchain4j.open-ai.chat-model | 阿里云 | LLM 推理 |
| DashScope (text-embedding-v3) | Embedding Model | langchain4j.open-ai.embedding-model | 阿里云 | 文本向量化 |
| Milvus | Vector DB | milvus.* | 自部署 | 向量存储与检索 |
| Elasticsearch | 混合检索 + 向量存储 | elasticsearch.* + spring.ai.vector-store | 自部署 | 关键词检索 + 向量检索 |
| BGE Reranker | Reranker | bge.reranker.* / rag.rerank.* | 自部署/API | 检索结果重排序 |
| Spring AI ChatModel | Chat Model | spring.ai.openai.* | OpenAI兼容 | ReAct Agent |

### Maven 依赖中的中间件 Client

| GroupId | ArtifactId | 对应中间件 |
|---------|-----------|-----------|
```

## Core Pitfalls

1. **Multi-profile configs**: Projects often have `application-sit.yml`, `application-prod.yml` etc. with different URLs per region. Scan ALL profiles, not just default.
2. **Custom Kafka configs**: Some projects connect to two Kafka clusters via `KafkaPrimaryConfig`/`KafkaSecondaryConfig` instead of standard auto-config. The `spring.kafka.bootstrap-servers` may only show ONE cluster — the second is hidden in custom `@Configuration` classes.
3. **MqttMessageEntity without MQTT client**: Some projects define DTOs named like `MqttMessageEntity` for Kafka/REST message-passing without actual MQTT client library. Check pom.xml before reporting MQTT.
4. **Dual services pattern**: Projects may use BOTH AWS SesClient AND JavaMailSender, or BOTH Kafka AND RabbitMQ. Don't stop at finding one — grep for both.
5. **@Value Map injection**: `@Value("#{${mz.region-uri}}")` injects a Map for region-based routing. Each entry is a separate endpoint.
6. **K8s manifests at project root**: `sit_*.yml`/`prod_*.yml` K8s manifests may contain env vars revealing infrastructure. Grep `kind: Deployment|kind: ConfigMap` at root level.
7. **Always specify `path` in glob/grep**: Relative patterns may fail if CWD ≠ project root. Use the workspace root explicitly.
8. **Verify glob hits early**: If `src/main/java/**/*.java` returns nothing, retry with explicit `path` parameter — CWD may differ.
9. **RestTemplate-only projects (no Feign)**: Some projects use RestTemplate exclusively for external calls, with URLs either injected via `@Value` or hardcoded in Java enums (e.g., `Env` enum per region). When `@FeignClient` grep returns nothing, always grep `RestTemplate` as fallback — do not assume no external HTTP calls exist. Hardcoded enum URLs require a separate grep for `http://` in .java files to discover.
10. **Commented-out controllers = dead SDK integration**: If a Controller class is entirely commented out (e.g., `//package ...`), the corresponding SDK dependency may still be in pom.xml but unused at runtime. Flag these as dead code rather than active dependencies. Grep for `//package` or `//import` at file start to detect.
11. **Caffeine as in-memory middleware**: Many projects use Caffeine cache for token/response caching without a Redis dependency. This is a real infrastructure dependency (affects memory footprint, cache invalidation behavior) but is invisible in config files. Only discovered via code grep.
12. **Multi-cloud per-region profiles**: Some projects deploy to multiple cloud regions, each using a different cloud provider (e.g., cn→Alibaba OSS, na/eu→AWS S3, ru→Huawei OBS). Each region profile may use entirely different config key structures (`config.sts.*` for AWS/Alibaba vs `config.iam.*` for Huawei) and different SDK beans. You must read ALL profile configs — a single profile only shows one cloud's dependencies. When you see profile names like `cn-sit`, `na-prod`, `ru-sit`, expect multi-cloud.
13. **@Profile-gated FeignClients**: Feign clients may have `@Profile("!ru")` or similar, making them conditionally active per region. A simple `@FeignClient` grep finds them, but the profile constraint means they're NOT always present at runtime. Always check for `@Profile` on Feign client interfaces and note the constraint in the report.
14. **RestTemplate fallback alongside cloud SDKs**: When a cloud SDK doesn't provide a convenient method for all operations (e.g., Huawei SDK IAM client can't do everything), services fall back to `RestTemplate` to call REST endpoints directly. This dual-pattern (SDK + RestTemplate for same cloud provider) is invisible if you only grep for SDK imports. Always cross-reference: if a service uses a cloud SDK, check if it ALSO uses RestTemplate for the same provider.
15. **Transitive dependencies from parent POM / core library**: The project's own pom.xml may only show a `<parent>` and a `core` dependency, while the real middleware clients (Spring Cloud, Feign, etc.) are inherited. Read the parent POM and core library POM from `~/.m2/repository/` (path: `~/.m2/repository/<groupId-path>/<artifactId>/<version>/<artifactId>-<version>.pom`) to discover transitive dependencies invisible in the project's own pom.xml.
16. **Dual-pathway Service (RestTemplate + Feign in same class)**: Some services route between two completely different HTTP client strategies based on a product/platform constant. E.g., `if (PRODUCT_PLATFORM_ROBOZONE.equals(platform))` → use RestTemplate + custom API/HTTP utility classes + region enum (MzEnv) for URL resolution; `else if (PRODUCT_PLATFORM_MIDEA.equals(platform))` → use Feign client + MJService. A simple `@FeignClient` grep only reveals the MIDEA pathway; the ROBOZONE pathway is invisible unless you also grep `RestTemplate` and custom utility classes. **Always check for branching in Service classes** — a single `@FeignClient` hit does NOT mean all external calls go through Feign.
17. **Dual AI framework coexistence (LangChain4j + Spring AI)**: Some projects use BOTH LangChain4j and Spring AI simultaneously — LangChain4j for the core RAG pipeline (embedding, retrieval, memory, query transformation) and Spring AI for specific features (ChatModel for ReAct agents, VectorStore for ES integration, document readers for PDF/Tika). A grep for only `dev.langchain4j` misses the Spring AI layer and vice versa. **Always grep for both frameworks** when either one is detected in pom.xml.
18. **Vector DB as middleware tier**: Vector databases (Milvus, Pinecone, Chroma, Weaviate) are a distinct infrastructure tier — they store embeddings, not traditional data. They appear in pom.xml as `langchain4j-milvus` or `spring-ai-milvus-store` (not as JDBC drivers), and are configured under custom prefixes (`milvus.*`) rather than `spring.datasource.*`. Some projects run BOTH Milvus AND Elasticsearch as dual vector stores, with `milvus.enable` and `elasticsearch.enable` feature flags to toggle between them. **Check for `*.enable` flags** — a vector DB in pom.xml may be conditionally active.
19. **LLM API providers behind custom config keys**: LLM APIs (DashScope, OpenAI, Azure OpenAI, etc.) are often configured under `langchain4j.open-ai.*` or `spring.ai.openai.*` with a `base-url` pointing to a compatible endpoint (e.g., `dashscope.aliyuncs.com/compatible-mode/v1` for Alibaba DashScope using OpenAI-compatible API). The same API key may serve BOTH chat and embedding models. **Always check `base-url` to identify the actual LLM provider** — `langchain4j.open-ai` doesn't necessarily mean OpenAI; it could be DashScope, DeepSeek, or any OpenAI-compatible API.
20. **@ConditionalOnProperty for AI/RAG feature gates**: RAG projects commonly use `@ConditionalOnProperty(name = "rag.query-expansion.enabled", havingValue = "true")` or `@ConditionalOnProperty(name = "rag.context-aware.enabled", havingValue = "true")` to gate AI features. These beans are invisible at runtime unless the feature flag is set. **Grep for `@ConditionalOnProperty.*rag\|@ConditionalOnProperty.*langchain4j\|@ConditionalOnProperty.*milvus\|@ConditionalOnProperty.*embedding`** to discover gated AI features that may not appear in a standard dependency scan.
21. **Reranker as hidden external service**: RAG pipelines often call a reranker API (BGE Reranker, Cohere Rerank, DashScope GTE-Rerank) as a separate HTTP call after initial retrieval. This service is configured under `bge.reranker.*`, `rag.rerank.*`, or `tavily.*` and is NOT a Spring-managed auto-configuration — it's typically a custom `@Component` using `RestTemplate` or `WebClient`. **Grep for `ScoringModel\|RerankModel\|BgeScoring`** to discover reranker integrations invisible in config scanning.

## Business Logic Exploration (Extended Scan)

When the user asks to "understand the business logic", "write business logic", "explore all services", or "read every service implementation", expand the scan beyond infrastructure to cover:

1. **Read ALL Controller classes** — map every API endpoint and request/response type
2. **Read ALL ServiceImpl classes** — understand business rules, dual implementations, branching logic
3. **Read ALL Entity/DTO classes** — domain model, field semantics, validation
4. **Read ALL Mapper/DAO classes** — data access patterns, custom SQL
5. **Read Kafka listeners** — async message processing
6. **Read config classes that define business behavior** — Env enums, security pipelines, interceptors

For each business domain, document:
- Business purpose (what it does for end users)
- Call chain: Controller → Service → Mapper → External
- Dual/multiple implementations of the same interface
- Profile-gated or region-specific behavior

Save business logic analysis as `references/<project-name>-business-logic.md` under the skill directory.

**Where to persist business logic output**: When the user explicitly asks to write business logic into a specific file (e.g., `@doc/infrastructure-dependencies.md`), append it as a new top-level section (##) at the end of that file — do NOT create a separate file unless asked. When no specific file is given, create a new `doc/business-logic.md` or append to the existing infrastructure doc at `doc/infrastructure-dependencies.md`. Always check if the target file already has infrastructure content and append after it.

## Tips

- Run grep searches in parallel batches to speed up scanning
- For large projects, start with pom.xml + config files first to get the high-level picture, then drill into code
- When scanning a new project, save results to `references/<project-name>-scan.md` for future reference
- **Persist scan output to the project directory** (default: `doc/infrastructure-dependencies.md`). Do NOT just display inline.
- **When doing business logic exploration**, also save a reference file under the skill's `references/` directory so future sessions can build on prior knowledge without re-reading the entire codebase.
- **Business logic doc format**: Use Chinese headings matching the project's existing doc style. Cover: functional domains (功能域), API endpoints table per domain, dual-implementation strategies (V1/V2 vs V3), sync logic, concurrency control (lock keys, timeouts), scheduled tasks, Kafka consumers, IOT command routing, interceptors/filters, and flow diagrams in ASCII art. Group by domain, not by layer.
- **Post-scan domain questions**: Users often follow up a dependency scan with domain-specific questions (e.g., "语音INDEX是怎么来的？" after scanning m7-voice). These questions reveal business concepts tied to infrastructure. When answering, trace from Controller → Service → Mapper to show the full call chain. Add these domain insights to the skill's `references/<project-name>-scan.md` under a "业务领域知识" section so future sessions already know the context.

## Reference Files

For detailed examples of patterns found across specific project scans, see `references/` directory:
- `advanced-pitfalls.md` — Edge cases: Nacos/ConfigCenter, K8s ConfigMap, multi-Kafka, ClickHouse dual-datasource, multi-cloud object storage, RTC platforms, Forest HTTP client, OS-level binaries, etc.
- Per-project scan files (e.g., `m7-voice-scan.md`, `robot-event-scan.md`) — for context on previously scanned projects
