# AGENT RULE


## Project-specific rules below this line

### Stack & Versions
- Primary: SpringBoot 3.x + SpringCloud (JDK 21 preferred; JDK 8 for legacy)
- Secondary: Python 3.13 (data/scripting only)
- Build: Maven (preferred)
- DB: MySQL/PostgreSQL + MyBatis-Plus
- Cache: Redis; MQ: RocketMQ/Kafka

### JDK Features by Version
- **JDK 8**: Stream, Lambda, Optional, LocalDateTime (avoid legacy Date/Calendar)
- **JDK 21**: Virtual Threads, Records, Text Blocks, Pattern Matching, Sequenced Collections

### Spring/Cloud Practices
- Feign: use fallback factories
- Config: `@ConfigurationProperties` over `@Value`; use `application-{profile}.yml`
- Errors: global `@RestControllerAdvice` with consistent format
- DTOs: Records (JDK 21) or Lombok `@Value` (JDK 8)
- Logging: `@Slf4j` + correlation ID in headers

### Testing & Quality
- Spring: `./mvnw test` / `./gradlew test`; coverage target 80%+
- Python: `pytest tests/ -v` + type hints + `mypy`

### Security & Secrets
- Never commit `application-prod.yml`, `.env`, or credentials
- Use Spring Cloud Config / Vault for prod secrets

### Error Patterns to Watch
- `RetryableException` (Feign) → retry with backoff
- `OptimisticLockException` → retry with version check
- `DataIntegrityViolationException` → handle constraint violations gracefully

---
