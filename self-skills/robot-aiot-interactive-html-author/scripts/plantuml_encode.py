#!/usr/bin/env python3
"""PlantUML 官方 text-encoding 编码器（diagram-embed-rendering.md §2.1 条 1-3）。

用法:
  python3 plantuml_encode.py diagram.puml              # 文件 → 编码串
  cat diagram.puml | python3 plantuml_encode.py -      # stdin → 编码串
  python3 plantuml_encode.py diagram.puml --url        # 输出完整 SVG URL
  python3 plantuml_encode.py diagram.puml --format png --server http://127.0.0.1:8080

规则:
  - 源码不含 @start/@end 时自动包裹 @startuml ... @enduml（条 1）
  - UTF-8 字节 → Deflate level 9（raw deflate，无 zlib 头）→ PlantUML 专用
    base64 变体（6-bit 映射表 0-9A-Za-z-_，无 padding）（条 2）
  - URL 拼接 <server>/svg/<encoded> 或 /png/（条 3）；默认公共服务器，
    涉密/内网图表禁止发往公共服务器，用 --server 指向本地（条 4）
"""

import argparse
import sys
import zlib

B64_MAP = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
DEFAULT_SERVER = "https://www.plantuml.com/plantuml"


def deflate9(data: bytes) -> bytes:
    co = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    return co.compress(data) + co.flush()


def encode6bit(data: bytes) -> str:
    out = []
    for i in range(0, len(data), 3):
        chunk = data[i : i + 3]
        b1 = chunk[0]
        b2 = chunk[1] if len(chunk) > 1 else 0
        b3 = chunk[2] if len(chunk) > 2 else 0
        out.append(B64_MAP[b1 >> 2])
        out.append(B64_MAP[((b1 & 0x3) << 4) | (b2 >> 4)])
        out.append(B64_MAP[((b2 & 0xF) << 2) | (b3 >> 6)])
        out.append(B64_MAP[b3 & 0x3F])
    return "".join(out)


def plantuml_encode(text: str) -> str:
    return encode6bit(deflate9(text.encode("utf-8")))


def ensure_wrapper(src: str) -> str:
    if "@start" in src and "@end" in src:
        return src
    return "@startuml\n" + src.strip() + "\n@enduml\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="PlantUML 源码文件路径，'-' 读 stdin")
    ap.add_argument("--url", action="store_true", help="输出完整渲染 URL")
    ap.add_argument("--format", choices=["svg", "png"], default="svg")
    ap.add_argument("--server", default=DEFAULT_SERVER)
    ap.add_argument(
        "--no-wrap", action="store_true", help="不自动包裹 @startuml/@enduml"
    )
    args = ap.parse_args()

    if args.source == "-":
        src = sys.stdin.read()
    else:
        try:
            with open(args.source, encoding="utf-8") as f:
                src = f.read()
        except OSError as e:
            print(f"FAIL 读取源码失败: {e}", file=sys.stderr)
            sys.exit(1)
    if not src.strip():
        print("FAIL 源码为空", file=sys.stderr)
        sys.exit(1)

    if not args.no_wrap:
        src = ensure_wrapper(src)
    encoded = plantuml_encode(src)
    if args.url:
        print(f"{args.server.rstrip('/')}/{args.format}/{encoded}")
    else:
        print(encoded)


if __name__ == "__main__":
    main()
