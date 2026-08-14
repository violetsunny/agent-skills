# m7-server Project Scan Reference

Project path: `/Users/kangll13/aiot/java-code/aiot-robot/m7-server`

## Known Scan Results (as of 2026-07)

### Config Files
- `application-ru-sit.yml`, `application-ru-prod.yml` — Russia region
- `application-na-sit.yml`, `application-na-prod.yml` — North America region
- `application-prod.yml` — Default production

### Key Service Classes Found
- `DevToProService.java`
- `ShortcutService.java`
- `TritonInferenceService.java` — AI inference via Triton
- `PartsInfoService.java`

### Known Patterns (from prior sessions)
- Uses RestTemplate/HttpUtils for HTTP calls (no Feign in m7-server)
- Region-based URI routing via `@Value("#{${mz.region-uri}}")` Map pattern
- Maven parent POM not in public repo — cannot `mvn compile` locally
- Kafka, Redis, MySQL are core middleware
- OpenSpec/OTA1 ecosystem uses RestTemplate; open-user-service uses Feign (separate project)
