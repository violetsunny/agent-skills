#!/usr/bin/env python3
"""多版本选优计分（multi-version-selection.md 受众权重表 + 一票否决 + 选优决策规则）。

用法:
  python3 review_score.py scores.json [--audience 领导层]

输入 JSON 形状:
  {
    "audience": "领导层",            // 领导层(默认)/技术同行/外部客户/大众；别名: 公开传播→大众
    "versions": [
      {
        "name": "A",
        "scores": {"信息传达":5,"视觉张力":3,"品牌契合":4,"技术稳健":5,"受众适配":4},
        "brandViolation": false,     // 可选: 品牌守门判定违反硬条款 → 一票否决 2
        "contrastFail": false        // 可选: 正文对比度实测 <4.5:1 → 先修再评（否决 3）
      }
    ]
  }

规则:
  - 一票否决先于加权总分: ① 技术稳健=1（打不开/白屏/报错/溢出/navSafeIntrusionPx>0）出局
    ② 品牌规范硬条款违反出局 ③ 对比度不达标先修再评，不带病打分
  - 加权总分 = Σ(分×权重)/Σ权重，保留两位；权重表见 md（领导层 5/2/3/3/4 等四行）
  - 决策: 分差 ≥0.5 取高分版；<0.5 比"决策者视角"单项（该受众权重最高维）取高者；
    仍平 → 摆出取舍点让用户裁决，不平摊不折中
  - 退出码: 0=选出定版 1=无法机器定版（全部出局 / 平局待用户裁决） 2=输入 schema 违规
"""

import argparse
import json
import sys

DIMENSIONS = ["信息传达", "视觉张力", "品牌契合", "技术稳健", "受众适配"]

WEIGHTS = {
    "领导层": [5, 2, 3, 3, 4],
    "技术同行": [5, 2, 2, 4, 4],
    "外部客户": [4, 3, 5, 3, 4],
    "大众": [3, 5, 4, 3, 4],
    "公开传播": [3, 5, 4, 3, 4],
}


def fail(msg):
    print(f"FAIL {msg}", file=sys.stderr)
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scores_json")
    ap.add_argument("--audience", default="", help="覆盖 JSON 内的受众声明")
    args = ap.parse_args()

    try:
        with open(args.scores_json, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        fail(f"读取打分 JSON 失败: {e}")

    audience = args.audience or data.get("audience") or "领导层"
    if audience not in WEIGHTS:
        fail(f"未知受众 '{audience}'，可选: {'/'.join(WEIGHTS)}")
    weights = WEIGHTS[audience]
    wsum = sum(weights)
    decision_dim = DIMENSIONS[weights.index(max(weights))]

    versions = data.get("versions")
    if not isinstance(versions, list) or len(versions) < 2:
        fail("versions 需要 ≥2 个版本")

    alive, vetoed = [], []
    for v in versions:
        name = v.get("name")
        if not name:
            fail("版本缺 name 字段")
        scores = v.get("scores")
        if not isinstance(scores, dict) or any(d not in scores for d in DIMENSIONS):
            fail(f"{name}: scores 缺维度，需要全五维 {DIMENSIONS}")
        for d in DIMENSIONS:
            s = scores[d]
            if not isinstance(s, (int, float)) or not (1 <= s <= 5):
                fail(f"{name}: {d}={s!r} 超出 1-5 分")
        if scores["技术稳健"] == 1:
            vetoed.append((name, "一票否决①: 技术稳健=1（打不开/白屏/报错/溢出）"))
            continue
        if v.get("brandViolation"):
            vetoed.append((name, "一票否决②: 品牌守门判定违反硬条款"))
            continue
        if v.get("contrastFail"):
            vetoed.append((name, "一票否决③: 正文对比度 <4.5:1，先修再评"))
            continue
        total = round(sum(scores[d] * w for d, w in zip(DIMENSIONS, weights)) / wsum, 2)
        alive.append((name, total, scores))

    print(f"受众: {audience}  权重: {dict(zip(DIMENSIONS, weights))}")
    for name, reason in vetoed:
        print(f"[出局] {name}: {reason}")
    if not alive:
        print("FAIL 全部版本被一票否决，无可排名版本")
        sys.exit(1)

    alive.sort(key=lambda x: -x[1])
    print("--- 加权总分排名 ---")
    for i, (name, total, _) in enumerate(alive, 1):
        print(f"{i}. {name}: {total:.2f}")

    if len(alive) == 1:
        print(f"选择: {alive[0][0]}（其余全部出局）")
        print("提醒: 落选版本移入 variants/ 留档，禁止跨版取材（选择无效铁律）")
        sys.exit(0)

    (n1, t1, s1), (n2, t2, s2) = alive[0], alive[1]
    gap = round(t1 - t2, 2)
    if gap >= 0.5:
        print(f"选择: {n1}（分差 {gap:.2f} ≥ 0.5，取高分版）")
        print("提醒: 落选版本移入 variants/ 留档，禁止跨版取材（选择无效铁律）")
        sys.exit(0)

    d1, d2 = s1[decision_dim], s2[decision_dim]
    print(
        f"分差 {gap:.2f} < 0.5，比决策者视角单项（{decision_dim}）: {n1}={d1} vs {n2}={d2}"
    )
    if d1 != d2:
        winner = n1 if d1 > d2 else n2
        print(f"选择: {winner}（决策者视角单项更高）")
        print("提醒: 落选版本移入 variants/ 留档，禁止跨版取材（选择无效铁律）")
        sys.exit(0)

    print(
        f"无法机器定版: {n1} 与 {n2} 总分差 {gap:.2f} 且 {decision_dim} 单项持平——"
        "摆出两版取舍点让用户裁决，不平摊、不折中"
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
