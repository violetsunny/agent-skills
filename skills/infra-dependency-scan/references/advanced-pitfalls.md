# Advanced Pitfalls for Infrastructure Dependency Scan

This file contains edge cases and project-specific patterns discovered across multiple scans. Consult this when the standard scan procedure misses something.

## Config & Environment

- **Nacos/Config Center**: Some projects externalize config to Nacos/Apollo. The local yml may only have bootstrap config. Check for `spring.cloud.nacos.*` and note that full config is in the config center.
- **Kubernetes ConfigMap**: In K8s-deployed Spring Boot services, infrastructure config (Redis host, Kafka bootstrap-servers, datasource URLs) is often stored in K8s ConfigMaps and injected as environment variables. The local yml may only have partial config with comments like `# host存在k8s configMap`. Look for these comments and also check for `k8s/`, `deploy/`, `helm/` directories with ConfigMap manifests. Grep for `CONFIGMAP|configMap|config-map` in the project root.
- **Selective middleware per profile**: Not all profiles use the same middleware. E.g., Kafka may appear only in `ru-prod` while other profiles omit it. Always scan ALL profiles independently — do not assume one profile's middleware list applies to all.

## HTTP Clients

- **Feign vs RestTemplate**: Some projects use both. Don't assume one pattern.
- **Region-suffixed Feign clients**: In multi-region IoT projects, the same external service often has multiple Feign client classes with region suffixes (e.g., `OTACnServiceFeign`, `OTANaServiceFeign`, `OTAEuServiceFeign`). These all call the same logical service but route to different regional endpoints. Group them as one service entry in the inventory, noting the region variants.
- **@Value URL + RestTemplate**: Not all HTTP calls use Feign. Some services inject a base URL via `@Value("${service-name.address}")` and call it with `RestTemplate`. Search for `@Value.*address` or `@Value.*url` combined with `RestTemplate` usage to find these.
- **Forest HTTP client**: `com.dtflys.forest:forest-spring-boot-starter` is a declarative HTTP client (like Feign) but uses `@ForestClient`, `@Get`, `@Post` etc. instead of `@FeignClient`. If pom.xml has this dependency, grep for `@ForestClient` and `@Get|@Post` in Forest client interfaces to find external HTTP services. Projects using both Feign and Forest are common in Midea codebases.
- **Hardcoded service URLs in enums**: Some integrations embed service URLs and API keys directly in Java enums or constants (e.g., `Env.CN_PRO("key", "http://iot4.midea.com.cn:28050")`). Grep for `http://` and `https://` patterns in enum and constant files.

## Messaging

- **Spring Cloud Stream over RabbitMQ**: Some projects use Spring Cloud Stream abstraction (`@EnableBinding`, `@StreamListener`, `StreamBridge`) instead of direct `@RabbitListener`/`RabbitTemplate`. The binding interface class (e.g., `RabbitStreamMessageBinding`) defines input/output channel names that map to actual queue/exchange names in config. Always grep for `@EnableBinding|@StreamListener|StreamBridge` to catch this pattern.
- **Multi-Kafka-cluster**: Some projects run multiple Kafka clusters with custom Spring config prefixes like `spring.kafka2.*`, `spring.device-unbind-kafka.*`. Each has its own `containerFactory` and `@KafkaListener`. Grep for custom `containerFactory` names and `@KafkaListener` annotations to find all clusters. The standard `spring.kafka.*` only covers the primary cluster.

## Databases

- **ClickHouse dual-datasource**: Projects with MySQL + ClickHouse often use `dynamic-datasource-spring-boot-starter` or custom `SqlSessionFactory` beans (e.g., `clickhouseSqlSessionFactory`) with `@MapperScan` pointing to separate mapper packages. Config key is typically `clickhouse.*` (not under `spring.datasource`). Grep for `ClickhouseDataSourceConfig`, `clickhouse.*` config, and `mybatis.clickhouse` mapper packages.
- **Druid datasource**: `spring.datasource.type: com.alibaba.druid.pool.DruidDataSource` and `spring.datasource.druid.*` config keys indicate Alibaba Druid pool. Druid has its own config keys under `druid:` that differ from HikariCP's `hikari:` keys.

## Object Storage

- **AWS dual-SDK version**: Projects using both AWS SDK v1 (`com.amazonaws.services.s3.AmazonS3`) and v2 (`software.amazon.awssdk.services.cloudfront.CloudFrontUtilities`) are common. S3 often uses v1, CloudFront uses v2. Report both SDK versions separately.
- **Multi-cloud object storage**: Some projects use AWS S3, Aliyun OSS, and Huawei OBS simultaneously (e.g., for region-based file routing). All three have separate SDKs and config keys. Maven artifacts: `aws-java-sdk-s3` (AWS v1), `aliyun-sdk-oss` (阿里云), `esdk-obs-java-bundle` (华为云). Grep for `AmazonS3`, `OSSClient`, `ObsClient` respectively.

## Special Integrations

- **RTC/Communication platforms**: Real-time communication SDKs like Agora/声网 (`io.agora.media.RtcTokenBuilder2`), Twilio, or ZEGO are common in IoT/video projects. They may appear as: (1) Maven dependencies for token generation, (2) Feign clients calling their REST APIs (e.g., `@FeignClient(url="${sw.domain:api.sd-rtn.com}")`), (3) custom config keys for app ID/certificate/secret. Grep for `agora`, `shengwang`, `zego`, `twilio`, `rtc`, `RtcToken` in Java source and config files.
- **OS-level binary dependencies**: Some projects depend on external command-line tools (e.g., FFmpeg, ImageMagick, wkhtmltopdf) invoked via `ProcessBuilder` or Java wrapper libraries (e.g., `net.bramp.ffmpeg`). These are NOT found by scanning Maven dependencies alone. Grep for `ProcessBuilder`, `Runtime.exec`, and `@Value` paths pointing to binary locations (e.g., `path.ffmpeg: /usr/bin/ffmpeg`). Also check for wrapper library artifacts in pom.xml (e.g., `net.bramp.ffmpeg`). Report these as infrastructure dependencies under a separate "OS/Binary Dependencies" section.

## Code-Level Pitfalls

- **Silent null-safety issues**: Map.get() → URI.create without null-check can NPE. Note these in the inventory if found.
- **@Value with Map**: `@Value("#{${mz.region-uri}}")` injects a Map — this is a region-based URI routing pattern (common in Midea projects). Each map entry is a separate service endpoint.

## Build

- **Maven parent POM**: If the parent POM is not in a public repo, `mvn compile` won't work locally. Don't try to verify dependencies that way — rely on static analysis of pom.xml.
