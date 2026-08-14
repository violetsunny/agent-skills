# rag-demo Infrastructure Scan Reference

> 扫描日期: 2026-08-04 | 项目路径: /Users/kangll13/aiot/java-code/self/gggggggood/LLMentor/rag-demo

## 项目概述

RAG Demo — 基于 LangChain4j + Spring AI 的高级 RAG 系统，支持混合检索、多格式文档处理、ReAct Agent。

## 技术栈

- **Spring Boot 3.x** (parent: cn.hollis.llm:LLMentor:1.0.0-SNAPSHOT)
- **JDK 21** (MyBatis-Plus Boot3 starter)
- **LangChain4j 1.13.0** (核心 RAG 框架)
- **Spring AI 1.1.4** (补充 ChatModel / VectorStore / Document Reader)

## 基础设施依赖清单

### 中间件 (Middleware)

| 名称 | 类型 | 配置 Key | 用途 |
|------|------|----------|------|
| MySQL | 数据库 | spring.datasource.url → ardm | 主数据存储（知识库文档、对话记录等） |
| Redis | 缓存 | spring.data.redis.* | 聊天记忆存储 (rag-demo:chat-memory:*) |
| Elasticsearch 8.11 | 混合检索+向量存储 | elasticsearch.* + spring-ai-starter-vector-store-elasticsearch | 关键词检索 + 向量检索 |
| Milvus 2.5 | 向量数据库 | milvus.* | 向量存储与检索（IVF_FLAT/COSINE） |
| MinIO | 对象存储 | minio.* | 图片存储（默认禁用 minio.enable=false） |

### AI/LLM 基础设施 (AI/LLM Infrastructure)

| 组件 | 类型 | 配置 Key / 依赖 | 提供商 | 用途 |
|------|------|-----------------|--------|------|
| DashScope (qwen-plus) | Chat Model | langchain4j.open-ai.chat-model → base-url: dashscope.aliyuncs.com | 阿里云 | LLM 推理（主对话、查询改写、意图识别） |
| DashScope (text-embedding-v3) | Embedding Model | langchain4j.open-ai.embedding-model → base-url: dashscope.aliyuncs.com | 阿里云 | 文本向量化 (dim=1536) |
| BGE-small-zh-v15 | Local Embedding | langchain4j-embeddings-bge-small-zh-v15 (ONNX) | 本地 | 离线中文向量化 (provider=bge-local 时使用) |
| DashScope GTE-Rerank | Reranker | rag.rerank.* → provider=dashscope, model=gte-rerank-v2 | 阿里云 | 检索结果重排序 |
| BGE Reranker (HTTP) | Reranker | bge.reranker.* → url, timeout-ms | 自部署 | 本地重排序服务（默认禁用） |
| Spring AI ChatModel | Chat Model | spring-ai-starter-model-openai | OpenAI兼容 | ReAct Agent 对话 |
| Tavily Search | Web Search API | tavily.* → api-key, search-depth, max-results | Tavily | RAG Web 搜索增强（默认 api-key 空=降级为 mock） |

### Maven 依赖中的中间件 Client

| GroupId | ArtifactId | 版本 | 对应中间件 |
|---------|-----------|------|-----------|
| dev.langchain4j | langchain4j | 1.13.0 | LangChain4j 核心 |
| dev.langchain4j | langchain4j-open-ai | 1.13.0 | OpenAI 兼容 API（用于 DashScope） |
| dev.langchain4j | langchain4j-milvus | 1.13.0-beta23 | Milvus 向量存储 |
| dev.langchain4j | langchain4j-elasticsearch | 1.13.0-beta23 | ES 向量存储 |
| dev.langchain4j | langchain4j-embeddings-bge-small-zh-v15 | 1.13.0-beta23 | BGE 中文 Embedding (ONNX) |
| dev.langchain4j | langchain4j-document-parser-apache-tika | 1.13.0-beta23 | Tika 文档解析 |
| dev.langchain4j | langchain4j-spring-boot-starter | 1.13.0-beta23 | LangChain4j Spring Boot 自动配置 |
| org.springframework.ai | spring-ai-starter-model-openai | 1.1.4 | Spring AI OpenAI 兼容 |
| org.springframework.ai | spring-ai-starter-vector-store-elasticsearch | 1.1.4 | Spring AI ES VectorStore |
| org.springframework.ai | spring-ai-advisors-vector-store | 1.1.4 | Spring AI 向量检索 Advisor |
| org.springframework.ai | spring-ai-pdf-document-reader | 1.1.4 | PDF 文档读取 |
| org.springframework.ai | spring-ai-tika-document-reader | 1.1.4 | Tika 文档读取 |
| io.milvus | milvus-sdk-java | 2.5.6 | Milvus Java SDK |
| co.elastic.clients | elasticsearch-java | 8.11.0 | ES Java Client v8 |
| org.elasticsearch.client | elasticsearch-rest-high-level-client | 7.17.21 | ES RestHighLevelClient (v7 兼容) |
| io.minio | minio | 8.5.1 | MinIO 对象存储 |
| com.mysql | mysql-connector-j | runtime | MySQL JDBC |
| com.baomidou | mybatis-plus-spring-boot3-starter | 3.5.9 | MyBatis-Plus |
| org.apache.pdfbox | pdfbox | 3.0.1 | PDF 处理 |
| org.apache.poi | poi-ooxml | 5.2.5 | Word/DOCX 处理 |
| com.alibaba | easyexcel | 3.3.4 | Excel/CSV 处理 |
| org.codehaus.groovy | groovy-jsr223 | 3.0.21 | CodeExecutorTool 沙箱 |

## 配置类列表

| 类名 | 注解 | 用途 |
|------|------|------|
| RagDemoApplication | @SpringBootApplication, @MapperScan | 启动类，扫描 cn.hollis.llm.mentor.ragdemo.mapper |
| RagConfiguration | @Configuration | RAG 核心配置：ContentRetriever, QueryTransformer, AiServices |
| LangChain4jConfig | @Configuration | LangChain4j ChatModel/StreamingChatModel/EmbeddingModel Bean |
| ElasticsearchConfig | @Configuration | ES Client 初始化、索引创建 |
| AsyncConfig | @Configuration, @EnableAsync | 异步线程池配置 |
| MybatisPlusConfig | @Configuration | MyBatis-Plus 分页插件 |

## @ConditionalOn* 条件 Bean

| 类 | 条件 | 说明 |
|----|------|------|
| ContextAwareQueryTransformer | @ConditionalOnProperty(name="rag.context-aware.enabled", havingValue="true") | 上下文感知查询改写 |
| QueryExpansionTransformer | @ConditionalOnProperty(name="rag.query-expansion.enabled", havingValue="true") | 查询扩展 |

## 关键架构模式

1. **双 AI 框架共存**: LangChain4j 负责 RAG pipeline (embedding, retrieval, memory, query transformation)，Spring AI 负责 ChatModel (ReAct Agent) + VectorStore (ES) + Document Reader
2. **双向量存储**: Milvus + Elasticsearch，通过 `milvus.enable` / `elasticsearch.enable` 切换
3. **三重检索+RRF融合+粗排+精排**: 向量检索→关键词检索→元数据检索→RRF融合→Rerank粗排→Rerank精排
4. **本地/云端双 Embedding**: DashScope API (provider=dashscope) vs 本地 BGE ONNX (provider=bge-local)
5. **Redis 聊天记忆**: 通过 DatabaseChatMemoryStore + Redis 实现，TTL 1小时
6. **降级模式**: MinIO 默认禁用、BGE Reranker 默认禁用（降级为词频匹配）、Tavily 无 key 降级为 mock

## 数据库表

- knowledge_document — 知识文档主表
- knowledge_document_version — 文档版本表
- chat_message — 聊天消息记录

## 包结构

```
cn.hollis.llm.mentor.ragdemo/
├── RagDemoApplication.java        # 启动类
├── agent/                          # ReAct Agent
│   ├── AgentChatParam.java
│   ├── AgentChatResult.java
│   └── RagReactAgent.java          # Spring AI ChatModel 驱动
├── ai/                             # AI 服务
│   ├── CommonChatService.java       # 通用对话
│   ├── IntentRecognitionService.java # 意图识别
│   └── RagStreamingService.java     # RAG 流式服务
├── config/                         # 配置类
│   ├── AsyncConfig.java
│   ├── ElasticsearchConfig.java
│   ├── LangChain4jConfig.java
│   ├── MybatisPlusConfig.java
│   └── RagConfiguration.java       # RAG 核心 Bean 装配
├── controller/                     # REST API
├── embedding/                      # 向量存储
│   └── VectorStoreService.java     # Milvus + ES 双存储抽象
├── entity/                         # 数据实体
├── event/                          # 事件驱动
│   ├── DocumentSplitCompletedEvent.java
│   └── EmbeddingEventListener.java
├── memory/                         # 对话记忆
│   └── DatabaseChatMemoryStore.java
├── mapper/                         # MyBatis Mapper
├── progress/                       # 进度追踪
│   ├── ProgressAwareContentAggregator.java
│   └── ProgressAwareContentRetriever.java
├── rerank/                         # 重排序
│   └── BgeScoringModel.java        # BGE Reranker HTTP 客户端
├── retrieval/                      # 检索层
│   ├── HybridRetrievalService.java  # 混合检索核心
│   ├── RetrievalCacheService.java   # 检索缓存
│   └── RerankRateLimiter.java       # Rerank 限流
├── service/                        # 业务服务
│   └── impl/
│       └── DocumentProcessServiceImpl.java
└── transformer/                    # 查询变换
    ├── ContextAwareQueryTransformer.java  # @Conditional
    └── QueryExpansionTransformer.java     # @Conditional
```
