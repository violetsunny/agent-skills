# archify 选型与门失败 playbook（嵌入场景）

批量生产实测沉淀（AIOTK LLMentor-handbook 37 页 / 44 artifact，archify 3.2.0 基线 + 3.3.0 增补）。写 candidate 前先过预检，把失败消灭在 finalize 之前。

## 类型选择（嵌入场景专用）

| 材料形态 | 首选 type | 禁忌与回落 |
|---|---|---|
| 泳道流程 / 请求处理 / 知识体系分解 | workflow | tree 在 3.2.0 下 stage 随视口拉伸（100vh），索引面板恒在折叠线下，测高失效——**嵌入场景禁默认用 tree**；仅当测高确认 content-driven 才可用，否则改 workflow 或走 variants.md 静态路线 |
| 系统组件 / 嵌套容器 | architecture | 渐变背景，测高走 p90 口径（脚本自动判别） |
| 数据流 | dataflow | 出现异常高画布（~3200px 白面板居中、上下大片空白）时回落 workflow |
| 时序交互 | sequence | stage min-height:100vh flex 垂直居中，内部滚动是固有行为；测高用 harness 读 scrollHeight（见下） |
| 循环 / 生命周期 | lifecycle 或 workflow | — |
| 时间演进 | timeline | **强制 ISO 日期；材料无日期即编造，禁选**，改 workflow |

## 写 candidate 前预检

1. workflow deliver 节点 col ≤ 5，超则分泳道。
2. canvas 宽 ≤ 1240px（sublabel-readability 门超限报 error），超则**合并节点减列**（实测 6 列 1246px → 合并 stuff+gen 减到 5 列一次过四门）；压 sublabel 字号伤可读性，不采用。
3. return / error 边**不写 route / fromSide / toSide**，交渲染器自动路由（硬写触发 route-preset-conflict、composition/proper-crossing、ambiguous-corridor、clean-flow/endpoint-side-direction）。
4. workflow mainPath 单调前进不得 col 回退；回边改 `role:"branch"` 放 mainPath 外。
5. dataflow 每条 flow 必须有 `label`；route 枚举 3.2.0 为 `auto|straight|vertical-channel|bottom-channel|top-channel`，**3.3.0 新增 up-channel/drop/outside-right/return-left**——按当前安装版本实测为准。
6. 双图页两个 candidate 命名 `candidate-<slugA>.json` / `candidate-<slugB>.json`，防同名互覆。
7. 跨泳道长边自动路由不可控（穿节点/绕路撞节点）：**删边**，语义放 explanation/card；设计时只用相邻泳道短虚线跨边（实测 ch13-2 两条短跨边一次过）。
8. 细节写不下进 explanation（3.3.0 ≤1200 字符），不堆节点；lanes/nodes/edges/cards 无 maxItems（4 泳道合法）。

## 门失败处置

- finalize 失败按报错的 `supportedFixes` 修，不瞎试。
- 换图类型对同一输出路径重跑 finalize 报 browser-check `evidence-path-conflict`（will not replace the existing unowned evidence path）→ 旧 receipts 移入 `_superseded-<type>/` 再重跑。
- `finalize <type>` 的 type 是必填第一位置参数，漏掉报 cli/usage。
- 批量生产用 `--quality showcase --json`。
- 非零退出不是成功；四门（validate/deliver/check/browser-check）全过才算出图完成。
- **delivery.json 非确定性产出**（同流程有的 artifact 有、有的没有），不得作为「必产」断言。
- receipt 双目录：全站扫描器只认 `validation/archify/<slug>/`——新 artifact 除 embed 目录外，须另建该目录放 candidate.json（重命名）+ 全部 receipt + **artifact 字节副本**，否则扫描报「sha 与 receipt 不一致 (receipt=None)」。

## sequence 类 harness 测高

角点采样对 100vh 居中产物在任何窗口高都报触底，无干净不动点。改父页 harness：iframe 加载产物 + `getBoundingClientRect` 读 SVGH 与 scrollHeight，Chrome 加 `--allow-file-access-from-files --virtual-time-budget=4000 --dump-dom`；iframe 定高取 scrollHeight，接受内部滚动（固有行为，非缺陷）。

## 版本注意

以上口径基于 archify 3.2.0 实测 + 3.3.0 增补（route 枚举/canvas 修法/交叉边/explanation 容量）。升级 archify 后 tree 视口行为与门限可能变化，须重测再更新本文件；批量生产期间冻结版本，不中途升级。