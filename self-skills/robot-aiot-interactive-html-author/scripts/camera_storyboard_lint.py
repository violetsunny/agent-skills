#!/usr/bin/env python3
"""分镜卡数值校验（camera-storyboard.md §3 对数时长公式 + §2 位移上限 + §11 定景公式）。

用法:
  python3 camera_storyboard_lint.py storyboard.json

输入 JSON 形状（每镜一条，字段按运镜类型取用）:
  {"shots": [
    {"page":1, "move":"定场微推", "zoomStart":1.0, "zoomEnd":1.06, "duration":2.8},
    {"page":3, "move":"推进", "zoomStart":1.0, "zoomEnd":1.45, "duration":0.30,
     "targetBox":[960,540]},
    {"page":4, "move":"静止"},
    {"page":5, "move":"横移", "distancePx":400, "duration":0.67},
    {"page":6, "move":"环绕", "rotY":20, "duration":1.5}
  ]}
  move 取值: 推进/推近/push-in、拉远/pull-out、横移/pan、升降/tilt/crane、
             环绕/orbit、静止/static、定场微推/establishing

规则:
  - 推拉时长 = |0.55 × log2(zoomEnd/zoomStart)| clamp [0.30,1.50]s，容差 ±0.011（两位小数舍入）
  - 例外档: 定场微推（倍率比 ≤1.1）不按公式，固定 2.5-3.0s 慢推
  - 推进上限 2.4x（§1）；横移位移 ≤420px（>860 弃镜改翻页 = FAIL，420-860 = WARN）；
    升降位移 ≤300px
  - 横移/升降时长 = |distancePx|/600 clamp [0.4,1.4]s
  - 环绕: rotY ≤24°、时长 1.2-1.8s、全 deck ≤1 页
  - 定景公式（给了 targetBox 时）: zoom = 0.8/max(w/1920, h/1080) 定档到最近景别档位区间
    （远 0.8-0.85 / 全 1.0 / 中 1.3-1.45 / 近 1.6-1.8 / 特 2.0-2.4），
    zoomEnd 须落该档区间内（边界容差 0.05），否则 FAIL
  - 退出码: 0=全过（WARN 不阻塞） 1=存在 FAIL 2=schema 违规
"""

import argparse
import json
import math
import sys

MOVE_ALIASES = {
    "推进": "zoom",
    "推近": "zoom",
    "push-in": "zoom",
    "push": "zoom",
    "拉远": "zoom",
    "pull-out": "zoom",
    "pull": "zoom",
    "横移": "pan",
    "pan": "pan",
    "升降": "tilt",
    "升": "tilt",
    "降": "tilt",
    "tilt": "tilt",
    "crane": "tilt",
    "环绕": "orbit",
    "orbit": "orbit",
    "静止": "static",
    "static": "static",
    "定场微推": "establish",
    "微推": "establish",
    "establishing": "establish",
}
PUSH_WORDS = {"推进", "推近", "push-in", "push"}

ZOOM_BANDS = [(0.8, 0.85), (1.0, 1.0), (1.3, 1.45), (1.6, 1.8), (2.0, 2.4)]
DUR_TOL = 0.011


def zoom_duration(z0, z1):
    d = 0.55 * math.log2(z1 / z0)
    return min(1.5, max(0.3, abs(d)))


def pan_duration(dist, speed=600.0):
    return min(1.4, max(0.4, abs(dist) / speed))


def snap_to_band(z):
    """定档：返回公式值最近的景别档位区间（区间内即该档，区间外取最近档）"""
    best, best_d = None, float("inf")
    for lo, hi in ZOOM_BANDS:
        d = 0 if lo <= z <= hi else min(abs(z - lo), abs(z - hi))
        if d < best_d:
            best, best_d = (lo, hi), d
    return best


def fail(msg):
    print(f"FAIL {msg}", file=sys.stderr)
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard_json")
    args = ap.parse_args()

    try:
        with open(args.storyboard_json, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        fail(f"读取分镜 JSON 失败: {e}")

    shots = data.get("shots")
    if not isinstance(shots, list) or not shots:
        fail("shots 需要非空数组")

    fails = warns = 0
    orbit_pages = 0

    def report(ok, level, page, msg):
        nonlocal fails, warns
        if ok:
            print(f"[OK  ] 页{page}: {msg}")
        elif level == "FAIL":
            fails += 1
            print(f"[FAIL] 页{page}: {msg}")
        else:
            warns += 1
            print(f"[WARN] 页{page}: {msg}")

    for i, shot in enumerate(shots):
        page = shot.get("page", f"#{i + 1}")
        move_word = str(shot.get("move", "")).strip()
        move = MOVE_ALIASES.get(move_word.lower())
        if move is None:
            fail(f"页{page}: 未知运镜 '{shot.get('move')}'")

        if move == "static":
            report(True, "", page, "静止（永远合法）")
            continue

        if move == "orbit":
            orbit_pages += 1
            rotY = shot.get("rotY")
            dur = shot.get("duration")
            if rotY is None or dur is None:
                fail(f"页{page}: 环绕需要 rotY 与 duration")
            report(abs(rotY) <= 24, "FAIL", page, f"环绕 rotY={rotY}°（上限 24°）")
            report(1.2 <= dur <= 1.8, "FAIL", page, f"环绕时长 {dur}s（要求 1.2-1.8s）")
            continue

        if move in ("pan", "tilt"):
            dist = shot.get("distancePx")
            dur = shot.get("duration")
            if dist is None or dur is None:
                fail(f"页{page}: {move_word} 需要 distancePx 与 duration")
            limit = 420 if move == "pan" else 300
            if move == "pan" and abs(dist) > 860:
                report(
                    False,
                    "FAIL",
                    page,
                    f"横移位移 {dist}px >860（画布宽 45%），弃镜改翻页",
                )
            elif abs(dist) > limit:
                level = "WARN" if move == "pan" else "FAIL"
                report(False, level, page, f"位移 {dist}px 超上限 {limit}px")
            else:
                report(True, "", page, f"位移 {dist}px ≤{limit}px")
            expected = pan_duration(dist)
            report(
                abs(dur - expected) <= DUR_TOL,
                "FAIL",
                page,
                f"时长 {dur}s，公式 clamp(|{dist}|/600, 0.4, 1.4) = {expected:.2f}s",
            )
            continue

        # zoom 类: 推进/拉远/定场微推
        z0, z1, dur = shot.get("zoomStart"), shot.get("zoomEnd"), shot.get("duration")
        if z0 is None or z1 is None or dur is None:
            fail(f"页{page}: {move_word} 需要 zoomStart/zoomEnd/duration")
        if z0 <= 0 or z1 <= 0:
            fail(f"页{page}: 倍率必须 >0")
        if move == "zoom" and move_word.lower() in PUSH_WORDS and z1 > 2.4:
            report(False, "FAIL", page, f"推进终点 {z1}x 超 §1 上限 2.4x")

        ratio = max(z0, z1) / min(z0, z1)
        if move == "establish" or ratio <= 1.1:
            report(
                2.5 <= dur <= 3.0,
                "FAIL",
                page,
                f"定场微推（倍率比 {ratio:.2f}≤1.1）走例外档 2.5-3.0s，实际 {dur}s",
            )
        else:
            expected = zoom_duration(z0, z1)
            report(
                abs(dur - expected) <= DUR_TOL,
                "FAIL",
                page,
                f"时长 {dur}s，公式 clamp(0.55×|log2({z1}/{z0})|, 0.3, 1.5) = {expected:.2f}s",
            )

        box = shot.get("targetBox")
        if box:
            w, h = float(box[0]), float(box[1])
            if w <= 0 or h <= 0:
                fail(f"页{page}: targetBox 宽高必须 >0")
            formula_z = 0.8 / max(w / 1920, h / 1080)
            lo, hi = snap_to_band(formula_z)
            report(
                lo - 0.05 <= z1 <= hi + 0.05,
                "FAIL",
                page,
                f"定景公式 0.8/max({w:g}/1920,{h:g}/1080)={formula_z:.2f} 定档 [{lo},{hi}]，zoomEnd={z1} 须落档内",
            )

    if orbit_pages > 1:
        fails += 1
        print(
            f"[FAIL] 全 deck 环绕 {orbit_pages} 页 >1（一种手法全 deck 只当一次主角）"
        )

    print(f"--- 分镜校验汇总: {len(shots)} 镜, FAIL={fails}, WARN={warns} ---")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
