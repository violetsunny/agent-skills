# open-user-service 项目扫描结果

> 扫描日期: 2026-08-04 | 项目路径: /Users/kangll13/aiot/java-code/aiot-robot/open-user-service

## 项目架构

DDD 四层结构:
```
com.midea.open/
├── application/          # 应用服务层 (DeviceService, AuthUserService, etc.)
├── domain/               # 领域层 (device/, command/, product/, user/, etc. 33个子域)
├── infrastructure/       # 基础设施层
│   ├── a4/
│   ├── client/           # Feign客户端按域分目录
│   │   ├── authuser/
│   │   ├── bigmodel/
│   │   ├── css/
│   │   ├── datahub/
│   │   ├── device/       # DeviceServiceFeign
│   │   ├── feedback/
│   │   ├── i18n/
│   │   ├── kong/
│   │   ├── ota/
│   │   ├── security/
│   │   └── voice/
│   ├── config/
│   ├── constant/         # ProductInfoConstant (brand/platform常量)
│   ├── enums/            # MzEnv, MideaEnv (region→URL枚举路由)
│   ├── meiju/            # MJService (美的通路封装)
│   ├── util/             # HTTP.java, API.java (自研通路HTTP工具)
│   └── ...
├── interfaces/           # 接口层
│   ├── api/
│   ├── assembler/
│   ├── dto/
│   └── facade/
└── OpenUserServiceApplication.java
```

## 关键架构模式: 双通路 (Dual Pathway)

### DeviceService 中的双通路路由

```java
// 判断逻辑: ProductInfoConstant.PRODUCT_PLATFORM_ROBOZONE vs PRODUCT_PLATFORM_MIDEA
if (ProductInfoConstant.PRODUCT_PLATFORM_ROBOZONE.equals(productInfo.getPlatform())) {
    // 自研通路: MzEnv枚举 + API.java + HTTP.java + RestTemplate
} else {
    // 美的通路: Feign + MJService
}
```

### 自研通路 (ROBOZONE)
- **URL路由**: `MzEnv` 枚举，通过 `@Value("${mz.env}")` 注入当前环境，`@Value("#{${mz.region-uri}}")` 注入 region→URL Map
- **HTTP调用**: `API.java` (签名/鉴权封装) + `HTTP.java` (请求发送) + RestTemplate
- **特点**: 需要自己处理签名、鉴权、超时、URL路由

### 美的通路 (MIDEA)
- **Feign客户端**: `DeviceServiceFeign` + 其他OTA Feign接口
- **封装层**: `MJService` 封装美的平台调用逻辑
- **特点**: 利用Spring Cloud声明式调用，多区域Feign (OTAEuServiceFeign, OTANaServiceFeign)

### ProductInfoConstant 关键常量
- `PRODUCT_BRAND_MIDEA = "midea"`
- `PRODUCT_PLATFORM_ROBOZONE` / `PRODUCT_PLATFORM_MIDEA`

## 中间件依赖

| 名称 | 类型 | 备注 |
|------|------|------|
| MySQL | 数据库 | 主数据存储 |
| Redis | 缓存 | 分布式缓存 |
| Kafka | 消息队列 | 异步消息 |
| Nacos | 注册中心/配置中心 | Spring Cloud |
| Feign | HTTP客户端 | 美的通路 |

**无 XXL-JOB 依赖** — pom.xml 和代码中均无 xxl-job 相关内容。

## Feign客户端清单

DeviceServiceFeign (在 infrastructure/client/device/) — 具体方法签名见源文件。

## 业务域概览

| 域 | 说明 |
|----|------|
| device | 设备管理，双通路命令下发 |
| command | 命令控制 |
| product | 产品信息(platform判断来源) |
| user | 用户管理 |
| firmware | 固件管理 |
| ota | OTA升级 |
| approval | 审批流程 |
| message | 消息通知 |
| whitelist | 白名单 |
